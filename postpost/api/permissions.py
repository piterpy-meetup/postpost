from rest_framework import permissions

from api.models import WorkspaceMember
from api.models.workspace_member import ADMIN_ROLE


class IsWorkspaceAdmin(permissions.BasePermission):
    """
    Permission check for workspace admin
    """

    def has_permission(self, request, view):
        is_workspace_admin = WorkspaceMember.objects.filter(
            workspace=request.workspace,
            member=request.user,
            role=ADMIN_ROLE,
        ).exists()
        return is_workspace_admin


class IsWorkspaceMember(permissions.BasePermission):
    """
    Permission check for workspace member
    """

    def has_permission(self, request, view):
        is_workspace_member = WorkspaceMember.objects.filter(
            workspace=request.workspace,
            member=request.user,
        ).exists()
        return is_workspace_member


