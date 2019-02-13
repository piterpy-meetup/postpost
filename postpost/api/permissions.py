from rest_framework import permissions
from rest_framework.request import Request

from api.models import WorkspaceMember
from api.models.workspace_member import ADMIN_ROLE


def check_authenticated(request: Request):
    return request.user.is_authenticated


def check_workspace_admin(request: Request):
    """
    Checks that the user role is admin role in current workspace.
    """
    is_workspace_admin = WorkspaceMember.objects.filter(
        workspace=request.workspace,
        member=request.user,
        role=ADMIN_ROLE,
    ).exists()
    return is_workspace_admin


def check_workspace_member(request: Request):
    """
    Just check user membership in current workspace.
    """
    is_workspace_member = WorkspaceMember.objects.filter(
        workspace=request.workspace,
        member=request.user,
    ).exists()
    return is_workspace_member


def check_superuser(request: Request):
    """
    Check standard django is_superuser flag :shrug:.

    More info:
    https://docs.djangoproject.com/en/2.1/ref/contrib/auth/#django.contrib.auth.models.User.is_superuser
    """
    is_superuser = request.user.is_authenticated() and request.user.is_superuser
    return is_superuser
