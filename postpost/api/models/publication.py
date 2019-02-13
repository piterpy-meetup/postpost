from django.db import models
from pyuploadcare.dj import models as uploadcare_models
from rest_framework.request import Request

from api import permissions
from api.models import PlatformPost
from api.models.workspace import Workspace


class Publication(models.Model):
    """
    Model for basic post. Text and picture may be override by each PlatformPost.
    """

    text = models.TextField()
    picture = uploadcare_models.ImageField(blank=True, null=True)

    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, null=False)
    scheduled_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    @property
    def current_status(self) -> str:
        """
        Return current status of publication based on platform posts statuses.
        """
        statuses = [platform.current_status for platform in self.platform_posts.all()]
        if len(set(statuses)) == 1:
            return statuses[0]

        if PlatformPost.FAILED_STATUS in statuses:
            # if one or more platform is failed,
            # post also is failed
            return PlatformPost.FAILED_STATUS
        elif PlatformPost.SENDING_STATUS in statuses:  # same with sending status
            return PlatformPost.SENDING_STATUS
        else:
            return PlatformPost.SUCCESS_STATUS

    @staticmethod
    def has_read_permission(request: Request) -> bool:
        return permissions.check_workspace_member(request)

    @staticmethod
    def has_write_permission(request: Request) -> bool:
        return permissions.check_workspace_member(request)
