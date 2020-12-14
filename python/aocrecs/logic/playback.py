"""Playback queries."""
import asyncio
from collections import defaultdict

from aocrecs.cache import cached, dataloader_cached
from aocrecs.util import by_key, compound_where
from aocrecs.logic import flags, metrics

from aocrecs.consts import (
    NORMALIZED_VILLAGER_ID, VILLAGER_IDS, NORMALIZED_MONK_ID,
    MONK_IDS, PREDATOR_IDS, BOAR_IDS, HERDABLE_IDS,
    FOOD_VILLAGER_IDS, WOOD_VILLAGER_IDS, STONE_VILLAGER_IDS,
    GOLD_VILLAGER_IDS, RESOURCE_VILLAGER_IDS
)

NORMALIZE_VALUES = dict(
    villager_ids=VILLAGER_IDS,
    normalized_villager_id=NORMALIZED_VILLAGER_ID,
    herdable_ids=HERDABLE_IDS,
    monk_ids=MONK_IDS,
    normalized_monk_id=NORMALIZED_MONK_ID
)

FLAGS = [
    ('deer_pushes', 'Deer Pushes', True, flags.deer_pushes()),
    ('daut_castles', 'Daut Castles', True, flags.daut_castle()),
    ('castle_drops', 'Castle Drops', True, flags.near_buildings([82])),
    ('boar_steals', 'Boar Steals', True, flags.thieves(BOAR_IDS)),
    ('sheep_steals', 'Sheep Steals', True, flags.thieves(HERDABLE_IDS)),
    ('lost_to_boar', 'Villager Lost to Boar', True, flags.lost_to_gaia(BOAR_IDS)),
    ('lost_to_predator', 'Villager Lost to Predator', True, flags.lost_to_gaia(PREDATOR_IDS)),
    ('lost_research', 'Lost Researches', True, flags.lost_techs()),
    ('bad_boar_lure', 'Bad Boar Lure', True, flags.bad_lure()),
    ('scout_war', 'Won Scout War', True, flags.scout_war()),
    ('trushes', 'Trush Towers', True, flags.near_buildings([79, 566])),
    ('fast_castle', 'Fast Castle', True, flags.fast_castle()),
    #('imperial horse collar', 'Imperial Horse Collar', True, flags.research_order(14, 203, [2])),
    ('badaboom', 'Splash Damage Kills', True, flags.badaboom()),
    ('castle_race', 'Won Castle Race', True, flags.castle_race()),
    ('archers', 'Trained Archers in Feudal', False, flags.trained_unit([4], 102)),
    ('skirms', 'Trained Skirmishers in Feudal', False, flags.trained_unit([7], 102)),
    ('scouts', 'Trained Scouts in Feudal', False, flags.trained_unit([448], 102)),
    ('drush', 'Drushed', False, flags.drush()),
    ('maa', 'Trained Men-at-arms in Feudal', False, flags.maa()),
    ('tc_killed_boar', 'Town Center killed Boar', True, flags.gaia_killed_by_tc(BOAR_IDS)),
    ('tc_killed_sheep', 'Town Center killed Sheep', True, flags.gaia_killed_by_tc(HERDABLE_IDS)),
    ('scout_lost_to_tc', 'Scout Lost to Town Center', True, flags.scout_lost_to_tc(102)),
]
METRICS = [
    ('dark_age_tc_idle', metrics.tc_idle()),
    ('total_tcs', metrics.tc_count()),
    ('average_floating_resources', metrics.floating()),
    ('seconds_housed', metrics.housed()),
    ('seconds_villagers_idle', metrics.villagers_idle()),
    ('seconds_popcapped', metrics.popcapped()),
    ('apm', metrics.apm())
]


@cached(ttl=None)
async def get_graph(database, match_id):
    """Get kill-graph nodes and edges."""
    node_query = """
        select instance_id as id, objects.name, players.color_id
        from (
            select instance_id, match_id, dataset_id, initial_player_number,
                case
                    when initial_object_id=any(:villager_ids) then :normalized_villager_id
                    when initial_object_id=any(:monk_ids) then :normalized_monk_id
                    else initial_object_id
                end as initial_object_id
            from object_instances
            where match_id=:match_id and initial_class_id=70 and initial_player_number > 0 and not (initial_object_id=any(:herdable_ids))
        ) as oi
        join objects on objects.id = oi.initial_object_id and objects.dataset_id=oi.dataset_id
        join players on players.number=oi.initial_player_number and players.match_id=oi.match_id
    """
    link_query = """
        with subquery as (
            select oi.instance_id as target, oi.destroyed_by_instance_id as source
            from object_instances as oi
            where match_id=:match_id and initial_class_id=70 and initial_player_number > 0 and not (initial_object_id=any(:herdable_ids))
        )
        select a.target, a.source
        from subquery as a join subquery as b on a.source=b.target
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
async def get_timeseries(keys, context):
    """Get timeseries data."""
    where, values = compound_where(keys, ('match_id', 'player_number'))
    query = """
        select
            player_number, match_id, timestamp, population, military,
            percent_explored, relic_gold, total_food, total_gold, total_stone,
            total_wood, trade_profit, value_current_units, value_lost_buildings,
            value_lost_units, value_objects_destroyed, value_spent_objects,
            value_spent_research, extract(epoch from timestamp)::integer as timestamp_secs,
            tribute_sent, tribute_received, kills, deaths, razes,
            kills - deaths as  kd_delta,
            case when value_lost_units+value_lost_buildings > 0 then value_objects_destroyed/(value_lost_units+value_lost_buildings)::float else 0.0 end as damage,
            case when value_spent_research > 100 then value_objects_destroyed/(value_spent_research)::float * 100 else 0.0 end as roi
        from timeseries
        where {}
        order by timestamp
    """.format(where)
    results = await context.database.fetch_all(query, values=values)
    return by_key(results, ('match_id', 'player_number'))


@dataloader_cached(ttl=None)
async def get_apm(keys, context):
    """Compute actions per minute."""
    query = """
        select x.match_id, x.player_number, x.ts as timestamp,
        extract(epoch from x.ts)::integer as timestamp_secs,
        sum(x.actions) over (partition by x.match_id, x.player_number ORDER BY x.ts rows between (60/:sample_rate)-1 preceding and current row) as actions
        from (
            select al.match_id, al.player_number, al.ts, count(action_log.action_id) as actions
            from action_log right join (
                select
                    match_id, number as player_number, make_interval(secs => extract('epoch' from generate_series(min(to_timestamp(0))::timestamp, max(to_timestamp(extract('epoch' from duration)))::timestamp, :sample_rate * interval '1 seconds'))) AS ts
                from players join matches on players.match_id=matches.id
                where match_id = any(:match_ids)
                group by match_id, number
            ) as al on
                action_log.match_id=al.match_id and
                make_interval(secs => floor((extract('epoch' from action_log.timestamp) / :sample_rate )) * :sample_rate)=al.ts and
                action_log.player_number=al.player_number
            where action_log.match_id = any(:match_ids)
            group by al.match_id, al.player_number, al.ts
        ) as x
        order by x.match_id, x.player_number, x.ts
    """
    results = await context.database.fetch_all(query, values=dict(match_ids=[k[0] for k in keys], sample_rate=30))
    return by_key(results, ('match_id', 'player_number'))


@dataloader_cached(ttl=None)
async def get_map_control(keys, context):
    """Get estimated map control from actions."""
    query = """
        with subquery as (
            select x.match_id, x.player_number, x.team_id,
            make_interval(secs => floor((extract('epoch' from x.ts) / :sample_rate )) * :sample_rate) as timestamp,
            case when avg(x.ma) is not null then avg(x.ma) else 0 end as control
            from (
                select al.match_id, al.player_number, al.team_id, al.ts,
                max(round((((to_me - to_opp) + between) / (between * 2)) * 100)) as control,
                avg(max(round((((to_me - to_opp) + between) / (between * 2)) * 100))) over (partition by al.match_id, al.team_id, al.player_number ORDER BY al.ts rows between :sample_rate-1 preceding and current row) as ma
                from (
                    select
                        al.match_id, al.player_number, al.timestamp, opps.number as other_number,
                        sqrt(power(al.action_x-players.start_x, 2) + power(al.action_y-players.start_y, 2)) as to_me,
                        sqrt(power(al.action_x-opps.start_x, 2) + power(al.action_y-opps.start_y, 2)) as to_opp,
                        sqrt(power(opps.start_x-players.start_x, 2) + power(opps.start_y-players.start_y, 2)) as between
                    from action_log as al join players on al.match_id=players.match_id and al.player_number=players.number
                    join players as opps on opps.match_id=players.match_id and opps.number!=players.number and opps.team_id!=players.team_id
                    where al.action_x is not null and al.action_y is not null and al.match_id = any(:match_ids)
                ) as x right join (
                    select
                        match_id, team_id, number as player_number, make_interval(secs => extract('epoch' from generate_series(min(to_timestamp(0))::timestamp, max(to_timestamp(extract('epoch' from duration)))::timestamp, interval '1 seconds'))) AS ts
                    from players join matches on players.match_id=matches.id
                    where match_id = any(:match_ids)
                    group by match_id, team_id, number
                ) as al on x.match_id=al.match_id and x.player_number=al.player_number and make_interval(secs => floor((extract('epoch' from x.timestamp) / 1 )) * 1)=al.ts
                group by al.match_id, al.player_number, al.team_id, al.ts
            ) as x
            group by x.match_id, x.player_number, x.team_id, make_interval(secs => floor((extract('epoch' from x.ts) / :sample_rate)) * :sample_rate)
        )
        select a.match_id, a.player_number, a.timestamp, extract(epoch from a.timestamp)::integer as timestamp_secs, round((((a.control-b.control)+100)/200)*100) as control_percent
        from subquery as a join subquery as b on a.match_id=b.match_id and a.timestamp=b.timestamp and a.player_number != b.player_number and a.team_id != b.team_id
        order by a.timestamp
    """
    results = await context.database.fetch_all(query, values=dict(match_ids=[k[0] for k in keys], sample_rate=30))
    return by_key(results, ('match_id', 'player_number'))



@dataloader_cached(ttl=None)
async def get_units_trained(keys, context):
    """Get counts of units trained bucketed by interval."""
    where, values = compound_where(keys, ('match_id', 'player_number'))
    query = """
        select player_number, x.match_id, objects.id as object_id, name, count, inter as timestamp, extract(epoch from inter)::integer as timestamp_secs
        from
        (
            select oi.match_id, player_number, ois.dataset_id,
            case
                when ois.object_id=any(:villager_ids) then :normalized_villager_id
                when ois.object_id=any(:monk_ids) then :normalized_monk_id
                else ois.object_id
            end as obj_id,
            to_timestamp(floor((extract('epoch' from created) / :interval )) * :interval) as inter,
            count(ois.instance_id) as count
            from object_instance_states as ois join
            (
                select min(id) as id,min(timestamp) from object_instance_states
                where ({}) and player_number > 0 and class_id=70 and not (object_id=any(:herdable_ids))
                group by instance_id
            ) as s on ois.id=s.id
            join object_instances as oi on ois.instance_id=oi.instance_id and oi.match_id=ois.match_id
            where oi.created > '00:00:10'
            group by player_number, obj_id, ois.dataset_id, oi.match_id, inter
            order by count desc
        ) as x join objects on x.obj_id=objects.id and x.dataset_id=objects.dataset_id
        order by timestamp, name
    """.format(where)
    results = await context.database.fetch_all(query, values=dict(values, interval=300, **NORMALIZE_VALUES))
    return by_key(results, ('match_id', 'player_number'))


@dataloader_cached(ttl=None)
async def get_flags(keys, context): # pylint: disable=too-many-locals
    """Get flagged player events."""
    results = {}
    for k in keys:
        results[k] = []
    for type_, name, use_evidence, (query, i_values) in FLAGS:
        if not use_evidence:
            continue
        if '{sq}' in query:
            query = query.format(sq='select id from matches where id = any(:match_ids)')
        query = f"""
            select inside.*
            from ({query}) as inside
            where match_id = any(:match_ids)
        """
        evidence_query = f'{query} order by timestamp'
        agg_query = f"""
            select inside.match_id, inside.number, count(*) as count
            from ({query}) as inside
            group by inside.match_id, inside.number
        """

        values = dict(i_values, match_ids=[k[0] for k in keys])
        evidence, flag_result = await asyncio.gather(
            context.database.fetch_all(evidence_query, values=values),
            context.database.fetch_all(agg_query, values=values)
        )

        evidence_lookup = defaultdict(list)
        for data in map(dict, evidence):
            evidence_lookup[(data['match_id'], data['number'])].append(
                dict(timestamp=data['timestamp'], value=data.get('value'))
            )

        for result in flag_result:
            key = (result['match_id'], result['number'])
            if key not in keys:
                continue
            results[key].append(dict(
                type=type_,
                name=name,
                count=result['count'],
                evidence=evidence_lookup[key]
            ))
    return results


@dataloader_cached(ttl=None)
async def get_metrics(keys, context):
    """Get player metrics."""
    queries = []
    for _, (query, values) in METRICS:
        if '{sq}' in query:
            query = query.format(sq='select id from matches where id = any(:match_ids)')
        queries.append(context.database.fetch_all(
            f"""
                select inside.*
                from ({query}) as inside
                where match_id = any(:match_ids)
            """,
            values=dict(values, match_ids=[k[0] for k in keys])
        ))

    results = defaultdict(dict)
    for i, metric_result in enumerate(await asyncio.gather(*queries)):
        for result in metric_result:
            key = (result['match_id'], result['number'])
            if key not in keys:
                continue
            results[key][METRICS[i][0]] = result['value']
    return results


async def object_count_query(database, match_ids, object_ids):
    """Count objects per interval."""
    query = """
        select
            ts.match_id, ts.number as player_number,
            ts.ts as timestamp, extract(epoch from ts.ts)::integer as timestamp_secs,
            sum(case when oi.created is null then 0 else 1 end) as count
        from (
        SELECT match_id, number, make_interval(secs => extract('epoch' from generate_series(min(to_timestamp(0))::timestamp, max(to_timestamp(extract('epoch' from duration)))::timestamp, :sample_rate * interval '1 second'))) AS ts
           FROM   players join matches on players.match_id=matches.id
           where match_id = any(:match_ids)
           GROUP  BY match_id, number
        ) as ts left join (
        select match_id, initial_player_number, created, destroyed
        from object_instances
        where initial_object_id = any(:object_ids) and match_id = any(:match_ids)
        ) as oi on oi.created <= (ts + (:sample_rate * interval '1 second')) and (oi.destroyed is null or oi.destroyed >= ts) and ts.match_id=oi.match_id and ts.number=oi.initial_player_number
        group by ts.match_id, ts.number, ts.ts
        order by ts.match_id, ts.number, ts.ts
    """
    results = await database.fetch_all(query, values=dict(match_ids=match_ids, object_ids=object_ids, sample_rate=30))
    return by_key(results, ('match_id', 'player_number'))


@dataloader_cached(ttl=None)
async def get_trade_carts(keys, context):
    """Get trade cart counts by interval."""
    return await object_count_query(context.database, [k[0] for k in keys], [128])


@dataloader_cached(ttl=None)
async def get_villagers(keys, context):
    """Get villager counts by interval."""
    return await object_count_query(context.database, [k[0] for k in keys], VILLAGER_IDS)


@dataloader_cached(ttl=None)
async def get_villager_allocation(keys, context):
    """Get villager allocation per player bucketed by interval."""
    where, values = compound_where(keys, ('match_id', 'player_number'))
    query = """
        select
            vils.match_id, vils.player_number, vils.res as name, buckets.inter as timestamp,
            extract(epoch from buckets.inter)::integer as timestamp_secs, count(distinct vils.instance_id)
        from (
            with subquery as (
                select row_number() over (order by x.instance_id, inter), x.match_id, ois.player_number, x.instance_id, x.inter, objects.name, oi.created, oi.destroyed,
                case
                    when object_id = any(:food_vils) then 'Food'
                    when object_id = any(:wood_vils) then 'Wood'
                    when object_id = any(:gold_vils) then 'Gold'
                    when object_id = any(:stone_vils) then 'Stone'
                    else 'idle'
                end as res
                from (
                    select max(id) as id, match_id, instance_id, make_interval(secs => floor((extract('epoch' from timestamp) / :interval )) * :interval) as inter
                    from object_instance_states
                    where object_id = any(:resource_vils)
                    and ({where})
                    group by instance_id, inter, match_id
                ) as x join object_instance_states as ois on x.match_id=ois.match_id and x.id=ois.id
                join object_instances oi on oi.match_id=ois.match_id and oi.instance_id=ois.instance_id
                join objects on objects.id=ois.object_id and objects.dataset_id=ois.dataset_id
            )
            select f.*, l.inter as next from
            subquery as f left join subquery as l on f.row_number=l.row_number-1 and f.instance_id=l.instance_id
        ) as vils join (
            select make_interval(secs => floor((extract('epoch' from timestamp) / :interval )) * :interval) as inter
            from object_instance_states as ois
            where ({where})
            group by inter
            order by inter
        ) as buckets on
            vils.inter <= buckets.inter and (vils.next is null or vils.next > buckets.inter) and
            vils.created <= (buckets.inter + (:interval * interval '1 second')) and
            (vils.destroyed is null or vils.destroyed >= buckets.inter)
        group by vils.match_id, vils.player_number, vils.res, buckets.inter
        order by buckets.inter, vils.player_number, vils.res
    """.format(where=where)
    results = await context.database.fetch_all(query, values=dict(
        values,
        resource_vils=RESOURCE_VILLAGER_IDS,
        food_vils=FOOD_VILLAGER_IDS,
        wood_vils=WOOD_VILLAGER_IDS,
        gold_vils=GOLD_VILLAGER_IDS,
        stone_vils=STONE_VILLAGER_IDS,
        interval=300
    ))
    return by_key(results, ('match_id', 'player_number'))
