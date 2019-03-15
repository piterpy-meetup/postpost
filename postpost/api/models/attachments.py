from django.db import models
from pyuploadcare.dj import models as uploadcare_models


class Attachment(models.Model):
    """
    Attachment to post.
    """

    parent_publication = models.ForeignKey(
        'Publication',
        on_delete=models.CASCADE,
        related_name='attachments',
        )
    picture = uploadcare_models.ImageField(blank=True, null=True)
