from pyuploadcare.dj import models as uploadcare_models
from rest_framework import serializers

from api import models


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
