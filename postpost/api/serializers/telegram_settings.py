from rest_framework import serializers

from api import models


class TelegramChannelSettingsSerializer(serializers.ModelSerializer):
    """
    Serializer for telegram_group type of PlatformPost.
    """

    class Meta(object):
        model = models.PlatformPost
        fields = [
            'id',
            'platform_type',
            'current_status',
            'text',
            'telegram_picture_as_link',
            'telegram_markdown',
        ]
