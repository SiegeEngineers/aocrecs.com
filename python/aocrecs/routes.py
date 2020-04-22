"""Routes."""
import asyncio
from starlette.responses import Response
from mgz.util import Version
from mgzdb.compress import decompress_tiles
from aocrecs.download import get_zip
from aocrecs.logic.minimap import generate_svg


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
