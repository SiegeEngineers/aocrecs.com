"""Events."""
import asyncio

import networkx
from aocrecs.cache import cached
from aocrecs.util import by_key


def get_sides(matches, participants):
    """Get users per side given matches."""
    users = {}
    for match in matches:
        users.update({
            p['user_id']: dict(
                id=p['user_id'],
                name=p['user_name'] or p['name'],
                platform_id=p['platform_id']
            ) for p in match['players']
        })
    return [
        dict(p, users=[users[u] for u in p['user_ids'] if u])
        for p in compute_participants(matches, participants)
    ]


async def get_series(database, series_id):
    """Get a series."""
    series_query = """
        select series.id, series.played, series_metadata.name, rounds.tournament_id, tournaments.id as tournament_id,
        tournaments.name as tournament_name, events.id as event_id, events.name as event_name
        from series join rounds on series.round_id=rounds.id join series_metadata on series.id=series_metadata.series_id
        join tournaments on rounds.tournament_id=tournaments.id
        join events on tournaments.event_id=events.id
        where series.id=:id
    """
    participants_query = 'select series_id, name, score, winner from participants where series_id=:id'
    matches_query = 'select id, series_id from matches where series_id=:id'
    values = {'id': series_id}
    series, participants, matches = await asyncio.gather(
        database.fetch_one(series_query, values=values),
        database.fetch_all(participants_query, values=values),
        database.fetch_all(matches_query, values=values)
    )
    return dict(
        series,
        participants=list(map(dict, participants)),
        match_ids=list(map(lambda m: m['id'], matches)),
        tournament=dict(
            id=series['tournament_id'],
            name=series['tournament_name'],
            event=dict(
                id=series['event_id'],
                name=series['event_name']
            )
        )
    )


@cached(ttl=86400)
async def get_event(database, event_id):
    """Get an event."""
    events_query = 'select id, name, year from events where id=:event_id'
    tournaments_query = 'select id, event_id, name from tournaments where event_id=:event_id'
    series_query = """
        select
            series.id, series.played, series_metadata.name, rounds.tournament_id
        from series
            join rounds on series.round_id=rounds.id
            join tournaments on rounds.tournament_id=tournaments.id
            join series_metadata on series.id=series_metadata.series_id
        where tournaments.event_id=:event_id
        order by series.id
    """
    participants_query = """
        select series_id, participants.name, score, winner
        from participants
            join series on participants.series_id=series.id
            join rounds on series.round_id=rounds.id
            join tournaments on rounds.tournament_id=tournaments.id
        where tournaments.event_id=:event_id
    """
    maps_query = """
        select
            map_name, avg(matches.duration)::interval(0) as avg_duration, count(distinct match_id) as matches, max(players.dataset_id) as dataset_id,
            round(count(distinct match_id)/(select count(*) from matches where event_id=:event_id)::numeric, 2) as played_percent,
            mode() within group (order by civilizations.id) as most_played_civ_id,
            mode() within group (order by civilizations.name) as most_played_civ_name
        from players
        join civilizations on civilizations.dataset_id=players.dataset_id and civilizations.id = players.civilization_id
        join matches on players.match_id=matches.id
        where event_id=:event_id
        group by map_name
        order by count(distinct match_id) desc
    """
    players_query = """
        select
            max(players.name) as name, max(players.platform_id) as platform_id, max(user_id) as user_id,
            max(people.id) as person_id, max(people.name) as person_name, max(people.country) as country,
            count(*) as matches, round(sum(players.winner::int)/count(*)::numeric, 2) as win_percent,
            max(matches.dataset_id) as dataset_id,
            avg(matches.duration)::interval(0) as avg_duration,
            mode() within group (order by civilizations.id) as most_played_civ_id,
            mode() within group (order by civilizations.name) as most_played_civ_name,
            mode() within group (order by matches.map_name) as most_played_map
        from players
        join civilizations on civilizations.dataset_id=players.dataset_id and civilizations.id = players.civilization_id
        join matches on players.match_id=matches.id
        left join users on players.platform_id=users.platform_id and players.user_id=users.id
        left join people on users.person_id=people.id
        where event_id=:event_id
        group by case when people.id is not null then people.id::varchar else players.name end
        order by count(*) desc, sum(players.winner::int)/count(*)::numeric desc
    """
    civilizations_query = """
        select
            civilizations.id, civilizations.name, avg(matches.duration)::interval(0) as avg_duration,
            count(distinct match_id) as matches, max(players.dataset_id) as dataset_id,
            count(*) as matches, round(sum(players.winner::int)/count(*)::numeric, 2) as win_percent,
            mode() within group (order by matches.map_name) as most_played_map
        from players
        join civilizations on civilizations.dataset_id=players.dataset_id and civilizations.id = players.civilization_id
        join matches on players.match_id=matches.id
        where event_id=:event_id
        group by civilizations.id, civilizations.name
        order by count(distinct match_id) desc
;
    """
    event, tournaments, series, maps, civilizations, players, participants = await asyncio.gather(
        database.fetch_one(events_query, values={'event_id': event_id}),
        database.fetch_all(tournaments_query, values={'event_id': event_id}),
        database.fetch_all(series_query, values={'event_id': event_id}),
        database.fetch_all(maps_query, values={'event_id': event_id}),
        database.fetch_all(civilizations_query, values={'event_id': event_id}),
        database.fetch_all(players_query, values={'event_id': event_id}),
        database.fetch_all(participants_query, values={'event_id': event_id})
    )
    series_data = by_key(series, 'tournament_id')
    participant_data = by_key(participants, 'series_id')
    return dict(
        event,
        maps=[
            dict(
                map=dict(
                    name=m['map_name']
                ),
                average_duration=m['avg_duration'],
                match_count=m['matches'],
                played_percent=m['played_percent'],
                most_played_civilization=dict(
                    id=m['most_played_civ_id'],
                    name=m['most_played_civ_name'],
                    dataset_id=m['dataset_id']
                )
            ) for m in maps
        ],
        civilizations=[
            dict(
                civilization=dict(
                    id=c['id'],
                    name=c['name'],
                    dataset_id=c['dataset_id']
                ),
                average_duration=c['avg_duration'],
                match_count=c['matches'],
                win_percent=c['win_percent'],
                most_played_map=c['most_played_map']
            ) for c in civilizations
        ],
        players=[
            dict(
                player=dict(
                    name=player['name'],
                    user=dict(
                        id=player['user_id'],
                        name=player['name'],
                        platform_id=player['platform_id'],
                        person=dict(
                            id=player['person_id'],
                            country=player['country'],
                            name=player['person_name']
                        ) if player['person_id'] else None
                    ) if player['user_id'] else None
                ),
                match_count=player['matches'],
                win_percent=player['win_percent'],
                average_duration=player['avg_duration'],
                most_played_map=player['most_played_map'],
                most_played_civilization=dict(
                    id=player['most_played_civ_id'],
                    name=player['most_played_civ_name'],
                    dataset_id=player['dataset_id']
                )
            ) for player in players
        ],
        tournaments=[dict(
            tournament,
            series=[dict(
                series_,
                participants=participant_data[series_['id']],
            ) for series_ in series_data[tournament['id']]]
        ) for tournament in tournaments]
    )


@cached(warm=True, ttl=86400)
async def get_events(database):
    """Get events."""
    events_query = 'select id, name, year from events order by year, name'
    events = await database.fetch_all(events_query)
    return [dict(e) for e in events]


def compute_participants(matches, challonge_data):
    """Compute series participants.

    Iterate all matches and players to create a graph.
    Apply connected components algorithm to resolve distinct
    participant groups over all matches.

    Sort participant groups by number of wins to correlate
    with Challonge participant data (which also includes number
    of wins).

    Note that edge cases exist that are not covered. For example,
    teams sometimes field a 1v1 player for a single match. If neither
    player in the 1v1 match takes part in any other matches,
    the players can't be placed in a participant group and their win
    is not counted. There are two consequences:

    1. Not counting a win may make the number of wins between
       participants even, in which case we don't know which
       participant group won the series.
    2. Not grouping a player means the participant player list
       will be incomplete.
    """
    graph = networkx.DiGraph()
    win_id = 0
    platform_ids = []
    name_to_user = {}
    for match in matches:
        # Record a win
        win_id += 1
        graph.add_node(win_id, type='win')

        # Record platform ID
        platform_ids.append(match['platform_id'])

        # Add node for each player
        for player in match['players']:
            name_to_user[player['name']] = player['user_id']
            graph.add_node(player['name'], type='player')

        # Can happen for incomplete matches
        if match['winning_team'] is None:
            continue

        # Connect winning players to recorded win
        for player in match['winning_team']['players']:
            graph.add_edge(player['name'], win_id)

        # Connect all players on the same team
        for team in match['teams']:
            for i in team['players']:
                for j in team['players']:
                    graph.add_edge(i['name'], j['name'])

    mgz_data = [{
        'wins': len([node for node in g if graph.nodes[node]['type'] == 'win']),
        'players': [node for node in g if graph.nodes[node]['type'] == 'player']
    } for g in networkx.weakly_connected_components(graph)]

    return [{
        'user_ids': [name_to_user[n] for n in mgz['players']],
        'winner': challonge['winner'],
        'name': challonge['name'],
        'score': challonge['score'],
        'platform_id': platform_ids[0]
    } for mgz, challonge in zip(
        sorted(mgz_data, key=lambda k: -1 * k['wins']),
        sorted(challonge_data, key=lambda k: -1 * k['score'] if k['score'] else 0)
    )]
