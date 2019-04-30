import logging
import os
from datetime import datetime
from typing import Dict

import requests
from celery import shared_task
from celery.local import Proxy
from celery.schedules import crontab
from celery.task import periodic_task

from api.models import PlatformPost
from gates import telegram, vkontakte

logger = logging.getLogger(__name__)


@shared_task  # type: ignore
def send_post_to_telegram_channel(scheduled_post_id: int):
    """
    Celery task which try to send post to telegram and change status of platform post.
    """
    post = PlatformPost.objects.select_related('publication').get(id=scheduled_post_id)
    # FIXME: переменные вынести в конфиг-файл
    try:
        telegram.send_post_to_telegram_chat(
            token=os.environ['BOT_TOKEN'],
            chat_id=os.environ['TELEGRAM_CHANNEL_ID'],
            post=post,
        )
        post.current_status = PlatformPost.SUCCESS_STATUS
    except requests.HTTPError as error:
        logger.error('Error by telegram API: %s', str(error))
        post.current_status = PlatformPost.FAILED_STATUS
    post.save()


@shared_task  # type: ignore
def send_post_to_vk_group(scheduled_post_id: int):
    """
    Celery task which tries to send post to vk and changes status of platform post.
    """
    post = PlatformPost.objects.select_related('publication').get(id=scheduled_post_id)
    try:
        vkontakte.send_post_to_group(
            token=os.environ['VK_TOKEN'],
            group_id=os.environ['VK_GROUP_ID'],
            api_version=os.environ['VK_API_VERSION'],
            post=post,
        )
        post.current_status = PlatformPost.SUCCESS_STATUS
    except vkontakte.VkAPIError as error:
        logger.error('Error by vk API: %s', str(error))
        post.current_status = PlatformPost.FAILED_STATUS
    post.save()


PLATFORM_TASK_MAPPING: Dict[str, Proxy] = {
    PlatformPost.TELEGRAM_CHANNEL_TYPE: send_post_to_telegram_channel,
    PlatformPost.VK_GROUP_TYPE: send_post_to_vk_group,
}


@periodic_task(run_every=crontab(minute='*', hour='*', day_of_month='*'))
def send_scheduled_posts():
    """
    Iterate over unsent platform post and dispatch their to platform-specific sending functions.
    """
    unsent_posts = PlatformPost.objects.filter(
        current_status=PlatformPost.SCHEDULED_STATUS,
        publication__scheduled_at__lte=datetime.now(),
    )
    logger.info('%s unsent platform-specific post found', unsent_posts.count())
    scheduled_posts = list(unsent_posts)  # get sql select before updating
    unsent_posts.update(current_status=PlatformPost.SENDING_STATUS)

    for post in scheduled_posts:
        task = PLATFORM_TASK_MAPPING.get(post.platform_type)
        if task is None:
            logger.error('Unsupported platform type for posting: %s', post.platform_type)
            post.current_status = PlatformPost.FAILED_STATUS
            post.save()
        else:
            logger.info('Add post with id %s to queue', post.id)
            task.delay(post.id)
