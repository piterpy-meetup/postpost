from drf_writable_nested import WritableNestedModelSerializer

from api import models
from api.serializers.platform_settings_field import PlatformSettingsRelatedField


class PublicationSerializer(WritableNestedModelSerializer):
    """
    Serializer for publication with platform posts field.
    """

    platform_posts = PlatformSettingsRelatedField(
        many=True,
    )

    class Meta(object):
        model = models.Publication
        fields = [
            'id',
            'text',
            'attachments',
            'scheduled_at',
            'current_status',
            'platform_posts',
            'created_at',
            'updated_at',
        ]
