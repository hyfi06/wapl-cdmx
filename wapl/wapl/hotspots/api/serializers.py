
# drf
from rest_framework import serializers

# wapl
from wapl.hotspots.models import Hotspot


class HotspotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotspot
        fields = [
            "name", "program", "installed_date",
            "lat", "long", "address", "mayoralty"
        ]
