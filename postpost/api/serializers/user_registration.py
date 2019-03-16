from datetime import timedelta

from django.contrib.auth import models as contrib_models
from django.utils import timezone
from oauth2_provider.models import AccessToken, Application, RefreshToken
from oauth2_provider.settings import oauth2_settings
from oauthlib import common  # noqa: F401
from pyuploadcare.dj import models as uploadcare_models  # noqa: F401
from rest_framework import serializers  # noqa: F401
from rest_framework.validators import UniqueValidator  # noqa: F401


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
