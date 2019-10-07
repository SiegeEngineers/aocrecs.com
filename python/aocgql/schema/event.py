"""Event schema."""
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from aocref import model
from mgzdb import schema
from aocgql.participants import compute_participants
from aocgql.schema.match import MatchHits, Match


# pylint: disable=no-member, missing-docstring, too-few-public-methods


class Event(SQLAlchemyObjectType):
    """Event."""
    class Meta:
        model = model.Event


class Tournament(SQLAlchemyObjectType):
    """Tournament."""
    class Meta:
        model = model.Tournament


class Round(SQLAlchemyObjectType):
    """Round."""
    class Meta:
        model = model.Round


class SeriesMetadata(SQLAlchemyObjectType):
    """Series Metadata."""
    class Meta:
        model = schema.SeriesMetadata


class Side(SQLAlchemyObjectType):
    """Side."""
    class Meta:
        model = model.Participant

    user_ids = graphene.List(graphene.String)
    users = graphene.List('aocgql.schema.User')

    def resolve_users(self, info):
        """Resolve Voobly Users participating in series."""
        return info.context['loaders'].user.load_many([
            (user_id, 'voobly') for user_id in self.user_ids # pylint: disable=not-an-iterable
        ])


class Series(SQLAlchemyObjectType):
    """Series."""
    class Meta:
        model = model.Series

    matches = graphene.Field(MatchHits, offset=graphene.Int(default_value=0), limit=graphene.Int(default_value=10))
    sides = graphene.List(Side)

    def resolve_matches(self, info, offset, limit):
        """Resolve matches played on this map."""
        query = Match.get_query(info).filter_by(series_id=self.id)
        return MatchHits(query=query, offset=offset, limit=limit)

    def resolve_sides(self, _):
        """Resolve series participants (always two).

        Only series derived from Challonge have participants.
        """
        return [
            Side(**data)
            for data in compute_participants(self.matches, self.participants)
        ]
