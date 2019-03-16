from rest_framework import serializers

from api import models


class VKGroupSettingsSerializer(serializers.ModelSerializer):
    """
    Serializer for vk_group type of PlatformPost.
    """

    class Meta(object):
        model = models.PlatformPost
        fields = [
            'id',
            'platform_type',
            'current_status',
            'text',
            'vk_clear_markdown',
        ]
