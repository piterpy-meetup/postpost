from rest_framework import serializers

from api import models


class AttachmentSerializer(serializers.ModelSerializer):
    """
    Serializer for attachments.
    """

    class Meta(object):
        model = models.Attachment
        fields = [
            'attachment',
        ]
