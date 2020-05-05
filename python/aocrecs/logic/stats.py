"""Global statistics."""
import asyncio
import datetime

from aocrecs.consts import COLLECTION_STARTED
from aocrecs.cache import cached


@cached(warm=True, ttl=2)
async def live_match_count(database):
    return await database.fetch_one('select count(*) as count from matches')


@cached(warm=True, ttl=3600)
async def summary(database):
    """Get summary statistics."""
    match_count, series_count, player_count = await asyncio.gather(
        live_match_count(database),
        database.fetch_one('select count(*) as count from series'),
        database.fetch_one('select count(*) as count from users'),
    )
    return {
        'match_count': int(match_count['count']),
        'series_count': series_count['count'],
        'player_count': player_count['count']
    }


@cached(warm=True, ttl=3600)
async def map_count(database):
    """Get map count."""
    query = "select count(*) as count from (select map_name from matches group by map_name) as x"
    result = await database.fetch_one(query)
    return result['count']


@cached(warm=[['game_types', 'type_id'], ['datasets', 'dataset_id'], ['platforms', 'platform_id']], ttl=86400)
async def rel_agg_query(database, table, foreign_key):
    """Aggregate across related table."""
    query = """
        select {table}.name, {table}.id, count(matches.{foreign_key}) as count
        from {table} join matches on {table}.id=matches.{foreign_key}
        group by {table}.name, {table}.id
        order by count(matches.{foreign_key}) desc
    """.format(table=table, foreign_key=foreign_key)
    return [dict(r) for r in await database.fetch_all(query)]


@cached(warm=[['files', 'language'], ['matches', 'diplomacy_type']], ttl=86400)
async def agg_query(database, table, field):
    """Aggregate on table."""
    query = """
        select {field} as name, count({field}) as count from {table} group by {field} order by count({field}) desc
    """.format(table=table, field=field)
    return [dict(r) for r in await database.fetch_all(query)]


@cached(warm=True, ttl=86400)
async def by_day(database):
    """Get daily match counts."""
    query = """
        select played::date as date, count(*) as count
        from matches
        where played > :start and played < :end
        group by played::date
        order by played::date
    """
    return [dict(r) for r in await database.fetch_all(query, values={
        'start': COLLECTION_STARTED,
        'end': datetime.datetime.now().date()
    })]
