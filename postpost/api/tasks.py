import logging
import os
from datetime import datetime, timezone

import requests
from celery import shared_task
from celery.schedules import crontab
from celery.task import periodic_task

from api.models import PlatformPost


logger = logging.getLogger(__name__)


@shared_task
def send_post_to_telegram_channel(scheduled_post_id: int):
    post = PlatformPost.objects.select_related('publication').get(id=scheduled_post_id)
    # FIXME: переменные вынести в конфиг-файл
    # TODO: перенести работу с отправкой сообщений в внешний модуль из тасок
    telegram_response = requests.post(
        'https://api.telegram.org/bot{0}/sendMessage'.format(
            os.environ['BOT_TOKEN']
        ),
        json={
            'chat_id': os.environ['TELEGRAM_CHANNEL_ID'],
            'text': post.text_for_posting
        }
    )
    if telegram_response.status_code != 200:
        logger.error('Error by telegram API: %s', telegram_response.content)
        post.current_status = PlatformPost.FAILED_STATUS
    else:
        post.current_status = PlatformPost.SUCCESS_STATUS
    post.save()


@shared_task
def send_post_to_vk_channel(scheduled_post_id: int):
    pass


PLATFORM_TASK_MAPPING = {
    PlatformPost.VK_GROUP_TYPE: send_post_to_vk_channel,
    PlatformPost.TELEGRAM_CHANNEL_TYPE: send_post_to_telegram_channel,
}


@periodic_task(run_every=crontab(minute='*', hour='*', day_of_month='*'))
def send_scheduled_posts():
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
