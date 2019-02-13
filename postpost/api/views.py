from django.contrib.auth import models as contrib_models
from dry_rest_permissions.generics import DRYPermissions
from rest_framework import mixins, viewsets, generics
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from api import models, serializers


class WorkspacePublication(viewsets.ModelViewSet):
    """
    View for get, delete and change publication entity.
    """

    permission_classes = [DRYPermissions]
    serializer_class = serializers.PublicationSerializer

    def get_queryset(self):
        """
        TODO: move this filter to `backend_filter`.
        """
        return models.Publication.objects.filter(
            workspace=self.request.workspace,
        )


class UserRegistration(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Register user and generate access/refresh token immediately.
    """

    permission_classes = [AllowAny]
    serializer_class = serializers.UserRegistrationSerializer
    queryset = contrib_models.User.objects.all()


class WorkspaceListCreate(generics.ListCreateAPIView):
    """
    Workspace views.
    """

    permission_classes = [DRYPermissions]
    serializer_class = serializers.WorkspaceSerializer

    def get_queryset(self):
        workspace_ids = models.WorkspaceMember.objects.select_related(
            'workspace',
        ).filter(
            member=self.request.user,
        ).values_list(
            'workspace',
            flat=True,
        )
        return models.Workspace.objects.filter(id__in=workspace_ids)


class WorkspaceMemberList(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    List of members available for all of workspace members.
    """

    serializer_class = serializers.PublicationSerializer
    permission_classes = [DRYPermissions]

    def get_queryset(self):
        """
        Filter members by current workspace.
        """
        return models.WorkspaceMember.objects.filter(
            workspace=self.request.workspace,
        ).select_related(
            'user',
        )


class WorkspaceMemberCreate(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Superuser view for creating member.

    For example, can used for emergency restoring workspace.
    """

    permission_classes = [DRYPermissions]
    serializer_class = serializers.PublicationSerializer  # FIXME


class WorkspaceMemberUpdateDestroy(
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    Allow removal membership and role changing for other members in workspace.
    """

    permission_classes = [DRYPermissions]
    serializer_class = serializers.PublicationSerializer  # FIXME

    def get_queryset(self):
        """
        Filter members by current workspace.
        """
        return models.WorkspaceMember.objects.filter(
            workspace=self.request.workspace,
        ).select_related(
            'user',
        )

