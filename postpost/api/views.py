from django.contrib.auth import models as contrib_models
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from api import models, serializers
from api.permissions import IsWorkspaceMember


class WorkspacePublication(viewsets.ModelViewSet):
    """
    View for get, delete and change publication entity.
    """

    permission_classes = [IsAuthenticated, IsWorkspaceMember]
    serializer_class = serializers.PublicationSerializer

    def get_queryset(self):
        """
        ASA.
        """
        return models.Publication.objects.filter(
            workspace=self.request.workspace,
        )


class UserRegistration(viewsets.ModelViewSet):
    """
    Register user and generate access/refresh token immediately.
    """

    permission_classes = [AllowAny]
    serializer_class = serializers.UserRegistrationSerializer
    queryset = contrib_models.User.objects.all()


class Workspace(viewsets.ModelViewSet):
    """
    Aaa.
    """
    lookup_field = 'name'

    permission_classes = [IsAuthenticated]
    serializer_class = serializers.WorkspaceSerializer
    queryset = models.Workspace.objects.all()
