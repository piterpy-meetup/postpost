from typing import List

from django.db import models
from pyuploadcare.dj import models as uploadcare_models

from api.models import PlatformPost


class Publication(models.Model):
    """
    Model for basic post. Text and picture may be override by each PlatformPost.
    """

    text = models.TextField()
    picture = uploadcare_models.ImageField(blank=True, null=True)

    scheduled_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    @property
    def current_status(self) -> str:
        """
        Return current status of publication based on platform posts statuses.
        """
        statuses: List[str] = [platform.current_status for platform in self.platform_posts.all()]
        if len(set(statuses)) == 1:
            return statuses[0]

        status: str = PlatformPost.SUCCESS_STATUS
        if PlatformPost.FAILED_STATUS in statuses:
            # if one or more platform is failed,
            # post also is failed
            status = PlatformPost.FAILED_STATUS
        elif PlatformPost.SENDING_STATUS in statuses:  # same with sending status
            status = PlatformPost.SENDING_STATUS
        return status
