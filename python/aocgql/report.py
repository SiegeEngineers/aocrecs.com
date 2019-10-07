"""Report functionality."""
import datetime

from sqlalchemy import func, desc, extract, case

from mgzdb import schema

from aocgql.const import COLLECTION_STARTED
from aocgql.metaladder import get_ranks
from aocgql.stats import wrap_percent


DEFAULT_LIMIT = 25


def diff(current, previous, key):
    """Diff two lists."""
    pmap = {}
    for i, item in enumerate(previous):
        if isinstance(item, dict):
            pmap[item[key]] = i
        else:
            pmap[getattr(item, key)] = i
    for i, item in enumerate(current):
        if isinstance(item, dict):
            value = item[key]
        else:
            value = getattr(item, key)
        yield {
            'rank': i + 1,
            'item': item,
            'change': pmap.get(value) - i if value in pmap else None
        }


def available_reports(session):
    """Get available reports."""
    valid_date = datetime.datetime.today()
    last_date = datetime.date(valid_date.year, valid_date.month, 1)
    return session.query(
        extract('year', schema.Match.played).label('y'),
        extract('month', schema.Match.played).label('m')
    ) \
        .filter(schema.Match.played >= COLLECTION_STARTED) \
        .filter(schema.Match.played < last_date) \
        .group_by('y', 'm') \
        .order_by(desc('y'), desc('m'))


def popular_maps(session, current, previous, limit=DEFAULT_LIMIT):
    """Get popular maps."""
    query = session.query(schema.Match.map_name, func.count(schema.Match.map_name)) \
        .group_by(schema.Match.map_name) \
        .order_by(desc(func.count(schema.Match.map_name))) \
        .filter(current)
    return diff(
        wrap_percent(query.filter(current))[:limit],
        wrap_percent(query.filter(previous)),
        'key'
    )


def longest_matches(session, filters, limit=DEFAULT_LIMIT):
    """Get longest matches."""
    return session.query(schema.Match) \
        .filter(filters) \
        .order_by(desc(schema.Match.duration)) \
        .limit(limit).all()


def most_matches(session, filters, platform_id, limit=DEFAULT_LIMIT):
    """Get players with the most matches."""
    return [{
        'user_id': row[0],
        'count': row[1]
    } for row in session.query(schema.Player.user_id, func.count(schema.Match.id)) \
        .join(schema.Match) \
        .filter(schema.Player.user_id != '') \
        .filter(schema.Match.platform_id == platform_id) \
        .filter(filters) \
        .group_by(schema.Player.user_id) \
        .order_by(desc(func.count(schema.Match.id))) \
        .limit(limit)]


def most_improvement(session, filters, platform_id, ladder_id, limit=DEFAULT_LIMIT):
    """Get players with most improvement."""
    return session.query(
        func.max(schema.Player.user_id),
        func.min(schema.Player.rate_snapshot),
        func.max(schema.Player.rate_snapshot),
        func.max(schema.Player.rate_snapshot) - func.min(schema.Player.rate_snapshot),
        func.count(schema.Match.id),
        func.count(case([(schema.Player.winner.is_(True), 1)])),
        func.count(case([(schema.Player.winner.is_(False), 1)]))
    ).join(schema.Match) \
        .filter(filters) \
        .filter(schema.Player.user_id != '') \
        .filter(schema.Player.rate_snapshot > 0) \
        .filter(schema.Match.ladder_id == ladder_id) \
        .filter(schema.Match.platform_id == platform_id) \
        .group_by(schema.Player.user_id) \
        .having(
            func.count(
                case([(schema.Player.winner.is_(True), 1)])
            ) > func.count(
                case([(schema.Player.winner.is_(False), 1)]))
        ) \
        .order_by(
            desc(func.max(schema.Player.rate_snapshot) - func.min(schema.Player.rate_snapshot))
        ) \
        .limit(limit).all()


def rankings(session, filters, prev_filters, platform_id, ladder_id, limit=DEFAULT_LIMIT): # pylint: disable=too-many-arguments
    """Get rankings for a ladder."""
    return diff(
        get_ranks(session, filters, platform_id, ladder_id).limit(limit),
        get_ranks(session, prev_filters, platform_id, ladder_id),
        'user_id'
    )
