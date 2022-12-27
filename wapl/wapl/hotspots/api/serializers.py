"""Hotspots serializers"""

# drf
from rest_framework import serializers

# wapl
from wapl.hotspots.models import Hotspot


class HotspotSerializer(serializers.ModelSerializer):
    """This serializer manges Hotspot model."""
    class Meta:
        model = Hotspot
        fields = [
            "name", "program", "installed_date",
            "lat", "long", "address", "mayoralty"
        ]
