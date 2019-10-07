"""Civilization schema."""
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from aocref import model
from mgzdb import schema

from aocgql.schema.match import MatchHits, Match


# pylint: disable=no-member, missing-docstring, too-few-public-methods


class Civilization(SQLAlchemyObjectType):
    """Civilization."""
    class Meta:
        model = model.Civilization

    cid = graphene.Int()
    matches = graphene.Field(MatchHits, offset=graphene.Int(default_value=0),
                             limit=graphene.Int(default_value=3))

    def resolve_cid(self, _):
        """Resolve civilization id."""
        return self.id

    def resolve_matches(self, info, offset, limit):
        """Resolve matches played on this map."""
        query = Match.get_query(info) \
            .join(schema.Player) \
            .join(model.Civilization) \
            .filter(model.Civilization.id == self.id) \
            .filter(model.Civilization.dataset_id == self.dataset_id)
        return MatchHits(query=query, offset=offset, limit=limit)


class CivilizationBonus(SQLAlchemyObjectType):
    """Civilizationi bonus."""
    class Meta:
        model = model.CivilizationBonus
