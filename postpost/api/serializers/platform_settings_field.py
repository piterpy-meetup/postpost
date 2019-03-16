from typing import Dict, Type

from rest_framework import serializers

from api import models
from api.serializers.telegram_settings import TelegramChannelSettingsSerializer
from api.serializers.vk_settings import VKGroupSettingsSerializer
from custom_types import JSON


class PlatformSettingsRelatedField(serializers.ModelSerializer):
    """
    Special hack field which on the fly change serializer class depending on platform_type.
    """

    serializers_by_type: Dict[str, Type[serializers.ModelSerializer]] = {
        models.PlatformPost.VK_GROUP_TYPE: VKGroupSettingsSerializer,
        models.PlatformPost.TELEGRAM_CHANNEL_TYPE: TelegramChannelSettingsSerializer,
        models.PlatformPost.TELEGRAM_SUPERGROUP_TYPE: TelegramChannelSettingsSerializer,  # FIXME
    }

    def to_representation(self, platform_settings: models.PlatformPost):  # noqa: D102
        serializer = self.serializers_by_type.get(
            platform_settings.platform_type,
        )
        if not serializer:
            raise Exception('Unknown type of platform')
        representation: JSON = serializer().to_representation(platform_settings)
        return representation

    def to_internal_value(self, native_values: JSON) -> models.PlatformPost:  # noqa: D102
        platform_type = native_values.get('platform_type')
        serializer = self.serializers_by_type.get(platform_type)
        if not serializer:
            raise serializers.ValidationError({'platform_type': 'Unknown type of platform'})

        return serializer().to_internal_value(native_values)

    class Meta(object):
        model = models.PlatformPost
        fields = '__all__'
