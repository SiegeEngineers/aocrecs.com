"""Schema."""

import graphene
from graphene.types.generic import GenericScalar
from sqlalchemy.orm import joinedload
from sqlalchemy import extract

from aocref import model
from mgzdb import schema

from aocgql.const import LADDERS
from aocgql.odds import odds
from aocgql.report import available_reports
from aocgql.schema.attributes import Dataset, Platform
from aocgql.schema.civilization import Civilization
from aocgql.schema.event import Event, Tournament, Series
from aocgql.schema.map import Map
from aocgql.schema.match import Search, Match
from aocgql.schema.player import Player
from aocgql.schema.report import Report
from aocgql.schema.stats import Stats, CivilizationStat
from aocgql.schema.user import User, MetaLadder, MetaLadderRank


# pylint: disable=no-self-use, invalid-name, redefined-builtin


class Query(graphene.ObjectType):
    """Query start point."""

    events = graphene.List(Event)
    meta_ladders = graphene.List(MetaLadder, platform_id=graphene.String())
    datasets = graphene.List(Dataset)
    platforms = graphene.List(Platform)
    maps = graphene.List(Map)

    serie = graphene.Field(Series, id=graphene.String())
    match = graphene.Field(Match, match_id=graphene.Int())
    civilization = graphene.Field(Civilization, id=graphene.Int(), dataset_id=graphene.Int())
    map = graphene.Field(Map, name=graphene.String())
    tournament = graphene.Field(Tournament, id=graphene.String())
    user = graphene.Field(User, user_id=graphene.String(), platform_id=graphene.String())

    odds = graphene.Field(GenericScalar, params=GenericScalar())
    stats = graphene.Field(Stats)
    report = graphene.Field(Report, year=graphene.Int(), month=graphene.Int())
    reports = graphene.List(Report)
    search = graphene.Field(Search, params=GenericScalar())

    def resolve_meta_ladders(self, _, platform_id):
        """Resolve meta ladders."""
        return [MetaLadder(
            id=id,
            platform_id=platform_id,
            name=name
        ) for id, name in LADDERS[platform_id].items()]

    def resolve_events(self, info):
        """Resolve all events."""
        return Event.get_query(info) \
            .options(joinedload(model.Event.tournaments)) \
            .options(joinedload(model.Event.maps)).all()

    def resolve_datasets(self, info):
        """Resolve all datasets."""
        return Dataset.get_query(info).all()

    def resolve_platforms(self, info):
        """Resolve all platforms."""
        return Platform.get_query(info).all()

    def resolve_maps(self, info):
        """Resolve all maps."""
        return [
            Map(name=match.map_name)
            for match in info.context['session'].query(schema.Match.map_name).distinct().all()
        ]

    def resolve_serie(self, info, id):
        """Resolve a particular series."""
        return Series.get_query(info).get(id)

    def resolve_match(self, info, match_id):
        """Resolve a match."""
        return Match.get_query(info).get(match_id)

    def resolve_civilization(self, info, id, dataset_id):
        """Resolve a civilization."""
        return info.context['loaders'].civilization.load((id, dataset_id))

    def resolve_map(self, _, name):
        """Resolve a map."""
        return Map(name=name)

    def resolve_tournament(self, info, id):
        """Resolve a tournament."""
        return info.context['loaders'].tournament.load(id)

    def resolve_user(self, info, user_id, platform_id):
        """Resolve a user."""
        return info.context['loaders'].user.load((user_id, platform_id))

    def resolve_odds(self, info, params):
        """Resolve odds."""
        return odds(info.context['session'], params)

    def resolve_stats(self, _):
        """Resolve database stats."""
        return Stats()

    def resolve_report(self, _, year, month):
        """Resolve a report."""
        return Report(year=year, month=month)

    def resolve_reports(self, info):
        """Resolve all reports."""
        return [
            Report(year=int(report[0]), month=int(report[1]))
            for report in available_reports(info.context['session'])
        ]

    def resolve_search(self, _, params):
        """Resolve a search."""
        return Search(params=params)


SCHEMA = graphene.Schema(query=Query, auto_camelcase=False)
