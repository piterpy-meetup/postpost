from django.db import models
from rest_framework.request import Request

from api import permissions


class Workspace(models.Model):
    """
    Workspace — space with members, publications and tuned platforms. Has a unique name.
    """

    name = models.SlugField(unique=True)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    @staticmethod
    def has_list_permission(request: Request) -> bool:
        return permissions.check_authenticated(request)

    @staticmethod
    def has_create_permission(request: Request) -> bool:
        return permissions.check_authenticated(request)