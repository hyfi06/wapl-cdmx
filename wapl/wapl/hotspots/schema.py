from django.db.models import F
from django.db.models.functions import Power

import graphene
from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from wapl.hotspots.models import Hotspot


class HotspotNode(DjangoObjectType):
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
    hotspots = relay.Node.Field(HotspotNode)
    all_hotspots = DjangoFilterConnectionField(HotspotNode)
    nearby_hotspots = DjangoFilterConnectionField(
        HotspotNode,
        lat=graphene.Float(),
        long=graphene.Float()
    )

    def resolve_nearby_hotspots(root, info, lat, long):
        return Hotspot.objects.all().annotate(
            distancie=(Power(F('lat') - lat, 2) + Power(F('long') - long, 2))
        ).order_by('distancie')
