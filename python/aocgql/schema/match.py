"""Match schema."""
import graphene
from graphene.types.generic import GenericScalar
from graphene_sqlalchemy import SQLAlchemyObjectType

from sqlalchemy import desc, nullslast
from sqlalchemy.orm import load_only, joinedload

from aocref import model
from mgzdb import schema
from aocgql.odds import odds
from aocgql.search import execute


# pylint: disable=missing-docstring, no-member, too-few-public-methods


class Odds(graphene.ObjectType):
    """Odds."""
    teams = GenericScalar()
    teams_and_map = GenericScalar()
    teams_and_civilizations = GenericScalar()
    civilizations = GenericScalar()
    civilizations_and_map = GenericScalar()



class Match(SQLAlchemyObjectType):
    """Game match."""
    class Meta:
        model = schema.Match

    duration_secs = graphene.Int()
    odds = graphene.Field(Odds)

    def resolve_odds(self, info):
        """Resolve match odds."""
        params = {
            'teams': [[{
                'user_id': p.user_id,
                'civilization_id': p.civilization_id
            } for p in t.members] for t in self.teams],
            'map': self.map_name,
            'type_id': self.type_id
        }
        return Odds(**odds(info.context['session'], params))

    def resolve_duration_secs(self, _):
        """Resolve match duration in seconds."""
        return self.duration.total_seconds()


class MatchHits(graphene.ObjectType):
    """Match hits from search."""
    count = graphene.Int()
    query = GenericScalar()
    offset = graphene.Int()
    limit = graphene.Int()
    hits = graphene.List(Match)

    def resolve_hits(self, _):
        """Resolve match hits."""
        # eager join all the relationships needed to display a full match
        return self.query.options(joinedload(schema.Match.teams) \
            .joinedload(schema.Team.members) \
            .joinedload(schema.Player.civilization)) \
        .options(joinedload(schema.Match.event_map).joinedload(model.EventMap.event)) \
        .options(joinedload(schema.Match.files)) \
        .options(joinedload(schema.Match.dataset)) \
        .options(joinedload(schema.Match.platform)) \
        .options(joinedload(schema.Match.ladder)) \
        .options(joinedload(schema.Match.speed)) \
        .options(joinedload(schema.Match.difficulty)) \
        .options(joinedload(schema.Match.type)) \
        .options(joinedload(schema.Match.map_size)) \
        .options(joinedload(schema.Match.map_reveal_choice)) \
        .options(joinedload(schema.Match.series).joinedload(model.Series.metadata)) \
        .options(joinedload(schema.Match.tournament)) \
        .options(joinedload(schema.Match.event)) \
        .order_by(nullslast(desc(schema.Match.played))) \
        .offset(self.offset).limit(self.limit) \
        .all()

    def resolve_count(self, _):
        """Resolve result count."""
        return self.query.options(load_only('id')).count()


class Search(graphene.ObjectType):
    """Search result."""
    params = GenericScalar()
    matches = graphene.Field(MatchHits, offset=graphene.Int(default_value=0),
                             limit=graphene.Int(default_value=10))

    def resolve_matches(self, info, offset, limit):
        """Resolve match results."""
        query = execute(Match.get_query(info), self.params)
        return MatchHits(query=query, offset=offset, limit=limit)
