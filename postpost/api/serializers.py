from typing import Sequence

from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from api import models


class VKGroupSettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PlatformPost
        fields = [
            'id',
            'platform_type',
            'current_status',
            'text',
            'vk_clear_markdown',
        ]


class TelegramChannelSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PlatformPost
        fields = [
            'id',
            'platform_type',
            'current_status',
            'text',
            'telegram_picture_as_link',
            'telegram_markdown',
        ]


class PlatformSettingsRelatedField(serializers.ModelSerializer):
    serializers_by_type = {
        models.PlatformPost.VK_GROUP_TYPE: VKGroupSettingsSerializer,
        models.PlatformPost.TELEGRAM_CHANNEL_TYPE: TelegramChannelSettingsSerializer,
        models.PlatformPost.TELEGRAM_SUPERGROUP_TYPE: TelegramChannelSettingsSerializer,  # FIXME
    }

    def to_representation(self, platform_settings: models.PlatformPost) -> dict:
        serializer = self.serializers_by_type.get(platform_settings.platform_type)
        if not serializer:
            raise Exception('Unknown type of platform')
        return serializer().to_representation(platform_settings)

    def to_internal_value(self, data: dict) -> models.PlatformPost:
        platform_type = data.get('platform_type')
        serializer = self.serializers_by_type.get(platform_type)
        if not serializer:
            raise serializers.ValidationError({'platform_type': 'Unknown type of platform'})

        return serializer().to_internal_value(data)

    class Meta:
        model = models.PlatformPost
        fields = '__all__'


class PublicationSerializer(WritableNestedModelSerializer):
    platform_posts = PlatformSettingsRelatedField(
        many=True,
    )

    class Meta:
        model = models.Publication
        fields = [
            'id',
            'text',
            'picture',
            'scheduled_at',
            'current_status',
            'platform_posts',
            'created_at',
            'updated_at',
        ]

    def validate_platform_posts(self, platform_posts: Sequence[models.PlatformPost]):
        if len(platform_posts) == 0:
            raise serializers.ValidationError("Must be set one or more platform settings")
