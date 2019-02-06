from django.contrib.auth import models as contrib_models
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from api import models, serializers
from api.permissions import IsWorkspaceMember


class WorkspacePublication(viewsets.ModelViewSet):
    """
    Workspace publications entity view.
    """

    permission_classes = [IsAuthenticated, IsWorkspaceMember]
    serializer_class = serializers.PublicationSerializer

    def get_queryset(self):
        return models.Publication.objects.filter(
            workspace=self.request.workspace,
        )


class Workspace(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.WorkspaceSerializer
    queryset = models.Workspace.objects.all()


class UserRegistration(viewsets.ModelViewSet):
    """
    Register user and generate access/refresh token immediately.
    """

    permission_classes = [AllowAny]
    serializer_class = serializers.UserRegistrationSerializer
    queryset = contrib_models.User.objects.all()
