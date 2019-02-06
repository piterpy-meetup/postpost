from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from api import models, serializers


class PublicationList(ListCreateAPIView):
    """
    Very basic view for Publications objects.
    """

    permission_classes = [IsAuthenticated]
    queryset = models.Publication.objects.all()
    serializer_class = serializers.PublicationSerializer


class Publication(RetrieveUpdateDestroyAPIView):
    """
    View for get, delete and change publication entity.
    """

    permission_classes = [IsAuthenticated]
    queryset = models.Publication.objects.all()
    serializer_class = serializers.PublicationSerializer


class UserRegistration(CreateAPIView):
    """
    Register user and generate access/refresh token immediately.
    """

    permission_classes = [AllowAny]
    serializer_class = serializers.UserRegistrationSerializer
