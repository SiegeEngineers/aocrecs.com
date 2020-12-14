"""Maps."""
import asyncio

from aocrecs.cache import cached
from aocrecs.util import by_key


@cached(warm=True, ttl=3600)
async def get_maps(database):
    """Get all maps."""
    query = """
        select (case when maps.id > 0 then true else false end) as builtin, map_name as name, count(matches.id) as count
        from matches left join maps on matches.map_name=maps.name and matches.dataset_id=maps.dataset_id
        group by map_name, maps.id
        order by count(matches.id) desc
    """
    event_query = """
        select events.id, events.name as name, event_maps.name as map_name from event_maps join events on event_maps.event_id=events.id
    """
    total, results, events = await asyncio.gather(
        database.fetch_one('select count(*) as count from matches'),
        database.fetch_all(query),
        database.fetch_all(event_query)
    )
    event_data = by_key(events, 'map_name')
    return [
        dict(
            map_,
            percent=map_['count']/total['count'],
            events=event_data[map_['name']]
        ) for map_ in results
    ]


@cached(ttl=None)
async def get_preview_url(context, map_name):
    """Get map tiles url."""
    preview_query = """
        select id from matches where map_name=:name and map_tiles is not null limit 1
    """
    preview = await context.database.fetch_one(preview_query, values={'name': map_name})
    if preview:
        return f"/api/map/{preview['id']}"
    return None


@cached(ttl=None)
async def get_map_events(keys, context):
    """Get events on a map."""
    query = """
        select events.id, events.name, event_maps.name as map_name
            from event_maps join events on event_maps.event_id=events.id
        where event_maps.name=any(:names)
    """
    return by_key(await context.database.fetch_all(query, values={'names': keys}), 'map_name')


@cached(ttl=1440)
async def get_top_civilizations(database, map_name, limit):
    """Get civilizations with most wins on a given map."""
    query = """
        select civilization_id as id, civilizations.name, civilizations.dataset_id
        from players join civilizations on players.dataset_id=civilizations.dataset_id and players.civilization_id=civilizations.id
            join matches on players.match_id=matches.id
        where winner=true and map_name=:map_name
        group by civilization_id, civilizations.name, civilizations.dataset_id
        order by count(match_id) desc limit :limit
    """
    return list(map(dict, await database.fetch_all(query, values={'map_name': map_name, 'limit': limit})))
