"""Compute odds for various scenarios."""
import logging
import time

from collections import defaultdict
from sqlalchemy import func, and_, or_, distinct
from sqlalchemy.orm import joinedload, load_only
from mgzdb import schema


LOGGER = logging.getLogger(__name__)


def odds(session, params):
    """Get odds based on parameters."""
    LOGGER.info("generating odds for %s", params)
    start_time = time.time()

    teams = {i: team for i, team in enumerate(params['teams'])}

    num_unique_civs = len({
        p['civilization_id'] for t in teams.values() for p in t if 'civilization_id' in p
    })

    result = {}
    map_filter = schema.Match.map_name == params['map']
    if 'teams' in params:
        result['teams'] = odds_query(session, teams, params['type_id'], user_filter=True)
        if 'map' in params:
            result['teams_and_map'] = odds_query(
                session, teams, params['type_id'], match_filters=map_filter, user_filter=True
            )

        if num_unique_civs > 1:
            result['teams_and_civilizations'] = odds_query(
                session, teams, params['type_id'], civ_filter=True, user_filter=True
            )
            result['civilizations'] = odds_query(
                session, teams, params['type_id'], civ_filter=True
            )

        if 'map' in params and num_unique_civs > 1:
            result['civilizations_and_map'] = odds_query(
                session, teams, params['type_id'], match_filters=map_filter, civ_filter=True
            )

    LOGGER.info("computed all odds in %f", time.time() - start_time)
    return result


def odds_query(session, teams, type_id, match_filters=None, civ_filter=False, user_filter=False): # pylint: disable=too-many-arguments
    """Run a query with odds constraints."""
    start_time = time.time()
    team_size = 'v'.join(str(len(t)) for t in teams.values())
    match_query = session.query(schema.Match) \
        .filter(schema.Match.team_size == team_size) \
        .filter(schema.Match.type_id == type_id)

    if match_filters is not None:
        match_query = match_query.filter(match_filters)

    for team in teams.values():
        if civ_filter:
            key = 'civilization_id'
            player_filters = schema.Player.civilization_id.in_([p['civilization_id'] for p in team])

        if user_filter:
            key = 'user_id'
            player_filters = schema.Player.user_id.in_([p['user_id'] for p in team])

        if user_filter and civ_filter:
            key = 'civilization_id'
            player_filters = or_(*[
                and_(
                    schema.Player.user_id == p['user_id'],
                    schema.Player.civilization_id == p['civilization_id']
                )
                for p in team])

        num_unique = len({p[key] for p in team})
        team_query = session.query(schema.Player.match_id) \
            .group_by(schema.Player.match_id, schema.Player.team_id) \
            .filter(player_filters) \
            .having(func.count(distinct(getattr(schema.Player, key))) == num_unique).subquery()
        match_query = match_query.join(team_query, and_(schema.Match.id == team_query.c.match_id))

    result = compute_odds(
        match_query.options(
            load_only('id'),
            joinedload(schema.Match.players, innerjoin=True).load_only(key, 'winner')
        ),
        key, teams)
    LOGGER.info("computed odds in %f", time.time() - start_time)
    return result


def compute_odds(match_query, key, teams):
    """Compute odds with query results."""
    total = 0
    wins = defaultdict(int)
    for match in match_query.all():
        total += 1
        winners = {getattr(p, key) for p in match.players if p.winner}
        for i, team in teams.items():
            if winners == {p[key] for p in team}:
                wins[i] += 1

    if total <= 1:
        return None

    return [{
        'wins': wins[i],
        'losses': total - wins[i],
        'percent': wins[i] / total if total else None
    } for i in teams.keys()]
