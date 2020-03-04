"""Market."""
from aocrecs.cache import cached, dataloader_cached
from aocrecs.util import by_key, compound_where


@cached(ttl=None)
async def get_prices(database, match_id):
    """Get market prices."""
    query = """
        select
            timestamp::interval(0), extract(epoch from timestamp)::integer as timestamp_secs,
            round((food + (food * .3)) * 100) as buy_food, round((wood + (wood * .3)) * 100) as buy_wood, round((stone + (stone * .3)) * 100) as buy_stone,
            round((food - (food * .3)) * 100) as sell_food, round((wood - (wood * .3)) * 100) as sell_wood, round((stone - (stone * .3)) * 100) as sell_stone
        from market
        where match_id=:match_id
        order by timestamp
    """
    results = await database.fetch_all(query, values=dict(match_id=match_id))
    return list(map(dict, results))


@dataloader_cached(ttl=None)
async def get_transactions(keys, context):
    """Get transactions."""
    where, values = compound_where(keys, ('players.match_id', 'player_number'))
    query = """
        select
            players.match_id, timestamp::interval(0), extract(epoch from timestamp)::integer as timestamp_secs,
            player_number,
            case when action_id=123 then 'Gold' else resources.name end as sold_resource,
            (amount * 100) as sold_amount,
            case when action_id=123 then resources.name else 'Gold' end as bought_resource
        from players left join transactions on transactions.match_id=players.match_id and transactions.player_number = players.number
        join resources on transactions.resource_id=resources.id
        where {}
        order by timestamp
    """.format(where)
    results = await context.database.fetch_all(query, values=values)
    return by_key(results, ('match_id', 'player_number'), defaults=keys)


@cached(ttl=None)
async def get_tribute(database, match_id):
    """Get tribute."""
    query = """
        select
            match_id, timestamp::interval(0), extract(epoch from timestamp)::integer as timestamp_secs,
            resources.name as resource, player_number, target_player_number,
            round(amount + (amount * fee)) as spent, round(amount) as received, round(fee * 100) as fee
        from tribute join resources on tribute.resource_id=resources.id
        where match_id=:match_id
        order by timestamp
    """
    results = await database.fetch_all(query, values=dict(match_id=match_id))
    return list(map(dict, results))
