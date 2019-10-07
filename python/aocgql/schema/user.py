"""User schema."""
import dateparser
import graphene

from sqlalchemy import distinct, func, case

from aocref import model
from mgzdb import schema

from aocgql.const import LADDERS
from aocgql.stats import rate_by_day
from aocgql.metaladder import get_rank, get_ranks
from aocgql.schema.match import MatchHits, Match
from aocgql.schema.stats import DateStat
from aocgql.schema.civilization import Civilization
from aocgql.schema.attributes import Dataset
from aocgql.schema.map import Map


def get_aliases(session, user_id, platform_id):
    """Get all used names of a user."""
    all_names = session.query(schema.Player) \
        .with_entities(distinct(schema.Player.name), schema.Player.user_name) \
        .filter(schema.Player.platform_id == platform_id) \
        .filter(schema.Player.user_id == user_id) \
        .filter(schema.Player.human.is_(True))
    aliases = set()
    for names in all_names:
        aliases |= set(names)
    return aliases


class User(graphene.ObjectType):
    """Platform user."""

    id = graphene.String()
    platform_id = graphene.String()
    name = graphene.String()
    canonical_name = graphene.String()
    meta_ranks = graphene.List(lambda: MetaLadderRank)
    matches = graphene.Field(MatchHits, offset=graphene.Int(default_value=0), limit=graphene.Int(default_value=3))
    aliases = graphene.List(graphene.String)
    top_map = graphene.Field(Map)
    top_civilization = graphene.Field(Civilization)
    top_dataset = graphene.Field(Dataset)

    def resolve_top_map(self, info):
        """Resolve map most played."""
        return Map(name=Match.get_query(info) \
            .join(schema.Player) \
            .with_entities(func.count(schema.Match.id), schema.Match.map_name) \
            .filter(schema.Player.user_id == str(self.id), schema.Match.platform_id == self.platform_id) \
            .group_by(schema.Match.map_name) \
            .order_by(func.count(schema.Match.id).desc()) \
            .first()[1])

    def resolve_top_civilization(self, info):
        """Resolve civilization most played."""
        result = Match.get_query(info) \
            .join(schema.Player) \
            .with_entities(schema.Player.civilization_id, schema.Match.dataset_id) \
            .filter(schema.Player.user_id == str(self.id), schema.Match.platform_id == self.platform_id) \
            .group_by(schema.Player.civilization_id, schema.Match.dataset_id) \
            .order_by(func.count(schema.Match.id).desc()) \
            .first()
        return info.context['loaders'].civilization.load(result)

    def resolve_top_dataset(self, info):
        """Resolve dataset most played."""
        dataset_id = Match.get_query(info) \
            .join(schema.Player) \
            .with_entities(schema.Match.dataset_id) \
            .filter(schema.Player.user_id == str(self.id), schema.Match.platform_id == self.platform_id) \
            .group_by(schema.Match.dataset_id) \
            .order_by(func.count(schema.Match.id).desc()) \
            .first()[0]
        return Dataset.get_query(info).get(dataset_id)

    def resolve_aliases(self, info):
        """Resolve aliases."""
        aliases = get_aliases(info.context['session'], self.id, self.platform_id)
        if self.canonical_name:
            other_users = info.context['session'].query(model.CanonicalPlayer) \
                .filter(model.CanonicalPlayer.name == self.canonical_name)
            for user in other_users:
                aliases |= get_aliases(info.context['session'], user.user_id, user.platform_id)
            aliases.discard(self.canonical_name)
        aliases.discard(self.name)
        return list(aliases)

    def resolve_matches(self, info, offset, limit):
        """Resolve matches played on this map."""
        query = Match.get_query(info) \
            .join(schema.Player) \
            .filter(schema.Player.user_id == str(self.id), schema.Match.platform_id == self.platform_id)
        return MatchHits(query=query, offset=offset, limit=limit)

    def resolve_meta_ranks(self, info):
        """Resolve user's ladder ranks."""
        session = info.context['session']
        ranks = []
        for ladder_id in LADDERS[self.platform_id].keys():
            rank, rating = get_rank(session, self.id, None, self.platform_id, ladder_id)
            if not rank:
                continue
            ranks.append(MetaLadderRank(
                rank=rank,
                user_id=self.id,
                rating=rating,
                ladder_id=ladder_id,
                platform_id=self.platform_id
            ))
        return ranks


class MetaLadderRank(graphene.ObjectType):
    """Meta ladder rank."""
    rank = graphene.Int()
    user_id = graphene.String()
    user_name = graphene.String()
    rating = graphene.Int()
    user = graphene.Field('aocgql.schema.User')
    ladder_id = graphene.Int()
    change = graphene.Int()
    platform_id = graphene.String()
    ladder = graphene.Field(lambda: MetaLadder)
    platform = graphene.Field('aocgql.schema.Platform')
    rate_by_day = graphene.List(DateStat, ladder_id=graphene.Int())
    streak = graphene.Int()

    def resolve_user(self, info):
        """Resolve user at this rank."""
        return info.context['loaders'].user.load((self.user_id, self.platform_id))

    def resolve_ladder(self, _):
        """Resolve rank's ladder."""
        return MetaLadder(id=self.ladder_id, name=LADDERS[self.platform_id][self.ladder_id])

    def resolve_platform(self, info):
        """Resolve rank's platform."""
        return info.context['session'].query('Platform').get(self.platform_id)

    def resolve_streak(self, info):
        """Resolve current win/loss streak."""
        subq = info.context['session'].query(func.max(schema.Match.played).label('boundary')) \
            .join(schema.Player) \
            .filter(schema.Player.user_id == self.user_id) \
            .group_by(schema.Player.winner) \
            .order_by(func.max(schema.Match.played)) \
            .limit(1) \
            .subquery('outcome')
        streak = info.context['session'].query(case([
            (schema.Player.winner.is_(True), func.count(schema.Match.id)),
            (schema.Player.winner.is_(False), -1 * func.count(schema.Match.id))
        ])).join(schema.Match) \
            .filter(schema.Match.played > subq.c.boundary) \
            .filter(schema.Player.user_id == self.user_id) \
            .group_by(schema.Player.winner).first()
        if streak:
            return streak[0]
        return 0

    def resolve_rate_by_day(self, info):
        """Resolve rate per day."""
        session = info.context['session']
        result = rate_by_day(session, self.user_id, self.platform_id, self.ladder_id)
        return [DateStat(
            date=dateparser.parse(x.date).date() if isinstance(x.date, str) else x.date,
            count=x.rate
        ) for x in result]


class MetaLadder(graphene.ObjectType):
    """Meta ladder."""
    id = graphene.Int()
    platform_id = graphene.String()
    platform = graphene.Field('aocgql.schema.Platform')
    ranks = graphene.List(lambda: MetaLadderRank, limit=graphene.Int(default_value=5))
    name = graphene.String()

    def resolve_ranks(self, info, limit):
        """Resolve ladder ranks."""
        session = info.context['session']
        results = get_ranks(session, None, self.platform_id, self.id).limit(limit)
        return [MetaLadderRank(
            rank=i + 1,
            user_id=x[0],
            user_name=x[1],
            rating=x[2],
            ladder_id=self.id,
            platform_id=self.platform_id
        ) for i, x in enumerate(results)]

    def resolve_platform(self, info):
        """Resolve ladder's platform."""
        return info.context['session'].query(model.Platform).get(self.platform_id)
