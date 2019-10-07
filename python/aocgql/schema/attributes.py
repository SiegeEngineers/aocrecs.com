"""Passthrough attributes."""

import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from aocref import model
from mgzdb import schema


# pylint: disable=too-few-public-methods, missing-docstring


class Ladder(SQLAlchemyObjectType):
    """Ladders."""
    class Meta:
        model = schema.Ladder

    lid = graphene.Int()

    def resolve_lid(self, _):
        """Resolve ladder id."""
        return self.id # pylint: disable=no-member


class CanonicalPlayer(SQLAlchemyObjectType):
    """Dataset."""
    class Meta:
        model = model.CanonicalPlayer


class Dataset(SQLAlchemyObjectType):
    """Dataset."""
    class Meta:
        model = model.Dataset


class Platform(SQLAlchemyObjectType):
    """Platform."""
    class Meta:
        model = model.Platform


class File(SQLAlchemyObjectType):
    """Recorded game file."""
    class Meta:
        model = schema.File


class Team(SQLAlchemyObjectType):
    """Team membership."""
    class Meta:
        model = schema.Team


class GameType(SQLAlchemyObjectType):
    """Game type."""
    class Meta:
        model = model.GameType


class StartingResources(SQLAlchemyObjectType):
    """Starting resources."""
    class Meta:
        model = model.StartingResources


class VictoryCondition(SQLAlchemyObjectType):
    """Victory condition."""
    class Meta:
        model = model.VictoryCondition


class MapRevealChoice(SQLAlchemyObjectType):
    """Map reveal choice."""
    class Meta:
        model = model.MapRevealChoice


class StartingAge(SQLAlchemyObjectType):
    """Starting age."""
    class Meta:
        model = model.StartingAge


class Difficulty(SQLAlchemyObjectType):
    """Difficulty."""
    class Meta:
        model = model.Difficulty


class Speed(SQLAlchemyObjectType):
    """Speed."""
    class Meta:
        model = model.Speed


class MapSize(SQLAlchemyObjectType):
    """Map size."""
    class Meta:
        model = model.MapSize


class PlayerColor(SQLAlchemyObjectType):
    """Player color."""
    class Meta:
        model = model.PlayerColor
