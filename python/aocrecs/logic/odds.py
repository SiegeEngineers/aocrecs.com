"""Compute odds for various scenarios."""
import asyncio
import logging
import time

from collections import defaultdict

from aocrecs.cache import cached
from aocrecs.util import by_key, compound_where


LOGGER = logging.getLogger(__name__)


async def get_odds(database, params):
    """Get odds based on parameters."""
    LOGGER.info("generating odds")
    start_time = time.time()

    players = [dict(
        civilization_id=data['civilization_id'],
        user_id=data['user_id'],
        winner=data['winner'],
        team_id=data['team_id']
    ) for data in params['players']]
    teams = by_key(players, 'team_id')
    num_unique_civs = len({p['civilization_id'] for p in players if 'civilization_id' in p})

    keys = []
    queries = []
    map_filter = ("matches.map_name=:map_name", {'map_name': params['map_name']})
    if 'teams' in params:
        keys.append('teams')
        queries.append(odds_query(database, teams, params['type_id'], user_filter=True))
        if 'map_name' in params:
            keys.append('teams_and_map')
            queries.append(odds_query(database, teams, params['type_id'], match_filters=map_filter, user_filter=True))

        if num_unique_civs > 1:
            keys.append('teams_and_civilizations')
            queries.append(odds_query(database, teams, params['type_id'], civ_filter=True, user_filter=True))
            keys.append('civilizations')
            queries.append(odds_query(database, teams, params['type_id'], civ_filter=True))

        if 'map_name' in params and num_unique_civs > 1:
            keys.append('civilizations_and_map')
            queries.append(odds_query(database, teams, params['type_id'], match_filters=map_filter, civ_filter=True))

    results = await asyncio.gather(*queries)
    LOGGER.debug("computed all odds in %f", time.time() - start_time)
    return dict(zip(keys, results))


@cached(ttl=1440)
async def odds_query(database, teams, type_id, match_filters=None, civ_filter=False, user_filter=False): # pylint: disable=too-many-arguments, too-many-locals
    """Run a query with odds constraints."""
    start_time = time.time()
    team_size = 'v'.join(str(len(t)) for t in teams.values())
    values = {'team_size': team_size, 'type_id': type_id}

    match_query = """
        select matches.id, players.winner, players.{}
            from matches join players on matches.id=players.match_id
    """
    for i, team in teams.items():
        if user_filter and civ_filter:
            key = 'civilization_id'
            keys = [(p['user_id'], p['civilization_id']) for p in team]
            player_filters, player_values = compound_where(keys, ('players.user_id', 'players.civilization_id'))
            values.update(player_values)

        elif civ_filter:
            key = 'civilization_id'
            player_filters = " players.civilization_id=any(:civilization_ids_{})".format(i)
            values.update({'civilization_ids_{}'.format(i): [p['civilization_id'] for p in team]})

        elif user_filter:
            key = 'user_id'
            player_filters = " players.user_id=any(:user_ids_{})".format(i)
            values.update({'user_ids_{}'.format(i): [p['user_id'] for p in team]})

        team_query = """
            select match_id from players
            where {}
            group by match_id, team_id
            having count(distinct players.{}) = {}
        """.format(player_filters, key, len({p[key] for p in team}))
        match_query += " join ({0}) as t{1} on matches.id=t{1}.match_id".format(team_query, i)

    match_query += " where matches.team_size=:team_size and matches.type_id=:type_id"
    match_query = match_query.format(key)

    if match_filters is not None:
        match_query += ' and ' + match_filters[0]
        values.update(match_filters[1])

    result = await database.fetch_all(match_query, values=values)
    result = compute_odds(by_key(result, 'id').values(), key, teams)
    LOGGER.debug("computed odds in %f", time.time() - start_time)
    return result


def compute_odds(results, key, teams):
    """Compute odds with query results."""
    total = 0
    wins = defaultdict(int)
    for match in results:
        total += 1
        winners = {p[key] for p in match if p['winner']}
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
