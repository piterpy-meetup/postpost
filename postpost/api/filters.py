from django_filters import rest_framework as filters

from api import models


class PublicationFilterSet(filters.FilterSet):
    """
    Uses for filtering in publication-list endpoint by query-string.
    """

    # scheduled=false is equivalent to scheduled_at__isnull=True
    scheduled = filters.BooleanFilter(
        field_name='scheduled_at',
        lookup_expr='isnull',
        exclude=True,
    )

    # If you want change this filtering, first read comment
    # for PlatformPost.PLATFORM_TYPES
    platform_types = filters.MultipleChoiceFilter(
        field_name='platform_posts__platform_type',
        choices=models.PlatformPost.PLATFORM_TYPES,
    )

    class Meta(object):
        model = models.Publication
        fields = ['scheduled', 'platform_types']
