"""Hotspot schema"""

# graphene
import graphene
from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

# wapl
from wapl.hotspots.models import Hotspot

# Utilities
from django.db.models import F
from django.db.models.functions import Power

class HotspotNode(DjangoObjectType):
    """Object Type of Hotspot. 
        - Include all fields
        - Filter by name, program, installed_date, address and mayoralty
        - Use relay.Node as interfaces for pagination.
    """
    class Meta:
        model = Hotspot
        fields = "__all__"
        filter_fields = (
            "name", "program", "installed_date", "address", "mayoralty"
        )
        interfaces = (relay.Node,)


class HotspotConnection (relay.Connection):
    class Meta:
        node = HotspotNode


class Query(ObjectType):
    """Hotpost querys
        - Hotspots, get data by hotspot id
        - allHotspots, retrieve all hotspots
        - nearbyHotspots, retrieve near hotspots
    """
    hotspots = relay.Node.Field(HotspotNode)
    all_hotspots = DjangoFilterConnectionField(HotspotNode)
    nearby_hotspots = DjangoFilterConnectionField(
        HotspotNode,
        lat=graphene.Float(),
        long=graphene.Float()
    )

    def resolve_nearby_hotspots(root, info, lat, long):
        """by business logic, when query have latitude and longitude as parameters, the queryset will be sorted by distance to given latitude and longitude"""
        return Hotspot.objects.all().annotate(
            distancie=(Power(F('lat') - lat, 2) + Power(F('long') - long, 2))
        ).order_by('distancie')
