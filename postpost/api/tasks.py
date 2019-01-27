import logging
import os
from datetime import datetime

import requests
from celery import shared_task
from celery.schedules import crontab
from celery.task import periodic_task

from api import vkontakte
from api.models import PlatformPost

logger = logging.getLogger(__name__)


@shared_task
def send_post_to_telegram_channel(scheduled_post_id: int):
    """
    Celery task which try to send post to telegram and change status of platform post.
    """
    post = PlatformPost.objects.select_related('publication').get(id=scheduled_post_id)
    # FIXME: переменные вынести в конфиг-файл
    # TODO: перенести работу с отправкой сообщений в внешний модуль из тасок
    telegram_response = requests.post(
        'https://api.telegram.org/bot{0}/sendMessage'.format(
            os.environ['BOT_TOKEN'],
        ),
        json={
            'chat_id': os.environ['TELEGRAM_CHANNEL_ID'],
            'text': post.text_for_posting,
        },
    )
    if telegram_response.status_code != requests.codes.ok:
        logger.error('Error by telegram API: %s', telegram_response.content)
        post.current_status = PlatformPost.FAILED_STATUS
    else:
        post.current_status = PlatformPost.SUCCESS_STATUS
    post.save()


@shared_task
def send_post_to_vk_group(scheduled_post_id: int):
    """
    Celery task which tries to send post to vk and changes status of platform post.
    """
    post = PlatformPost.objects.select_related('publication').get(id=scheduled_post_id)
    vk_response = vkontakte.send_post_to_group(
        token=os.environ['VK_TOKEN'],
        group_id=os.environ['VK_GROUP_ID'],
        api_version=os.environ['VK_API_VERSION'],
        message=post.text_for_posting,
        attachments=[],
    )
    if vk_response.status_code != requests.codes.ok or 'error' in vk_response.json():
        logger.error('Error by vk API: %s', vk_response.content)
        post.current_status = PlatformPost.FAILED_STATUS
    else:
        post.current_status = PlatformPost.SUCCESS_STATUS
    post.save()


PLATFORM_TASK_MAPPING = {
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
        logger.info('Add post with id %s to queue', post.id)
        task.delay(post.id)
