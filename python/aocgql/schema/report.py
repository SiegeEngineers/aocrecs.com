"""Report schema."""
import datetime
import dateutil.relativedelta

import graphene

from sqlalchemy import extract, distinct, func, and_

from mgzdb import schema

from aocgql import report
from aocgql.schema.match import Match
from aocgql.schema.stats import MapStat
from aocgql.schema.user import MetaLadderRank, User


class UserStat(graphene.ObjectType):
    """User statistic."""

    user_id = graphene.String()
    platform_id = graphene.String()
    user = graphene.Field(User)
    rank = graphene.Int()
    change = graphene.Int()
    count = graphene.Int()

    def resolve_user(self, info):
        """Resolve associated user."""
        return info.context['loaders'].user.load((self.user_id, self.platform_id))


class ImprovementStat(graphene.ObjectType):
    """Improvement statistic."""

    user_id = graphene.String()
    platform_id = graphene.String()
    user = graphene.Field(User)
    min_rate = graphene.Int()
    max_rate = graphene.Int()
    diff_rate = graphene.Int()
    count = graphene.Int()
    wins = graphene.Int()
    losses = graphene.Int()

    def resolve_user(self, info):
        """Resolve associated user."""
        return info.context['loaders'].user.load((self.user_id, self.platform_id))


class Report(graphene.ObjectType):
    """Stats."""

    year = graphene.Int()
    month = graphene.Int()
    popular_maps = graphene.List(MapStat)
    longest_matches = graphene.List(Match)
    most_matches = graphene.List(UserStat, platform_id=graphene.String())
    most_improvement = graphene.List(ImprovementStat, platform_id=graphene.String(), ladder_id=graphene.Int())
    rankings = graphene.List(MetaLadderRank, platform_id=graphene.String(), ladder_id=graphene.Int())
    total_matches = graphene.Int()
    total_players = graphene.Int()

    def month_filters(self):
        """Generate month filters."""
        prev = datetime.date(self.year, self.month, 1) - dateutil.relativedelta.relativedelta(months=1)
        filters = and_(
            extract('year', schema.Match.played) == self.year,
            extract('month', schema.Match.played) == self.month
        )
        prev_filters = and_(
            extract('year', schema.Match.played) == prev.year,
            extract('month', schema.Match.played) == prev.month
        )
        return filters, prev_filters

    def resolve_popular_maps(self, info):
        """Resolve popular maps."""
        filters, prev_filters = self.month_filters()
        return [MapStat(
            name=stat['item']['key'],
            count=stat['item']['num'],
            percent=stat['item']['percent'],
            rank=stat['rank'],
            change=stat['change']
        ) for stat in report.popular_maps(info.context['session'], filters, prev_filters)]

    def resolve_longest_matches(self, info):
        """Resolve longest matches."""
        filters, _ = self.month_filters()
        return report.longest_matches(info.context['session'], filters)

    def resolve_most_matches(self, info, platform_id):
        """Resolve most matches."""
        filters, _ = self.month_filters()
        return [UserStat(
            user_id=r['user_id'],
            platform_id=platform_id,
            count=r['count'],
        ) for r in report.most_matches(info.context['session'], filters, platform_id)]

    def resolve_most_improvement(self, info, platform_id, ladder_id):
        """Resolve most improved players."""
        filters, _ = self.month_filters()
        return [ImprovementStat(
            user_id=i[0],
            platform_id=platform_id,
            min_rate=i[1],
            max_rate=i[2],
            diff_rate=i[3],
            count=i[4],
            wins=i[5],
            losses=i[6]
        ) for i in report.most_improvement(info.context['session'], filters, platform_id, ladder_id)]

    def resolve_rankings(self, info, platform_id, ladder_id):
        """Resolve ladder rankings."""
        filters, prev_filters = self.month_filters()
        return [MetaLadderRank(
            user_id=r['item'].user_id,
            user_name=r['item'].user_name,
            rank=r['rank'],
            rating=r['item'].rate_after,
            ladder_id=ladder_id,
            platform_id=platform_id,
            change=r['change']
        ) for r in report.rankings(info.context['session'], filters, prev_filters, platform_id, ladder_id)]

    def resolve_total_matches(self, info):
        """Resolve total matches."""
        filters, _ = self.month_filters()
        return info.context['session'] \
            .query(func.count(schema.Match.id).filter(filters)) \
            .first()[0]

    def resolve_total_players(self, info):
        """Resolve total players."""
        filters, _ = self.month_filters()
        return Match.get_query(info) \
            .join(schema.Player) \
            .filter(filters) \
            .with_entities(func.count(distinct(schema.Player.user_id))) \
            .first()[0]
