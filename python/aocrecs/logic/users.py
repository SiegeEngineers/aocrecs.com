"""Users."""
import asyncio

from aocrecs.cache import cached, dataloader_cached
from aocrecs.util import by_key, compound_where


@dataloader_cached(ttl=1440)
async def get_person(keys, context): # pylint: disable=too-many-locals
    """Get person."""
    where, values = compound_where(keys, ('user_id', 'platform_id'))
    account_query = """
        select canonical_players.user_id as id, canonical_players.platform_id, max(players.name) as name
        from canonical_players
        join (select name from canonical_players where {}) as s on canonical_players.name=s.name
        join players on players.user_id=canonical_players.user_id and players.platform_id=canonical_players.platform_id
        where players.human=true
        group by canonical_players.user_id, canonical_players.platform_id
    """.format(where)
    alias_query = """
        select distinct canonical_players.user_id as id, players.name as player_name, players.user_name as user_name, canonical_players.name as person_name, canonical_players.platform_id
        from canonical_players
        join (select name from canonical_players where {}) as s on canonical_players.name=s.name
        join players on players.user_id=canonical_players.user_id and players.platform_id=canonical_players.platform_id
        where players.human=true
    """.format(where)
    accounts, aliases = await asyncio.gather(
        context.database.fetch_all(account_query, values=values),
        context.database.fetch_all(alias_query, values=values)
    )

    account_data = by_key(accounts, ('id', 'platform_id'))
    alias_data = by_key(aliases, ('id', 'platform_id'))

    out = {}
    for key, aliases_ in alias_data.items():
        person_name = None
        alias_set = set()
        for row in aliases_:
            person_name = row['person_name']
            alias_set.add(row['player_name'])
            if row['user_name']:
                alias_set.add(row['user_name'])
        person = None
        if person_name:
            person = dict(
                name=person_name,
                aliases=list(alias_set),
                accounts=account_data.get(key, [])
            )
        out[key] = person
    return out


@cached(ttl=1440)
async def get_user(database, user_id, platform_id):
    """Get user."""
    query = """
        select user_name, name
        from players
        where user_id=:id and platform_id=:platform_id
        order by match_id desc limit 1
    """
    names = await database.fetch_one(query, values={'id': user_id, 'platform_id': platform_id})
    return dict(id=user_id, platform_id=platform_id, name=names['user_name'] or names['name'])


@cached(ttl=1440)
async def get_top_map(database, user_id, platform_id):
    """Get top map for user."""
    print(user_id, platform_id)
    query = """
        select map_name as name
        from players join matches on players.match_id=matches.id
        where user_id=:id and matches.platform_id=:platform_id and winner=true
        group by map_name
        order by count(id) desc limit 1
    """
    top = await database.fetch_one(query, values={'id': user_id, 'platform_id': platform_id})
    if top:
        return dict(top)
    return None


@cached(ttl=1440)
async def get_top_civilization(database, user_id, platform_id):
    """Get top civilizations for user."""
    query = """
        select civilization_id as id, civilizations.name, civilizations.dataset_id
        from players join civilizations on players.dataset_id=civilizations.dataset_id and players.civilization_id=civilizations.id
        where user_id=:id and platform_id=:platform_id and winner=true
        group by civilization_id, civilizations.name, civilizations.dataset_id
        order by count(match_id) desc limit 1
    """
    top = await database.fetch_one(query, values={'id': user_id, 'platform_id': platform_id})
    if top:
        return dict(top)
    return None


@cached(ttl=1440)
async def get_top_dataset(database, user_id, platform_id):
    """Get top dataset for user."""
    query = """
        select dataset_id as id, datasets.name
        from players join datasets on players.dataset_id=datasets.id
        where user_id=:id and platform_id=:platform_id
        group by dataset_id, datasets.name
        order by count(match_id) desc limit 1
    """
    return dict(await database.fetch_one(query, values={'id': user_id, 'platform_id': platform_id}))
