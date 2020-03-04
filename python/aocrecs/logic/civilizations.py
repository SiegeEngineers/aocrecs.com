"""Civilizations."""
import asyncio
from aocrecs.cache import cached


@cached(ttl=None)
async def get_civilization(database, civilization_id, dataset_id):
    """Get a civilization."""
    query = """
        select civilizations.id, civilizations.dataset_id, civilizations.name
        from civilizations
        where id=:id and dataset_id=:dataset_id
    """
    bonuses = """
        select type, description
        from civilization_bonuses
        where civilization_id=:id and dataset_id=:dataset_id
    """
    values = {'id': civilization_id, 'dataset_id': dataset_id}
    result, bonuses = await asyncio.gather(
        database.fetch_one(query, values=values),
        database.fetch_all(bonuses, values=values)
    )
    return dict(result, bonuses=list(map(dict, bonuses)))


@cached(warm=[[0], [1], [100]], ttl=3600)
async def get_all_civilizations(database, dataset_id):
    """Get all civilizations."""
    query = """
        select civilizations.id, civilizations.dataset_id, civilizations.name, s.count
        from (
            select civilization_id, count(civilization_id) as count
            from players where dataset_id=:dataset_id
            group by civilization_id
        ) as s join civilizations on s.civilization_id = civilizations.id and civilizations.dataset_id=:dataset_id
        order by s.count desc
    """
    values = {'dataset_id': dataset_id}
    total, results = await asyncio.gather(
        database.fetch_one('select count(*) as count from players where dataset_id=:dataset_id', values=values),
        database.fetch_all(query, values=values)
    )
    return [dict(s, percent=s['count']/total['count']) for s in results]
