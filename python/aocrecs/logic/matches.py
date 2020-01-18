"""Matches."""
import asyncio

from aocrecs.cache import cached, dataloader_cached
from aocrecs.util import by_key, compound_where


@cached(ttl=None)
async def get_chat(database, match_id):
    """Get match chat."""
    query = """
        select name, player_number, message, origination, audience, timestamp
        from chat join players on chat.player_number=players.number and chat.match_id=players.match_id
        where chat.match_id=:match_id
        order by timestamp
    """
    result = await database.fetch_all(query, values={'match_id': match_id})
    return [dict(c, player=dict(name=c['name'], number=c['player_number'], match_id=match_id)) for c in result]


@dataloader_cached(ttl=None)
async def get_research_by_player(keys, database):
    """Get researches."""
    where, values = compound_where(keys, ('match_id', 'player_number'))
    query = """
        select name, started, finished, player_number, match_id
        from research join technologies on research.technology_id=technologies.id and research.dataset_id=technologies.dataset_id
        where {}
        order by started
    """.format(where)
    results = await database.fetch_all(query, values=values)
    return by_key(results, ('match_id', 'player_number'))


def make_players(player_data, match_id):
    """Make player structures."""
    return [
        dict(
            player,
            user=dict(
                id=player['user_id'],
                name=player['name'],
                platform_id=player['platform_id']
            ) if player['user_id'] else None,
            civilization=dict(
                id=player['civilization_id'],
                name=player['civilization_name'],
                dataset_id=player['dataset_id']
            )
        ) for player in player_data[match_id]
    ]


def make_teams(player_data, match_id):
    """Make team structures."""
    team_data = [
        dict(
            team_id=team_id,
            winner=any([p['winner'] for p in team]),
            players=team,
            match_id=match_id
        ) for team_id, team in by_key(player_data, 'team_id').items()
    ]
    winning_team = next((t for t in team_data if t['winner']), None)
    return team_data, winning_team


def make_files(player_data, file_data, match_id, url_func):
    """Make files structures."""
    by_number = by_key(player_data, 'number')
    return [
        dict(
            file_,
            download_link=url_func('download', file_id=file_['id']),
            owner=by_number[file_['owner_number']][0]
        ) for file_ in file_data[match_id]
    ]


@dataloader_cached(ttl=None)
async def get_match(keys, context):
    """Get a match."""
    player_query = """
        select players.match_id, players.team_id, players.number, players.name, players.winner, teams.winner as t_winner,
            player_colors.name as color, players.color_id,
            civilizations.id as civilization_id, civilizations.name as civilization_name,
            players.dataset_id, players.platform_id, players.user_id, players.user_name,
            rate_snapshot, rate_before, rate_after, mvp, human, score, military_score,
            economy_score, technology_score, society_score, units_killed, buildings_razed,
            buildings_lost, units_converted, food_collected, wood_collected, stone_collected,
            gold_collected, tribute_sent, tribute_received, trade_gold, relic_gold,
            extract(epoch from feudal_time)::integer as feudal_time_secs, extract(epoch from castle_time)::integer as castle_time_secs,
            extract(epoch from imperial_time)::integer as imperial_time_secs, explored_percent, research_count,
            total_wonders, total_castles, total_relics, villager_high
        from players join teams on players.team_id=teams.team_id and players.match_id=teams.match_id
        join player_colors on players.color_id=player_colors.id
        join civilizations on players.dataset_id=civilizations.dataset_id and players.civilization_id=civilizations.id
        join datasets on players.dataset_id=datasets.id
        join platforms on players.platform_id=platforms.id
        where players.match_id=any(:match_id)
    """
    file_query = """
        select id, match_id, size, original_filename, language, encoding, owner_number
        from files where match_id=any(:match_id)
    """
    match_query = """
        select matches.id, map_name, rms_seed,
            matches.dataset_id, datasets.name as dataset_name,
            matches.platform_id, platforms.name as platform_name,
            platforms.url as platform_url, platforms.match_url as platform_match_url,
            matches.event_id, events.name as event_name,
            matches.tournament_id, tournaments.name as tournament_name,
            matches.series_id, series_metadata.name as series_name,
            matches.ladder_id, ladders.name as ladder_name,
            difficulties.name as difficulty,
            game_types.name as type, matches.type_id,
            map_reveal_choices.name as map_reveal_choice,
            map_sizes.name as map_size,
            speeds.name as speed,
            starting_ages.name as starting_age,
            starting_resources.name as starting_resources,
            victory_conditions.name as victory_condition,
            played, rated, diplomacy_type, team_size, platform_match_id,
            cheats, population_limit, lock_teams, mirror, dataset_version,
            versions.name as version, extract(epoch from duration)::integer as duration_secs, winning_team_id
        from matches
        join versions on matches.version_id=versions.id
        join datasets on matches.dataset_id=datasets.id
        join platforms on matches.platform_id=platforms.id
        join difficulties on matches.difficulty_id=difficulties.id
        join game_types on matches.type_id=game_types.id
        join map_reveal_choices on matches.map_reveal_choice_id=map_reveal_choices.id
        join map_sizes on matches.map_size_id=map_sizes.id
        join speeds on matches.speed_id=speeds.id
        left join starting_ages on matches.starting_age_id=starting_ages.id
        left join starting_resources on matches.starting_resources_id=starting_resources.id
        left join victory_conditions on matches.victory_condition_id=victory_conditions.id
        left join ladders on matches.ladder_id=ladders.id and matches.platform_id=ladders.platform_id
        left join events on matches.event_id=events.id
        left join tournaments on matches.tournament_id=tournaments.id
        left join series_metadata on matches.series_id=series_metadata.series_id
        where matches.id=any(:id)
    """
    matches, players, files = await asyncio.gather(
        context.database.fetch_all(match_query, values={'id': keys}),
        context.database.fetch_all(player_query, values={'match_id': keys}),
        context.database.fetch_all(file_query, values={'match_id': keys})
    )
    output = {}
    for match in matches:
        match_id = match['id']
        player_data = make_players(by_key(players, 'match_id'), match_id)
        team_data, winning_team = make_teams(player_data, match_id)
        output[match_id] = dict(
            match,
            players=player_data,
            teams=team_data,
            winning_team=winning_team,
            minimap_link=context.request.url_for('minimap', match_id=match_id),
            event=dict(
                id=match['event_id'],
                name=match['event_name']
            ) if match['event_id'] else None,
            tournament=dict(
                id=match['tournament_id'],
                name=match['tournament_name']
            ) if match['tournament_id'] else None,
            series=dict(
                id=match['series_id'],
                name=match['series_name']
            ) if match['series_id'] else None,
            files=make_files(player_data, by_key(files, 'match_id'), match_id, context.request.url_for),
            dataset=dict(
                id=match['dataset_id'],
                name=match['dataset_name']
            ),
            platform=dict(
                id=match['platform_id'],
                name=match['platform_name'],
                url=match['platform_url'],
                match_url=match['platform_match_url']
            ),
            ladder=dict(
                id=match['ladder_id'],
                name=match['ladder_name'],
                platform_id=match['platform_id']
            ) if match['ladder_id'] else None
        )
    return output
