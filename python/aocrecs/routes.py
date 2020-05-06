"""Routes."""
import asyncio
import requests
from starlette.responses import Response, PlainTextResponse
from mgz.util import Version
from mgzdb.compress import decompress_tiles
from aocrecs.download import get_zip
from aocrecs.logic.minimap import generate_svg

async def nightbot(request):
    """Nightbot match prototype."""
    steam_id = request.path_params['steam_id']
    data = requests.get('https://aoe2.net/api/player/lastmatch?game=aoe2de&steam_id={}'.format(steam_id)).json()
    profile_ids = [str(player['profile_id']) for player in data['last_match']['players']]
    civ_ids = [player['civ'] for player in data['last_match']['players']]
    person_query = "select name, users.id from people join users on people.id=users.person_id where users.platform_id='de' and users.id=any(:profile_ids)"
    map_query = "select name from maps where dataset_id=100 and id=:map_id"
    civ_query = "select name, id from civilizations where dataset_id=100 and id=any(:civ_ids)"
    players, map_, civs = await asyncio.gather(
        request.app.state.database.fetch_all(person_query, values=dict(profile_ids=profile_ids)),
        request.app.state.database.fetch_one(map_query, values=dict(map_id=data['last_match']['map_type'])),
        request.app.state.database.fetch_all(civ_query, values=dict(civ_ids=civ_ids))
    )
    def player_string(player, names, civs):
        return '{} ({}) as {}'.format(names.get(player['profile_id'], player['name']), player['rating'], civs.get(player['civ']))
    names = {int(player['id']): player['name'] for player in players}
    civs = {civ['id']: civ['name'] for civ in civs}
    vs = ' -VS- '.join([player_string(player, names, civs) for player in data['last_match']['players']])
    return PlainTextResponse('{} on {}'.format(vs, map_['name']))


async def download(request):
    """Download recorded game files."""
    file_id = request.path_params['file_id']
    query = """
        select files.hash, original_filename, version_id
        from files join matches on files.match_id=matches.id
        where files.id=:id
    """
    result = await request.app.state.database.fetch_one(query, values={'id': file_id})
    return Response(get_zip(result['hash'], result['original_filename'], Version(result['version_id'])), media_type='application/zip')


async def portrait(request):
    """Return player portrait."""
    person_id = request.path_params['person_id']
    query = """
        select portrait from people where id=:id
    """
    result = await request.app.state.database.fetch_one(query, values={'id': person_id})
    return Response(result['portrait'], media_type='image/jpeg')


async def svg_map(request):
    """Get map tile SVGs."""
    match_id = request.path_params['match_id']
    match_query = """
        select dataset_id, map_size_id, map_tiles from matches where id=:match_id
    """
    tile_query = """
        select id, color_level, color_up, color_down
        from terrain
        where dataset_id=:dataset_id and id = any(:terrain_ids)
    """
    object_query = """
        select initial_object_id, initial_player_number, initial_class_id, created_x, created_y
        from object_instances
        where match_id=:match_id and created = '00:00:00'
    """
    player_color_query = """
        select number, hex
        from players join player_colors on players.color_id=player_colors.id
        where players.match_id=:match_id
    """
    match = await request.app.state.database.fetch_one(match_query, values={'match_id': match_id})
    if not match['map_tiles']:
        return Response()
    tiles = decompress_tiles(match['map_tiles'], match['map_size_id'])
    terrain, objects, player_colors = await asyncio.gather(
        request.app.state.database.fetch_all(tile_query, values={
            'dataset_id': match['dataset_id'],
            'terrain_ids': {t['terrain_id'] for t in tiles}
        }),
        request.app.state.database.fetch_all(object_query, values={
            'match_id': match_id
        }),
        request.app.state.database.fetch_all(player_color_query, values={
            'match_id': match_id
        })
    )
    svg = generate_svg(
        tiles,
        match['map_size_id'],
        {t['id']: {'level': t['color_level'], 'up': t['color_up'], 'down': t['color_down']} for t in terrain},
        objects,
        {p['number']: p['hex'] for p in player_colors}
    )
    return Response(svg, media_type='image/svg+xml')
