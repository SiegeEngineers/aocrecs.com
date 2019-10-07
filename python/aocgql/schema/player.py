"""Player schema."""
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from mgzdb import schema
from aocgql.schema.user import User


# pylint: disable=no-member, too-few-public-methods, missing-docstring


class Player(SQLAlchemyObjectType):
    """Match player."""
    class Meta:
        model = schema.Player

    user = graphene.Field(User)
    feudal_time_secs = graphene.Int()
    castle_time_secs = graphene.Int()
    imperial_time_secs = graphene.Int()

    def resolve_feudal_time_secs(self, _):
        """Resolve feudal time in seconds."""
        if self.feudal_time:
            return self.feudal_time.total_seconds()
        return None

    def resolve_castle_time_secs(self, _):
        """Resolve castle time in seconds."""
        if self.castle_time:
            return self.castle_time.total_seconds()
        return None

    def resolve_imperial_time_secs(self, _):
        """Resolve imperial time in seconds."""
        if self.imperial_time:
            return self.imperial_time.total_seconds()
        return None

    def resolve_user(self, info):
        """Resolve user associated with player."""
        if self.platform:
            return info.context['loaders'].user.load((self.user_id, self.platform_id))
        return None
