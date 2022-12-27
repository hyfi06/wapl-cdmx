"""Hotspot views."""

# django
from django.db.models import F
from django.db.models.functions import Power

# drf
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter

# wapl
from wapl.hotspots.models import Hotspot

# Utils
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import HotspotSerializer


class HotspotsViewSet(ReadOnlyModelViewSet):
    """This class manage Hotspots Views. By business logic, it is read-only
        Querys:
        - detail by name of hotspot
        - search by name and address
        - filter by name, address and program
        - list sorted by proximity to given latitude and longitude
    """
    serializer_class = HotspotSerializer
    queryset = Hotspot.objects.all()
    lookup_field = "name"
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'address']
    filterset_fields = ['name', 'address', 'program']

    def get_queryset(self, *args, **kwargs):
        """by business logic, when query have latitude and longitude as parameters, the queryset will be sorted by distance to given latitude and longitude"""
        queryset = Hotspot.objects.all()
        if self.action == 'list':
            if "lat" in self.request.query_params and "long" in self.request.query_params:
                lat = float(self.request.query_params["lat"])
                long = float(self.request.query_params["long"])
                return queryset.annotate(
                    distance=(Power(F('lat') - lat, 2) + Power(F('long') - long, 2))
                ).order_by('distance')
        return queryset
