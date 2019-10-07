"""Stats schema."""

import dateparser
import graphene

from aocref import model
from mgzdb import schema

from aocgql import stats
from aocgql.schema.civilization import Civilization
from aocgql.schema.map import Map


# pylint: disable=no-self-use, too-few-public-methods, too-many-public-methods


def _pick_label(label):
    """Pick a label."""
    if isinstance(label, bool):
        return 'Yes' if label else 'No'
    return label


def _resolve_agg(info, *args, **kwargs):
    """Resolve an aggregation."""
    agg_func = stats.group_by
    if len(args) == 3:
        agg_func = stats.group_by_relation

    query = agg_func(info.context['session'], *args)
    if 'filter' in kwargs:
        query = query.filter(kwargs['filter'])

    return [StatItem(id=item[1], label=_pick_label(item[0]), count=item[2])
            for item in query.all() if item[1] is not None]


class Stat(graphene.ObjectType):
    """Stat."""
    count = graphene.Int()
    percent = graphene.Float()
    rank = graphene.Int()
    change = graphene.Int()


class CivilizationStat(Stat):
    """Civilization stat."""

    civilization = graphene.Field(Civilization)
    civilization_id = graphene.Int()
    dataset_id = graphene.Int()

    def resolve_civilization(self, info):
        """Resolve associated civilization."""
        return info.context['loaders'].civilization.load((self.civilization_id, self.dataset_id))


class MapStat(Stat, Map):
    """Map stat."""


class DateStat(graphene.ObjectType):
    """Daily stat."""
    date = graphene.Date()
    count = graphene.Int()


class StatItem(graphene.ObjectType):
    """Stat item."""
    id = graphene.String()
    label = graphene.String()
    count = graphene.Int()


class Stats(graphene.ObjectType):
    """Stats."""
    files = graphene.Int()
    matches = graphene.Int()
    series = graphene.Int()
    map_count = graphene.Int()
    users = graphene.Int()
    by_civilization = graphene.List(CivilizationStat, dataset_id=graphene.Int())
    by_map = graphene.List(MapStat)
    by_day = graphene.List(DateStat)
    platforms = graphene.List(StatItem)
    encodings = graphene.List(StatItem)
    datasets = graphene.List(StatItem)
    team_sizes = graphene.List(StatItem)
    diplomacy_types = graphene.List(StatItem)
    languages = graphene.List(StatItem)
    maps = graphene.List(StatItem)
    game_types = graphene.List(StatItem)
    speeds = graphene.List(StatItem)
    population_limits = graphene.List(StatItem)
    ladders = graphene.List(StatItem, platform_id=graphene.String())
    civilizations = graphene.List(StatItem, dataset_id=graphene.Int())
    events = graphene.List(StatItem)
    tournaments = graphene.List(StatItem)
    mirror = graphene.List(StatItem)
    rated = graphene.List(StatItem)
    rms_zr = graphene.List(StatItem)
    cheats = graphene.List(StatItem)
    lock_teams = graphene.List(StatItem)
    team_together = graphene.List(StatItem)
    lock_speed = graphene.List(StatItem)
    all_technologies = graphene.List(StatItem)
    winner = graphene.List(StatItem)
    mvp = graphene.List(StatItem)
    colors = graphene.List(StatItem)

    def resolve_files(self, info):
        """Resolve file count."""
        return info.context['session'].query(schema.File.id).count()

    def resolve_matches(self, info):
        """Resolve match count."""
        return info.context['session'].query(schema.Match.id).count()

    def resolve_series(self, info):
        """Resolve series count."""
        return info.context['session'].query(model.Series.id).count()

    def resolve_users(self, info):
        """Resolve user count."""
        return info.context['session'].query(schema.User.id).count()

    def resolve_map_count(self, info):
        """Resolve map count."""
        return info.context['session'].query(schema.Match.map_name).distinct().count()

    def resolve_civilizations(self, info, dataset_id):
        """Resolve civilization aggregation."""
        return _resolve_agg(
            info,
            model.Civilization.name, schema.Player, schema.Player.civilization_id,
            filter=(schema.Player.dataset_id == dataset_id)
        )

    def resolve_ladders(self, info, platform_id):
        """Resolve ladder aggregation."""
        return _resolve_agg(
            info,
            schema.Ladder.name, schema.Match, schema.Match.ladder_id,
            filter=(schema.Match.platform_id == platform_id)
        )

    def resolve_mirror(self, info):
        """Resolve mirror aggregation."""
        return _resolve_agg(info, schema.Match.mirror)

    def resolve_rated(self, info):
        """Resolve rated aggregation."""
        return _resolve_agg(info, schema.Match.rated)

    def resolve_rms_zr(self, info):
        """Resolve RMS ZR aggregation."""
        return _resolve_agg(info, schema.Match.rms_zr)

    def resolve_cheats(self, info):
        """Resolve cheat aggregation."""
        return _resolve_agg(info, schema.Match.cheats)

    def resolve_lock_teams(self, info):
        """Resolve lock team aggregation."""
        return _resolve_agg(info, schema.Match.lock_teams)

    def resolve_team_together(self, info):
        """Resolve team together aggregation."""
        return _resolve_agg(info, schema.Match.team_together)

    def resolve_lock_speed(self, info):
        """Resolve lock speed aggregation."""
        return _resolve_agg(info, schema.Match.lock_speed)

    def resolve_all_technologies(self, info):
        """Resolve all tech aggregation."""
        return _resolve_agg(info, schema.Match.all_technologies)

    def resolve_population_limits(self, info):
        """Resolve population limit aggregation."""
        return _resolve_agg(info, schema.Match.population_limit)

    def resolve_platforms(self, info):
        """Resolve platform aggregation."""
        return _resolve_agg(info, model.Platform.name, schema.Match, schema.Match.platform_id)

    def resolve_datasets(self, info):
        """Resolve dataset aggregation."""
        return _resolve_agg(info, model.Dataset.name, schema.Match, schema.Match.dataset_id)

    def resolve_events(self, info):
        """Resolve event aggregation."""
        return _resolve_agg(info, model.Event.name, schema.Match, schema.Match.event_id)

    def resolve_tournaments(self, info):
        """Resolve tournament aggregation."""
        return _resolve_agg(info, model.Tournament.name, schema.Match, schema.Match.tournament_id)

    def resolve_encodings(self, info):
        """Resolve encoding aggregation."""
        return _resolve_agg(info, schema.File.encoding)

    def resolve_languages(self, info):
        """Resolve language aggregation."""
        return _resolve_agg(info, schema.File.language)

    def resolve_team_sizes(self, info):
        """Resolve team size aggregation."""
        return _resolve_agg(info, schema.Match.team_size)

    def resolve_diplomacy_types(self, info):
        """Resolve diplomacy type aggregation."""
        return _resolve_agg(info, schema.Match.diplomacy_type)

    def resolve_maps(self, info):
        """Resolve map aggregation."""
        return _resolve_agg(info, schema.Match.map_name)

    def resolve_game_types(self, info):
        """Resolve game type aggregation."""
        return _resolve_agg(info, model.GameType.name, schema.Match, schema.Match.type_id)

    def resolve_speeds(self, info):
        """Resolve speed aggregation."""
        return _resolve_agg(info, model.Speed.name, schema.Match, schema.Match.speed_id)

    def resolve_colors(self, info):
        """Resolve color aggregation."""
        return _resolve_agg(info, model.PlayerColor.name, schema.Player, schema.Player.color_id)

    def resolve_winner(self, info):
        """Resolve winner aggregation."""
        return _resolve_agg(info, schema.Player.winner)

    def resolve_mvp(self, info):
        """Resolve MVP aggregation."""
        return _resolve_agg(info, schema.Player.mvp)

    def resolve_by_civilization(self, info, dataset_id):
        """Resolve matches by civilization."""
        session = info.context['session']
        result = stats.civs_per_dataset(session, dataset_id)
        return [
            CivilizationStat(
                civilization_id=stat['key'],
                dataset_id=dataset_id,
                count=stat['num'],
                percent=stat['percent']
            )
            for stat in result
        ]

    def resolve_by_map(self, info):
        """Resolve matches per map."""
        session = info.context['session']
        result = stats.maps(session)
        return [
            MapStat(name=stat['key'], count=stat['num'], percent=stat['percent'])
            for stat in result
        ]

    def resolve_by_day(self, info):
        """Resolve matches per day."""
        session = info.context['session']
        result = stats.matches_by_day(session)
        return [DateStat(
            date=dateparser.parse(x.date).date() if isinstance(x.date, str) else x.date,
            count=x.matches
        ) for x in result]
