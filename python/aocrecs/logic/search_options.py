"""Search options."""
import asyncio
from aocrecs.cache import cached


def bool_option():
    """Shortcut for boolean options."""
    return [{'value': True, 'label': 'Yes'}, {'value': False, 'label': 'No'}]


def diplo_options():
    """Diplomacy options.

    TODO: make this a table in mgzdb
    """
    return [
        {'value': '1v1', 'label': '1v1'},
        {'value': 'TG', 'label': 'TG'},
        {'value': 'FFA', 'label': 'FFA'},
        {'value': 'Other', 'label': 'Other'}
    ]


@cached(warm=True, ttl=None)
async def civilizations(database, dataset_id):
    """Get civilizations for a dataset."""
    query = "select id as value, name as label from civilizations where dataset_id=:dataset_id"
    return list(map(dict, await database.fetch_all(query, values={'dataset_id': dataset_id})))


@cached(warm=True, ttl=None)
async def ladders(database, platform_id):
    """Get ladders for a platform."""
    query = "select id as value, name as label from ladders where platform_id=:platform_id"
    return list(map(dict, await database.fetch_all(query, values={'platform_id': platform_id})))


@cached(warm=True, ttl=None)
async def general(database):
    """Get general search options."""
    colors, game_types, datasets, platforms, events, tournaments = await asyncio.gather(
        database.fetch_all("select id as value, name as label from player_colors"),
        database.fetch_all("select id as value, name as label from game_types"),
        database.fetch_all("select id as value, name as label from datasets"),
        database.fetch_all("select id as value, name as label from platforms"),
        database.fetch_all("select id as value, name as label from events"),
        database.fetch_all("select id as value, name as label from tournaments")
    )
    return {
        'rms_zr': bool_option(),
        'mirror': bool_option(),
        'rated': bool_option(),
        'mvp': bool_option(),
        'winner': bool_option(),
        'playback': bool_option(),
        'colors': list(map(dict, colors)),
        'diplomacy_types': diplo_options(),
        'game_types': list(map(dict, game_types)),
        'datasets': list(map(dict, datasets)),
        'platforms': list(map(dict, platforms)),
        'events': list(map(dict, events)),
        'tournaments': list(map(dict, tournaments))
    }
