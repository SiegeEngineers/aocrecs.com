"""Routes."""
from starlette.responses import Response
from mgzdb.compress import decompress_tiles
from aocrecs.download import get_zip
from aocrecs.logic.minimap import generate_svg


async def download(request):
    """Download recorded game files."""
    file_id = request.path_params['file_id']
    query = """
        select hash, original_filename from files where id=:id
    """
    result = await request.app.state.database.fetch_one(query, values={'id': file_id})
    return Response(get_zip(result['hash'], result['original_filename']), media_type='application/zip')


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
    match = await request.app.state.database.fetch_one(match_query, values={'match_id': match_id})
    if not match['map_tiles']:
        return Response()
    tiles = decompress_tiles(match['map_tiles'], match['map_size_id'])
    terrain = await request.app.state.database.fetch_all(tile_query, values={
        'dataset_id': match['dataset_id'],
        'terrain_ids': {t['terrain_id'] for t in tiles}
    })
    svg = generate_svg(
        tiles,
        match['map_size_id'],
        {t['id']: {'level': t['color_level'], 'up': t['color_up'], 'down': t['color_down']} for t in terrain}
    )
    return Response(svg, media_type='image/svg+xml')
