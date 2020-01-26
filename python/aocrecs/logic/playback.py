import asyncio

from aocrecs.cache import cached, dataloader_cached
from aocrecs.util import by_key, compound_where


NORMALIZED_VILLAGER_ID = 83
VILLAGER_IDS = [
    83, 218, 123, 581, 579, 354, 120, 220, 259, 212, 112,
    124, 590, 592, 214, 212, 118, 216, 293, 122
]
NORMALIZED_MONK_ID = 125
MONK_IDS = [
    125, 286
]
NORMALIZED_PREDATOR_ID = 126
PREDATOR_IDS = [126, 486, 812, 1029, 1031, 1135, 1137]
BOAR_IDS = [
    48, 412, 822, 1139
]
HERDABLE_IDS = [
    594, 1060, 705, 305, 833, 1142
]
HUNT_IDS = [
    65, 333, 329, 1026, 1019
]
TC_IDS = [
    71, 109, 141, 142
]
SCOUT_IDS = [
    448, 751
]
NORMALIZE_VALUES = dict(
    villager_ids=VILLAGER_IDS,
    normalized_villager_id=NORMALIZED_VILLAGER_ID,
    herdable_ids=HERDABLE_IDS,
    monk_ids=MONK_IDS,
    normalized_monk_id=NORMALIZED_MONK_ID
)


async def get_graph(database, match_id):
    node_query = """
        select instance_id as id, name from
        (
            select oi.instance_id, player_number, ois.dataset_id,
            case
                when ois.object_id=any(:villager_ids) then :normalized_villager_id
                when ois.object_id=any(:monk_ids) then :normalized_monk_id
                else ois.object_id
            end as obj_id
            from object_instance_states as ois join
            (
                select min(id) as id,min(timestamp) from object_instance_states
                where match_id=:match_id and class_id=70 and player_number > 0 and not (object_id=any(:herdable_ids))
                group by instance_id
            ) as s on ois.id=s.id
            join object_instances as oi on ois.instance_id=oi.instance_id and oi.match_id=ois.match_id
        ) as x
        join objects on objects.id = x.obj_id and objects.dataset_id=x.dataset_id
        order by instance_id
    """
    link_query = """
        select oi.instance_id as target, oi.destroyed_by_instance_id as source
        from object_instance_states as ois join
        (
            select min(id) as id,min(timestamp) from object_instance_states
            where match_id=:match_id and class_id=70 and player_number > 0 and not (object_id=any(:herdable_ids))
            group by instance_id
        ) as s on ois.id=s.id
        join object_instances as oi on ois.instance_id=oi.instance_id and oi.match_id=ois.match_id
        join
        (
            select min(class_id) as class_id, instance_id from object_instance_states
            where match_id=:match_id and class_id=70 and player_number > 0 and not (object_id=any(:herdable_ids))
            group by instance_id
        ) as z on oi.destroyed_by_instance_id=z.instance_id
    """
    nodes, links = await asyncio.gather(
        database.fetch_all(node_query, values=dict(match_id=match_id, **NORMALIZE_VALUES)),
        database.fetch_all(link_query, values=dict(match_id=match_id, herdable_ids=HERDABLE_IDS))
    )
    link_ids = {l['source'] for l in links} | {l['target'] for l in links}
    return dict(
        nodes=[dict(n) for n in nodes if n['id'] in link_ids],
        links=[dict(l) for l in links]
    )


@dataloader_cached(ttl=None)
async def get_units_trained(keys, database):
    where, values = compound_where(keys, ('match_id', 'player_number'))
    query = """
        select player_number, x.match_id, objects.id as object_id, name, count
        from
        (
            select oi.match_id, player_number, ois.dataset_id,
            case
                when ois.object_id=any(:villager_ids) then :normalized_villager_id
                when ois.object_id=any(:monk_ids) then :normalized_monk_id
                else ois.object_id
            end as obj_id,
            count(ois.instance_id) as count
            from object_instance_states as ois join
            (
                select min(id) as id,min(timestamp) from object_instance_states
                where ({}) and player_number > 0 and class_id=70 and not (object_id=any(:herdable_ids))
                group by instance_id
            ) as s on ois.id=s.id
            join object_instances as oi on ois.instance_id=oi.instance_id and oi.match_id=ois.match_id
            group by player_number, obj_id, ois.dataset_id, oi.match_id
            order by count desc
        ) as x join objects on x.obj_id=objects.id and x.dataset_id=objects.dataset_id
    """.format(where)
    results = await database.fetch_all(query, values=dict(values, **NORMALIZE_VALUES))
    return by_key(results, ('match_id', 'player_number'))
