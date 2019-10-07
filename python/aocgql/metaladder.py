"""Metaladder.

Generate a current ladder snapshot based on the
last observed rating of all players on a given
platform and ladder.
"""

from sqlalchemy import func, and_
from mgzdb import schema


def get_ranks(session, filters, platform_id, ladder_id):
    """Get all ladder ranks."""
    subq = session.query(
        schema.Player.user_id,
        func.max(schema.Match.played).label('maxdate')
    ).join(schema.Match)

    if filters is not None:
        print(filters)
        subq = subq.filter(filters)

    subq = subq.filter(schema.Match.platform_id == platform_id) \
        .filter(schema.Match.ladder_id == ladder_id) \
        .filter(schema.Player.rate_after is not None) \
        .group_by(schema.Player.user_id).subquery('t2')

    query = session.query(schema.Player.user_id, schema.Player.user_name, schema.Player.rate_after) \
        .join(schema.Match) \
        .join(
            subq,
            and_(
                schema.Player.user_id == subq.c.user_id,
                schema.Match.played == subq.c.maxdate
            )
        ) \
        .filter(schema.Match.platform_id == platform_id) \
        .filter(schema.Match.ladder_id == ladder_id) \
        .filter(schema.Player.rate_after is not None) \
        .order_by(schema.Player.rate_after.desc())
    return query


def get_rank(session, user_id, filters, platform_id, ladder_id):
    """Get user's rank and rating on a given ladder."""
    results = get_ranks(session, filters, platform_id, ladder_id).all()
    for i, player in enumerate(results):
        if player.user_id == user_id:
            return i + 1, player.rate_after
    return None, None
