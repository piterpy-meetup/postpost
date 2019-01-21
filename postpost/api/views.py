from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from api import models, serializers


class PublicationList(ListCreateAPIView):
    """
    Very basic view for Publications objects.
    """

    queryset = models.Publication.objects.all()
    serializer_class = serializers.PublicationSerializer


class Publication(RetrieveUpdateDestroyAPIView):
    """
    Very basic view for Publication object.
    """

    queryset = models.Publication.objects.all()
    serializer_class = serializers.PublicationSerializer
