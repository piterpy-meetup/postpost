from django.db import models


class Workspace(models.Model):
    """
    Workspace — space with members, publications and tuned platforms. Has a unique name.
    """

    name = models.SlugField(unique=True)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
