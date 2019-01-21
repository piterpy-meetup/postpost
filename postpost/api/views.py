from django.http import JsonResponse
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from api import models, serializers


class PublicationList(ListCreateAPIView):
    queryset = models.Publication.objects.all()
    serializer_class = serializers.PublicationSerializer


class Publication(RetrieveUpdateDestroyAPIView):
    queryset = models.Publication.objects.all()
    serializer_class = serializers.PublicationSerializer
