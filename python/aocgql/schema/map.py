"""Map schema."""
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from aocref import model
from aocgql.stats import civs_per_map

from aocgql.schema.civilization import Civilization
from aocgql.schema.match import MatchHits, Match


# pylint: disable=too-few-public-methods, missing-docstring


class BuiltinMap(SQLAlchemyObjectType):
    """Builtin map."""
    class Meta:
        model = model.Map


class EventMap(SQLAlchemyObjectType):
    """Event map."""
    class Meta:
        model = model.EventMap


class MapPopularCiv(graphene.ObjectType):
    """Civilization stat."""

    percent = graphene.Float()
    civilization = graphene.Field(Civilization)
    civilization_id = graphene.Int()
    dataset_id = graphene.Int()

    def resolve_civilization(self, info):
        """Resolve associated civilization."""
        return info.context['loaders'].civilization.load((self.civilization_id, self.dataset_id))


class Map(graphene.ObjectType):
    """Map."""
    name = graphene.String()
    event_maps = graphene.List(lambda: EventMap)
    matches = graphene.Field(MatchHits, offset=graphene.Int(default_value=0),
                             limit=graphene.Int(default_value=3))
    popular_civs = graphene.List(MapPopularCiv, limit=graphene.Int(default_value=3))
    builtin = graphene.Boolean()

    def resolve_event_maps(self, info):
        return info.context['loaders'].event_map.load(self.name)

    def resolve_matches(self, info, offset, limit):
        """Resolve matches played on this map."""
        query = Match.get_query(info).filter_by(map_name=self.name)
        return MatchHits(query=query, offset=offset, limit=limit)

    def resolve_builtin(self, info):
        """Resolve whether this map is a builtin."""
        return info.context['loaders'].builtin_map.load(self.name)

    def resolve_popular_civs(self, info, limit):
        """Resolve popular civilizations on this map (only WK)."""
        session = info.context['session']
        result = civs_per_map(session, self.name)
        return [MapPopularCiv(civilization_id=stat['key'], dataset_id=1, percent=stat['percent'])
                for stat in result][:limit]
