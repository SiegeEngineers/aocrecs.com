"""Montly reports."""
import asyncio
import datetime
from dateutil.relativedelta import relativedelta
from aocrecs.consts import COLLECTION_STARTED
from aocrecs.logic.metaladder import compute_ranks
from aocrecs.cache import cached


LAST_MONTH = datetime.datetime.today() - relativedelta(months=+1)


def compute_map_data(result):
    """Compute rank and percent from map counts."""
    total = sum([r['count'] for r in result])
    return [
        dict(
            count=r['count'],
            map=dict(name=r['name']),
            rank=i + 1,
            percent=r['count']/total
        ) for i, r in enumerate(result)
    ]


def diff(current, previous, key):
    """Diff two lists."""
    pmap = {}
    for i, item in enumerate(previous):
        pmap[item[key]] = i
    for i, item in enumerate(current):
        value = item[key]
        yield dict(
            item,
            change=pmap.get(value) - i if value in pmap else None
        )


def available_reports():
    """Get available reports."""
    valid_date = datetime.datetime.today()
    last_date = datetime.date(valid_date.year, valid_date.month, 1)
    results = []
    i = COLLECTION_STARTED
    while i != last_date:
        results.append(i)
        i = i + relativedelta(months=+1)
    return [dict(year=d.year, month=d.month) for d in reversed(results)]


async def rankings(database, platform_id, ladder_id, year, month, limit): # pylint: disable=too-many-arguments
    """Get rankings for report interval."""
    prev = datetime.date(year, month, 1) - relativedelta(months=1)
    filters = "extract(year from matches.played)=:year and extract(month from matches.played)=:month"
    current, previous = await asyncio.gather(
        compute_ranks(database, (filters, {'year': year, 'month': month}), platform_id, ladder_id),
        compute_ranks(database, (filters, {'year': prev.year, 'month': prev.month}), platform_id, ladder_id)
    )
    return [
        dict(
            rank=i+1,
            rating=r['rating'],
            change=r['change'],
            user=dict(
                id=r['user_id'],
                name=r['user_name'] if r['user_name'] else r['name'],
                platform_id=platform_id,
                person=dict(id=r['person_id'], name=r['person_name'], country=r['country']) if r['person_id'] else None
            )
        )
        for i, r in enumerate(diff(current[:limit], previous, 'user_id'))
    ]


@cached(warm=[
    ['voobly', 131, LAST_MONTH.year, LAST_MONTH.month, 25],
    ['voobly', 132, LAST_MONTH.year, LAST_MONTH.month, 25]
], ttl=None)
async def most_improvement(database, platform_id, ladder_id, year, month, limit): # pylint: disable=too-many-arguments
    """Get most improvement for report interval."""
    query = """
    select max(players.user_id) as user_id, max(players.user_name) as user_name, max(players.name) as name, min(players.rate_snapshot) as min_rate,
        max(players.rate_snapshot) as max_rate, max(players.rate_snapshot) - min(players.rate_snapshot) as diff_rate,
        count(matches.id) as count,
        sum(case when players.winner is true then 1 else 0 end) as wins,
        sum(case when players.winner is true then 0 else 1 end) as losses
        from matches join players on matches.id=players.match_id
        where extract(year from matches.played)=:year and extract(month from matches.played)=:month
            and players.user_id != '' and players.rate_snapshot > 0
            and matches.ladder_id=:ladder_id and matches.platform_id=:platform_id
        group by players.user_id
        having sum(case when players.winner is true then 1 else 0 end) > sum(case when players.winner is true then 0 else 1 end)
        order by max(players.rate_snapshot) - min(players.rate_snapshot) desc
        limit :limit
    """
    values = {'limit': limit, 'year': year, 'month': month, 'platform_id': platform_id, 'ladder_id': ladder_id}
    results = await database.fetch_all(query, values=values)
    return [
        dict(
            r,
            rank=i + 1,
            user=dict(id=r['user_id'], platform_id=platform_id, name=r['user_name'] if r['user_name'] else r['name'])
        ) for i, r in enumerate(results)
    ]


@cached(warm=[[LAST_MONTH.year, LAST_MONTH.month, 25]], ttl=None)
async def report(database, year, month, limit):
    """Get a report."""
    matches_query = """
        select count(*) as count
        from matches
        where extract(year from played)=:year and extract(month from played)=:month
    """
    players_query = """
        select count(distinct players.user_id) as count
        from matches join players on matches.id=players.match_id
        where extract(year from played)=:year and extract(month from played)=:month
    """
    most_matches_query = """
        select players.user_id, players.platform_id, players.user_name, count(matches.id) as count
        from players join matches on players.match_id=matches.id
        where players.user_id != '' and
            extract(year from matches.played)=:year and extract(month from matches.played)=:month
        group by players.user_id, players.platform_id, players.user_name
        order by count(matches.id) desc
        limit :limit
    """
    popular_maps_query = """
        select map_name as name, count(map_name) as count
        from matches
        where extract(year from played)=:year and extract(month from played)=:month
        group by map_name
        order by count(map_name) desc
    """
    longest_matches_query = """
        select id
        from matches
        where extract(year from played)=:year and extract(month from played)=:month
        order by duration desc
        limit :limit
    """
    total_matches, total_players, most_matches, popular_maps, longest_matches = await asyncio.gather(
        database.fetch_one(matches_query, values={'year': year, 'month': month}),
        database.fetch_one(players_query, values={'year': year, 'month': month}),
        database.fetch_all(most_matches_query, values={'limit': limit, 'year': year, 'month': month}),
        database.fetch_all(popular_maps_query, values={'year': year, 'month': month}),
        database.fetch_all(longest_matches_query, values={'limit': limit, 'year': year, 'month': month}),
    )
    return {
        'year': year,
        'month': month,
        'total_matches': total_matches['count'],
        'total_players': total_players['count'],
        'most_matches': [dict(
            user=dict(id=m['user_id'], platform_id=m['platform_id'], name=m['user_name']),
            rank=i + 1,
            count=m['count']
        ) for i, m in enumerate(most_matches)],
        'popular_maps': compute_map_data(popular_maps)[:limit],
        'longest_match_ids': list(map(lambda m: m['id'], longest_matches))
    }
