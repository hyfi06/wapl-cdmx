import graphene
import hotspots.schema


class Query(hotspots.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
