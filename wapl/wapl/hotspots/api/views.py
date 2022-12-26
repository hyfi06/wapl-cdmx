"""Hotspot views."""

from django.db.models import F
from django.db.models.functions import Power

# drf
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter

from django_filters.rest_framework import DjangoFilterBackend

# wapl
from wapl.hotspots.models import Hotspot

from .serializers import HotspotSerializer


class HotspotsViewSet(ReadOnlyModelViewSet):
    serializer_class = HotspotSerializer
    queryset = Hotspot.objects.all()
    lookup_field = "name"
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'address']
    filterset_fields = ['name', 'address', 'program']

    def get_queryset(self, *args, **kwargs):
        queryset = Hotspot.objects.all()
        if self.action == 'list':
            if "lat" in self.request.query_params and "long" in self.request.query_params:
                lat = float(self.request.query_params["lat"])
                long = float(self.request.query_params["long"])
                return queryset.annotate(
                    distancie=(Power(F('lat') - lat, 2) + Power(F('long') - long, 2))
                ).order_by('distancie')
        return queryset
