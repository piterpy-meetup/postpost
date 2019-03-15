from datetime import timedelta
from typing import Dict, Sequence, Type

from django.contrib.auth import models as contrib_models
from django.utils import timezone
from drf_writable_nested import WritableNestedModelSerializer
from oauth2_provider.models import AccessToken, Application, RefreshToken
from oauth2_provider.settings import oauth2_settings
from oauthlib import common
from pyuploadcare.dj import models as uploadcare_models  # noqa: F401
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from api import models
from custom_types import JSON


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

    def validate_platform_posts(self, platform_posts: Sequence[models.PlatformPost]):
        """
        In publication must be one or more platform post.
        """
        if len(platform_posts) == 0:
            raise serializers.ValidationError('Must be set one or more platform settings')


class AttachmentSerializer(serializers.ModelSerializer):
    """
    Serializer for attachments.
    """

    picture = uploadcare_models.ImageField(blank=True, null=True)

    class Meta(object):
        model = models.Attachment
        fields = [
            'parent_publication',
            'picture',
        ]


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    Check user creds, create User and access/refresh token.
    """

    email = serializers.EmailField(
        required=True,
        allow_null=False,
        validators=[
            UniqueValidator(
                queryset=contrib_models.User.objects.all(),
                lookup='iexact',
            ),
        ],
    )
    username = serializers.SlugField(
        required=True,
        min_length=5,
        allow_null=False,
        validators=[
            UniqueValidator(
                queryset=contrib_models.User.objects.all(),
                lookup='iexact',
            ),
        ],
    )
    password = serializers.CharField(required=True, allow_null=False, write_only=True, min_length=8)
    client_id = serializers.CharField(required=True, allow_null=False, write_only=True)

    access_token = serializers.SerializerMethodField()
    refresh_token = serializers.SerializerMethodField()

    def get_access_token(self, _):
        """
        Getter for access token.
        """
        return self._access_token

    def get_refresh_token(self, _):
        """
        Getter for refresh token.
        """
        return self._refresh_token

    def create(self, validated_data):
        """
        Create User object and generate some oauth stuff like access/refresh token.
        """
        try:
            application = Application.objects.get(client_id=validated_data['client_id'])
        except Application.DoesNotExist:
            raise serializers.ValidationError('Invalid client id')
        user = contrib_models.User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        expires = timezone.now() + timedelta(seconds=oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS)

        access_token = AccessToken(
            user=user,
            scope='',
            expires=expires,
            token=common.generate_token(),
            application=application,
        )
        access_token.save()
        self._access_token = access_token.token

        refresh_token = RefreshToken(
            user=user,
            token=common.generate_token(),
            application=application,
            access_token=access_token,
        )
        refresh_token.save()
        self._refresh_token = refresh_token.token

        return user

    class Meta(object):
        model = contrib_models.User
        fields = [
            'id',
            'email',
            'username',
            'password',
            'client_id',
            'access_token',
            'refresh_token',
        ]
