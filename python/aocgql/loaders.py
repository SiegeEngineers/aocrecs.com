"""Data loaders."""
from collections import defaultdict

from promise import Promise
from promise.dataloader import DataLoader
from sqlalchemy import and_, or_, func
from sqlalchemy.orm import joinedload
from sqlalchemy.inspection import inspect

from aocref import model
from mgzdb import schema
from aocgql.schema.user import User


# pylint: disable=method-hidden


class SessionLoader(DataLoader):
    """Dataloader with session."""

    def __init__(self, session):
        """Initialize."""
        super(SessionLoader, self).__init__()
        self.session = session


class TournamentLoader(SessionLoader):
    """Tournamment loader."""

    def batch_load_fn(self, keys):
        """Batch load tournaments."""
        results = self.session.query(model.Tournament) \
            .options(joinedload(model.Tournament.rounds) \
                .joinedload(model.Round.series) \
                .joinedload(model.Series.participants)) \
            .options(joinedload(model.Tournament.rounds) \
                .joinedload(model.Round.series) \
                .joinedload(model.Series.metadata)) \
            .filter(model.Tournament.id.in_(keys))
        by_key = {item.id: item for item in results.all()}
        return Promise.resolve([by_key[ref] if ref in by_key else None for ref in keys])


class EventMapLoader(SessionLoader):
    """Event map loader."""

    def batch_load_fn(self, keys):
        """Batch load event maps."""
        results = self.session.query(model.EventMap) \
            .options(joinedload(model.EventMap.event)) \
            .filter(model.EventMap.name.in_(keys))
        by_key = defaultdict(list)
        for item in results.all():
            by_key[item.name].append(item)
        return Promise.resolve([by_key[ref] for ref in keys])


class UserLoader(SessionLoader):
    """User loader."""

    def batch_load_fn(self, keys):
        """Batch load users."""
        ors = []
        for key in keys:
            ors.append(and_(schema.Player.user_id == key[0], schema.Player.platform_id == key[1]))

        subq = self.session.query(
            schema.Player.user_id, schema.Player.platform_id,
            func.max(schema.Player.match_id).label('match_id')
        ) \
            .filter(or_(*ors)) \
            .filter(schema.Player.human.is_(True)) \
            .group_by(schema.Player.user_id, schema.Player.platform_id) \
            .subquery()

        names = self.session.query(
            schema.Player.user_id, schema.Player.platform_id, schema.Player.name,
            schema.Player.user_name, model.CanonicalPlayer.name
        ) \
            .outerjoin(model.CanonicalPlayer, and_(
                schema.Player.user_id == model.CanonicalPlayer.user_id,
                schema.Player.platform_id == model.CanonicalPlayer.platform_id
            )) \
            .filter(
                schema.Player.match_id == subq.c.match_id,
                schema.Player.user_id == subq.c.user_id,
                schema.Player.platform_id == subq.c.platform_id
            ).all()

        results = {}
        for row in names:
            results[(row[0], row[1])] = {
                'name': row[3] or row[2],
                'canonical_name': row[4]
            }

        return Promise.resolve([User(
            id=key[0],
            platform_id=key[1],
            **results[key]
        ) for key in keys])


class BuiltinMapLoader(SessionLoader):
    """Builtin map loader."""

    def batch_load_fn(self, keys):
        """Batch load builtin map boolean."""
        results = self.session.query(model.Map).filter(model.Map.name.in_(keys))
        by_key = {item.name: item for item in results.all()}
        return Promise.resolve([ref in by_key for ref in keys])


class KeyLoader(DataLoader):
    """Generic primary key loader."""

    def __init__(self, session, table):
        """Initialize."""
        super(KeyLoader, self).__init__()
        self.session = session
        self.table = table
        key = inspect(table).primary_key
        self.key = [col.name for col in key]

    def batch_load_fn(self, keys):
        """Batch load keys."""
        ors = []
        for key in keys:
            ands = []
            for pair in list(zip(self.key, key)):
                ands.append(getattr(self.table, pair[0]) == pair[1])
            ors.append(and_(*ands))
        results = self.session.query(self.table).filter(or_(*ors))
        by_key = {inspect(item).identity: item for item in results.all()}
        return Promise.resolve([by_key[ref] if ref in by_key else None for ref in keys])


class Loader(): # pylint: disable=too-few-public-methods
    """Loader wrapper."""

    def __init__(self, session):
        """Initialize."""
        self.civilization = KeyLoader(session, model.Civilization)
        self.event_map = EventMapLoader(session)
        self.builtin_map = BuiltinMapLoader(session)
        self.tournament = TournamentLoader(session)
        self.user = UserLoader(session)
