"""Meta-ladders."""
import datetime
from aocrecs.consts import COLLECTION_STARTED
from aocrecs.cache import cached


@cached(ttl=1440)
async def compute_ranks(database, filters, platform_id, ladder_id):
    """Compute ranks of all ladder participants."""
    part_1 = """
        select players.user_id, players.name, players.user_name, players.rate_after as rating
        from players join matches on players.match_id=matches.id
            join (
                select user_id, max(played) as maxdate
                from players join matches on players.match_id=matches.id
                where players.platform_id=:platform_id and players.rate_after > 0 and matches.ladder_id=:ladder_id
    """
    part_2 = """
                group by user_id
            ) as s on players.user_id=s.user_id and matches.played=s.maxdate
        where matches.platform_id=:platform_id and matches.ladder_id=:ladder_id and players.rate_after > 0
        order by players.rate_after desc
    """
    values = {'platform_id': platform_id, 'ladder_id': ladder_id}
    if filters:
        part_1 += " and " + filters[0]
        values.update(filters[1])
    return await database.fetch_all(part_1 + part_2, values=values)


async def compute_rank(database, user_id, filters, platform_id, ladder_id):
    """Get user's rank and rating on a given ladder."""
    results = await compute_ranks(database, filters, platform_id, ladder_id)
    for i, player in enumerate(results):
        if player['user_id'] == user_id:
            return {'rank': i + 1, 'rating': player['rating']}
    return None


async def get_meta_ranks(database, user_id, platform_id, ladder_ids):
    """Get ladder ranks for a given user."""
    query = 'select id, platform_id, name from ladders where platform_id=:platform_id and id = any(:ladder_ids)'
    results = await database.fetch_all(query, values={'platform_id': platform_id, 'ladder_ids': ladder_ids})
    ranks = []
    for ladder in results:
        rank = await compute_rank(database, user_id, None, platform_id, ladder['id'])
        if rank is None:
            continue
        ranks.append(dict(
            rank,
            ladder=dict(ladder),
            user=dict(id=user_id, platform_id=platform_id)
        ))
    return ranks


@cached(ttl=None)
async def get_ladders(database, platform_id, ladder_ids):
    """Get platform ladders."""
    query = 'select id, platform_id, name from ladders where platform_id=:platform_id and id = any(:ladder_ids)'
    values = {'platform_id': platform_id, 'ladder_ids': ladder_ids}
    return list(map(dict, await database.fetch_all(query, values=values)))


@cached(ttl=1440)
async def get_streak(database, user_id, platform_id, ladder_id):
    """Compute player's most recent win/loss streak."""
    query = """
        select (case when players.winner is true then count(players.match_id) else -1 * count(players.match_id) end) as streak
        from players join matches on matches.id=players.match_id
        where matches.played > (
            select max(played) as boundary
            from matches join players on matches.id=players.match_id
            where players.user_id=:id and matches.platform_id=:platform_id and matches.ladder_id=:ladder_id
            group by players.winner
            order by max(played)
            limit 1
        ) and players.user_id=:id and matches.platform_id=:platform_id and matches.ladder_id=:ladder_id
        group by players.winner limit 1
    """
    streak = await database.fetch_one(query, values={'id': user_id, 'platform_id': platform_id, 'ladder_id': ladder_id})
    if streak:
        return streak['streak']
    return None


@cached(ttl=1440)
async def get_rate_by_day(database, user_id, platform_id, ladder_id):
    """Compute max rate reached per day for a player."""
    query = """
        select matches.played::date as date, max(players.rate_after) as count
        from matches join players on matches.id=players.match_id
        where players.user_id=:id and matches.platform_id=:platform_id and matches.ladder_id=:ladder_id
            and matches.played is not null and matches.played > :after and matches.played < :before
        group by date
        order by date
    """
    rates = await database.fetch_all(query, values={
        'id': user_id,
        'platform_id': platform_id,
        'ladder_id': ladder_id,
        'after': COLLECTION_STARTED,
        'before': datetime.date.today()
    })
    return list(map(dict, rates))


async def get_ranks(database, platform_id, ladder_id, limit):
    """Contextualize ladder ranks."""
    ranks = await compute_ranks(database, None, platform_id, ladder_id)
    return [
        dict(
            rank=i + 1,
            rating=r['rating'],
            user=dict(
                id=r['user_id'],
                name=r['user_name'] if r['user_name'] else r['name'],
                platform_id=platform_id
            ),
            ladder=dict(
                id=ladder_id
            )
        )
        for i, r in enumerate(ranks[:limit])
    ]
