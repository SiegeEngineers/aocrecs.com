"""Compute various statistics."""

import datetime
from sqlalchemy import func, desc

from aocref import model
from mgzdb import schema

from aocgql.const import COLLECTION_STARTED

def wrap_percent(result):
    """Compute percent from raw counts."""
    out = []
    result = dict(result)
    total = sum(result.values())
    for key in sorted(result, key=result.get, reverse=True):
        num = result[key]
        out.append({'key': key, 'num': num, 'percent': num/total})
    return out


def group_by(session, field):
    """Group by a field."""
    return session.query(field, field, func.count(field)) \
        .group_by(field).order_by(desc(func.count(field)))


def group_by_relation(session, field, relation, relation_field):
    """Group by a relation field."""
    return session.query(func.max(field), relation_field, func.count(relation_field)) \
        .join(relation) \
        .group_by(relation_field) \
        .order_by(desc(func.count(relation_field)))


def civs_per_dataset(session, dataset_id):
    """Civilization usage per dataset."""
    return wrap_percent(
        session.query(model.Civilization.id, func.count(schema.Player.civilization_id)) \
            .join(schema.Player) \
            .filter(model.Civilization.dataset_id == dataset_id) \
            .group_by(model.Civilization.id, schema.Player.civilization_id).all()
        )


def civs_per_map(session, map_name):
    """Civilization usage per map (1v1 only)."""
    return wrap_percent(
        session.query(model.Civilization.id, func.count(schema.Player.civilization_id).label('count')) \
            .join(schema.Player).join(schema.Match) \
            .filter(schema.Match.map_name == map_name) \
            .filter(schema.Match.diplomacy_type == '1v1') \
            .group_by(model.Civilization.id, schema.Player.civilization_id) \
            .order_by(desc(func.count(schema.Player.civilization_id))).all()
    )


def maps(session):
    """Map usage."""
    return wrap_percent(session.query(schema.Match.map_name, func.count(schema.Match.map_name)) \
        .group_by(schema.Match.map_name).all())


def matches_by_day(session):
    """Matches played per day."""
    return session.query(func.date(schema.Match.played).label('date'), func.count(schema.Match.id).label('matches')) \
        .filter(schema.Match.played is not None) \
        .filter(schema.Match.played >= COLLECTION_STARTED) \
        .filter(schema.Match.played < datetime.date.today()) \
        .group_by('date') \
        .order_by('date')


def rate_by_day(session, user_id, platform_id, ladder_id):
    """Rating per day."""
    return session.query(
        func.date(schema.Match.played).label('date'),
        func.max(schema.Player.rate_after).label('rate')
        ) \
        .join(schema.Player) \
        .filter(schema.Player.user_id == user_id) \
        .filter(schema.Match.platform_id == platform_id) \
        .filter(schema.Match.ladder_id == ladder_id) \
        .filter(schema.Match.played is not None) \
        .filter(schema.Match.played >= COLLECTION_STARTED) \
        .filter(schema.Match.played < datetime.date.today()) \
        .group_by('date') \
        .order_by('date')
