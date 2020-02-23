"""Users."""
import asyncio

from aocrecs.cache import cached


@cached(ttl=1440)
async def get_people(database):
    """Get all people."""
    query = """
        select
            people.id, people.name, people.country, count(distinct match_id) as match_count,
            min(extract(year from matches.played)) as first_year, max(extract(year from matches.played)) as last_year
        from people join users on people.id=users.person_id
        join players on users.id=players.user_id and players.platform_id=users.platform_id
        join matches on players.match_id=matches.id
        where players.human=true
        group by people.id, people.name, people.country
        order by people.name
    """
    return list(map(dict, await database.fetch_all(query)))


@cached(ttl=1440)
async def get_person(database, person_id):
    """Get a person."""
    person_query = """
        select id, name, country from people
        where id=:person_id
    """
    account_query = """
        select users.id, users.platform_id, max(players.name) as name, platforms.name as platform_name
        from users join players on players.user_id=users.id and players.platform_id=users.platform_id
        join platforms on users.platform_id=platforms.id
        where person_id=:person_id and players.human=true
        group by users.id, users.platform_id, platforms.name
        order by platforms.name, max(players.name)
    """
    event_query = """
        select distinct events.id, events.name, events.year
        from people join users on people.id=users.person_id
        join players on users.id=players.user_id and players.platform_id=users.platform_id
        join matches on players.match_id=matches.id
        join events on events.id=matches.event_id
        where person_id=:person_id and players.human=true
        order by events.year desc
    """
    alias_query = """
        select distinct players.name, players.user_name
        from users join players on players.user_id=users.id and players.platform_id=users.platform_id
        where person_id=:person_id and players.human=true
    """
    person, accounts, aliases, events = await asyncio.gather(
        database.fetch_one(person_query, values=dict(person_id=person_id)),
        database.fetch_all(account_query, values=dict(person_id=person_id)),
        database.fetch_all(alias_query, values=dict(person_id=person_id)),
        database.fetch_all(event_query, values=dict(person_id=person_id))
    )
    aliases_set = set()
    for row in aliases:
        if row['name']:
            aliases_set.add(row['name'])
        if row['user_name']:
            aliases_set.add(row['user_name'])
    return dict(
        person,
        accounts=[
            dict(
                id=a['id'],
                name=a['name'],
                platform_id=a['platform_id'],
                platform=dict(id=a['platform_id'], name=a['platform_name'])
            ) for a in accounts
        ],
        aliases=list(aliases_set),
        events=[dict(e) for e in events]
    )


@cached(ttl=1440)
async def get_user(database, user_id, platform_id):
    """Get user."""
    query = """
        select u.user_id, u.name, u.user_name, people.id as person_id, people.name as person_name, people.country
        from (
            select user_name, name, user_id
            from players join matches on players.match_id=matches.id
            where players.user_id=:user_id and players.platform_id=:platform_id and players.human=true
            order by matches.played desc limit 1
        ) as u join users on u.user_id=users.id
        left join people on users.person_id=people.id
    """
    user = await database.fetch_one(query, values={'user_id': user_id, 'platform_id': platform_id})
    person = None
    if user['person_name']:
        person = dict(
            id=user['person_id'],
            name=user['person_name'],
            country=user['country']
        )
    return dict(
        id=user_id,
        platform_id=platform_id,
        name=user['user_name'] or user['name'],
        person=person
    )


@cached(ttl=1440)
async def get_top_map(database, user_id, platform_id):
    """Get top map for user."""
    query = """
        select map_name as name
        from players join matches on players.match_id=matches.id
        where user_id=:id and matches.platform_id=:platform_id and winner=true and human=true
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
        where user_id=:id and platform_id=:platform_id and winner=true and human=true
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
        where user_id=:id and platform_id=:platform_id and human=true
        group by dataset_id, datasets.name
        order by count(match_id) desc limit 1
    """
    return dict(await database.fetch_one(query, values={'id': user_id, 'platform_id': platform_id}))
