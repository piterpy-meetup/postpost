from django.conf import settings
from django.db import models

from api.models.workspace import Workspace

PUBLISHER_ROLE = 'publisher'
ADMIN_ROLE = 'admin'
WORKSPACE_ROLES = [
    (PUBLISHER_ROLE, 'Publisher: only create and edit publications'),
    (ADMIN_ROLE, 'Admin: also can edit platforms and members'),
]


class WorkspaceMember(models.Model):
    """
    Many-to-many junction table user <-> workspace with role.
    """

    member = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=False,
    )
    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        null=False,
    )
    role = models.CharField(
        choices=WORKSPACE_ROLES,
        default=PUBLISHER_ROLE,
        null=False,
        max_length=64,  # noqa: Z432
    )

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta(object):
        unique_together = ('member', 'workspace')
