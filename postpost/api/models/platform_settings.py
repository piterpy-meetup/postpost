from django.db import models


class PlatformPost(models.Model):
    """
    Big model with all of possible settings for all used platforms for posting.
    """

    # Easy for using in filtering without hardcoding database-level constant, like
    # `PlatformPost.objects.filter(platform_type=PlatformPost.VK_GROUP_TYPE))`
    TELEGRAM_CHANNEL_TYPE = 'telegram_channel'
    TELEGRAM_SUPERGROUP_TYPE = 'telegram_supergroup'
    VK_GROUP_TYPE = 'vk_group'
    PLATFORM_TYPES = [
        (TELEGRAM_CHANNEL_TYPE, 'Telegram Channel'),
        (TELEGRAM_SUPERGROUP_TYPE, 'Telegram Supergroup (chat)'),
        (VK_GROUP_TYPE, 'VK Group (public)'),
    ]

    SCHEDULED_STATUS = 'scheduled'
    SENDING_STATUS = 'sending'
    FAILED_STATUS = 'failed'
    SUCCESS_STATUS = 'success'
    PLATFORM_STATUSES = [
        (SCHEDULED_STATUS, 'Post was scheduled'),
        (SENDING_STATUS, 'Post is sending'),
        (FAILED_STATUS, 'Sending was failed'),
        (SUCCESS_STATUS, 'Sending was success'),
    ]

    publication = models.ForeignKey(
        'Publication',
        on_delete=models.CASCADE,
        related_name='platform_posts',
    )

    platform_type = models.CharField(max_length=32, choices=PLATFORM_TYPES)  # noqa: Z432
    text = models.TextField(blank=True)
    current_status = models.CharField(
        max_length=32,  # noqa: Z432
        choices=PLATFORM_STATUSES,
        default=SCHEDULED_STATUS,
        editable=False,
    )

    vk_clear_markdown = models.NullBooleanField(default=True)

    telegram_picture_as_link = models.NullBooleanField(default=True)
    telegram_markdown = models.NullBooleanField(default=True)

    @property
    def text_for_posting(self) -> str:
        """
        Platform post text more specific then publication text, then override if set.
        """
        text: str = self.text or self.publication.text
        return text
