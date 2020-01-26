import asyncio
import csv
import databases
import coloredlogs
from collections import defaultdict
import datetime
import asyncpg
import pygsheets
from decimal import Decimal
from starlette.config import Config
from starlette.datastructures import URL
from tabulate import tabulate

from aocrecs.logic.playback import (
    VILLAGER_IDS, NORMALIZED_VILLAGER_ID, PREDATOR_IDS,
    BOAR_IDS, HERDABLE_IDS, TC_IDS, HUNT_IDS, SCOUT_IDS
)

config = Config('./.env') # pylint: disable=invalid-name
DATABASE_URL = config('DATABASE_URL', cast=URL)
DEBUG = config('DEBUG', cast=bool, default=False)


def lost_to_gaia(gaia_ids):
    query = """
        select final.match_id, players.name as name, players.number, predator, timestamp::interval(0)
        from (
        with subquery as (
        select
            x.match_id, instance_id as id, name, player_number,
            destroyed_by_instance_id, x.obj_id as object_id,
            objects.name as predator, x.destroyed
        from
        (
            select oi.instance_id, player_number, ois.dataset_id, oi.destroyed_by_instance_id, ois.match_id, oi.destroyed,
            case
                when ois.object_id = any(:villager_ids) then :normalized_villager_id
                else ois.object_id
            end as obj_id
            from object_instance_states as ois join
            (
                select min(object_instance_states.id) as id,min(timestamp), match_id from object_instance_states
                join matches on match_id=matches.id
                where class_id=70 and {where}
                group by instance_id, match_id
            ) as s on ois.id=s.id and ois.match_id=s.match_id
            join object_instances as oi on ois.instance_id=oi.instance_id and oi.match_id=ois.match_id
        ) as x
        join objects on objects.id = x.obj_id and objects.dataset_id=x.dataset_id
        order by match_id, instance_id
        )
        select b.match_id, a.name as killer, b.name as unit, b.player_number, a.name as predator, b.destroyed as timestamp
        from subquery as a
        join subquery as b on a.id=b.destroyed_by_instance_id and a.match_id=b.match_id
        where a.object_id = any(:gaia_ids) and b.object_id = :normalized_villager_id
        ) as final
        join players on players.match_id=final.match_id and players.number=final.player_number
    """
    return query, 'count(*)', dict(
        villager_ids=VILLAGER_IDS,
        normalized_villager_id=NORMALIZED_VILLAGER_ID,
        gaia_ids=gaia_ids
    )


def housed():
    query = """
        select timeseries.match_id, sum(case when headroom=0 then 1 else 0 end) as seconds_housed, players.name, players.number
        from timeseries join matches on matches.id=timeseries.match_id
        join players on players.match_id=matches.id and timeseries.player_number=players.number
        where {where}
        group by players.name, players.number, timeseries.match_id
    """
    return query, 'round(avg(seconds_housed))::integer', dict()


def stealers(object_ids):
    query = """
    select players.match_id, opp.name, opp.number, destroyed::interval(0) as timestamp
from (
    select oi.instance_id, player_number, ois.dataset_id, oi.destroyed_by_instance_id, ois.match_id, oi.created_x, oi.created_y, oi.destroyed
    from object_instance_states as ois join
    (select min(object_instance_states.id) as id,min(timestamp), match_id from object_instance_states
join matches on match_id=matches.id
        where class_id=70 and {where} and object_id = any(:object_ids) group by instance_id, match_id
    ) as s on ois.id=s.id and ois.match_id=s.match_id
    join object_instances as oi on ois.instance_id=oi.instance_id and oi.match_id=ois.match_id
) as boars
join players on boars.match_id=players.match_id
join matches on players.match_id=matches.id
join
(
    select oi.instance_id, player_number, ois.dataset_id, oi.destroyed_by_instance_id, ois.match_id
    from object_instance_states as ois join
    (select min(object_instance_states.id) as id,min(timestamp), match_id from object_instance_states
join matches on match_id=matches.id
        where class_id=70 and {where} and
        object_id = any(:villager_ids)
group by instance_id, match_id
    ) as s on ois.id=s.id and ois.match_id=s.match_id
    join object_instances as oi on ois.instance_id=oi.instance_id and oi.match_id=ois.match_id
) as villagers
on boars.match_id=villagers.match_id and boars.destroyed_by_instance_id=villagers.instance_id
join players as opp on matches.id=opp.match_id and opp.number=villagers.player_number
where (sqrt(power(created_x-players.start_x, 2) + power(created_y-players.start_y,2)) < sqrt(power(created_x-opp.start_x, 2) + power(created_y-opp.start_y,2))) = true and players.number <> villagers.player_number
    """
    return query, 'count(*)', dict(
        villager_ids=VILLAGER_IDS,
        object_ids=object_ids
    )

def exploration():
    query = """
        select players.match_id, explored_percent::decimal/100 as value, players.name, players.number
        from matches join players on matches.id=players.match_id
        where {where}
    """
    return query, 'round(avg(value), 2)', dict()

def relics():
    query = """
        select players.match_id, total_relics as value, players.name, players.number
        from matches join players on matches.id=players.match_id
        where {where}
    """
    return query, 'round(avg(value), 2)', dict()

def matches():
    query = """
        select players.match_id, players.name, players.number
        from matches join players on matches.id=players.match_id
        where {where}
    """
    return query, 'count(*)', dict()


def win_ratio():
    query = """
        select won, total.id as match_id, total.name, total.number
        from
        (select matches.id, name, players.number
        from matches join players on matches.id=players.match_id
        where {where}
        ) as total
        full join
        (select 'yes' as won, name, matches.id
        from matches join players on matches.id=players.match_id
        where {where} and players.winner = true
        ) as wins
        on wins.name=total.name and total.id=wins.id
    """
    return query, 'round(count(won)::decimal/count(match_id)::decimal, 2)', dict()

def wheelbarrow():
    query = """
        select players.match_id, started as value, players.name, players.number
        from research join matches on research.match_id=matches.id
        join players on players.match_id=matches.id and players.number=research.player_number
        where research.technology_id=213 and {where}
    """
    return query, 'avg(value)::interval(0)', dict()

def tc_idle():
    query = """
        select players.match_id, (extract(\'epoch\' from started)::int % 25) as seconds_idle, players.name, players.number
        from research join matches on research.match_id=matches.id
        join players on players.match_id=matches.id and players.number=research.player_number
        where research.technology_id=101 and {where}
    """
    return query, 'round(avg(seconds_idle), 0)', dict()

def floating():
    query = """
        select players.match_id, round(avg(food+wood+stone+gold), 0) as value, players.name, players.number
        from timeseries join players on timeseries.match_id=players.match_id and timeseries.player_number = players.number
        join matches on matches.id=players.match_id
        where {where}
        group by players.match_id, players.name, players.number
    """
    return query, 'avg(value)::int', dict()

def near_buildings(building_ids):
    query = """
        select ois.match_id, rusher.name, rusher.number, oi.building_started
        from object_instance_states as ois join
        (select min(object_instance_states.id) as id, min(timestamp), match_id from object_instance_states
            join matches on match_id=matches.id
            where class_id=80 and {where} and
            object_id = any(:near_buildings)
            group by instance_id, match_id
        ) as s on ois.id=s.id and ois.match_id=s.match_id
        join object_instances as oi on ois.instance_id=oi.instance_id and oi.match_id=ois.match_id
        join players as opp on opp.match_id=oi.match_id and opp.number <> player_number
        join players as rusher on rusher.match_id=oi.match_id and rusher.number = player_number
        where
            oi.building_started is not null and
            (sqrt(power(created_x-rusher.start_x, 2) + power(created_y-rusher.start_y,2)) > (sqrt(power(created_x-opp.start_x, 2) + power(created_y-opp.start_y,2))) * 3) = true
    """
    return query, 'count(distinct match_id)', dict(near_buildings=building_ids)


def imperial_bowsaw(): # alt: 1 hour bowsaw
    query = """
        select x.match_id, players.name, players.number, started as started_bowsaw, imp.finished as imp_time
        from research as x
        join matches on matches.id=x.match_id
        join players on players.match_id=x.match_id and players.number=x.player_number
        join (
            select match_id, player_number, finished from research
            where technology_id=103
        ) as imp on imp.match_id=players.match_id and imp.player_number=players.number
        where {where} and technology_id=203 and started > imp.finished
    """
    return query, 'count(match_id)', dict()

def fast_castle():
    query = """
        select x.match_id, players.name, players.number, finished as feudal_time, castle.started as castle_clicked, castle.started - finished as delay
        from research as x
        join matches on matches.id=x.match_id
        join players on players.match_id=x.match_id and players.number=x.player_number
join  (select match_id, player_number, started from research where technology_id=102
) as castle on castle.match_id=players.match_id and castle.player_number=players.number
        where {where} and technology_id=101 and (castle.started - finished) < '00:01:00'
    """
    return query, 'count(match_id)', dict()

def tc_count(): # TODO: filter out unbuilt
    query = """
        select players.match_id, players.name, players.number, count(distinct instance_id) as value
        from object_instance_states as ois join matches on matches.id=ois.match_id
        join players on matches.id=players.match_id and ois.player_number=players.number
        where {where} and object_id = any(:tc_ids)
        group by players.match_id, players.name, players.number
    """
    return query, 'round(avg(value),1)', dict(tc_ids=TC_IDS)

def daut_castle():
    query = """
        select players.match_id, players.name, players.number, x.match_id as value, destroyed_building_percent as deleted_at_percent, destroyed as timestamp
        from (
            select oi.match_id, ois.player_number, oi.deleted, oi.destroyed_building_percent, oi.destroyed
            from object_instances as oi
            join object_instance_states as ois on oi.instance_id=ois.instance_id and oi.match_id=ois.match_id
            join matches on oi.match_id=matches.id
            where {where} and ois.object_id=82
        ) as x join players on x.match_id=players.match_id and x.player_number=players.number
        where x.deleted is true and destroyed_building_percent > 0.1
    """
    return query, 'count(value)', dict()

def deer_lures():
    query = """
        select players.match_id, players.name, players.number, deer.destroyed as timestamp
        from
        (
        select oi.instance_id, player_number, ois.dataset_id, oi.destroyed_by_instance_id, ois.match_id, oi.destroyed_x, oi.destroyed_y, oi.destroyed
            from object_instance_states as ois join
            (select min(object_instance_states.id) as id,min(timestamp), match_id from object_instance_states
        join matches on match_id=matches.id
                where class_id=70 and {where} and
                object_id = any(:hunt_ids)
        group by instance_id, match_id
            ) as s on ois.id=s.id and ois.match_id=s.match_id
            join object_instances as oi on ois.instance_id=oi.instance_id and oi.match_id=ois.match_id
        ) as deer
        join
        (
            select oi.instance_id, player_number, ois.dataset_id, oi.destroyed_by_instance_id, ois.match_id
            from object_instance_states as ois join
            (select min(object_instance_states.id) as id,min(timestamp), match_id from object_instance_states
        join matches on match_id=matches.id
                where class_id=70 and {where} and
                object_id = any(:villager_ids)
        group by instance_id, match_id
            ) as s on ois.id=s.id and ois.match_id=s.match_id
            join object_instances as oi on ois.instance_id=oi.instance_id and oi.match_id=ois.match_id
        ) as villagers
        on deer.match_id=villagers.match_id and deer.destroyed_by_instance_id=villagers.instance_id
        join players on deer.match_id=players.match_id and players.number=villagers.player_number
        where sqrt(power(deer.destroyed_x-players.start_x, 2) + power(deer.destroyed_y-players.start_y,2)) < 7
    """
    return query, 'count(*)', dict(
        hunt_ids=HUNT_IDS,
        villager_ids=VILLAGER_IDS
    )

def scout_war():
    query = """
        with subquery as (
        select min(oi.instance_id) as instance_id, player_number, ois.match_id
            from object_instance_states as ois join
            (select min(object_instance_states.id) as id,min(timestamp), match_id from object_instance_states
        join matches on match_id=matches.id
                where class_id=70 and {where} and object_id = any(:scout_ids) group by instance_id, match_id
            ) as s on ois.id=s.id and ois.match_id=s.match_id
            join object_instances as oi on ois.instance_id=oi.instance_id and oi.match_id=ois.match_id
        group by player_number, ois.match_id
        order by ois.match_id
        )
        select x.match_id, players.name, players.number, oi.destroyed as won_at
        from subquery as x
        join object_instances as oi on oi.match_id=x.match_id and oi.instance_id=x.instance_id
        left join subquery as opp on oi.destroyed_by_instance_id=opp.instance_id and oi.match_id=opp.match_id
        join players on players.match_id=x.match_id and players.number = opp.player_number
    """
    return query, 'count(match_id)', dict(
        scout_ids=SCOUT_IDS
    )

def trained_unit(object_ids):
    query = """
    select (case when uses.val = 1 then 'yes' else 'no' end) as trained, total.id as match_id, total.name as name, total.number as number
    from
        (
        select 1 as val, players.name, matches.id
        from object_instance_states
        join matches on match_id=matches.id
        join players on players.match_id=matches.id and players.number=object_instance_states.player_number
        where class_id=70 and {where} and object_id=any(:object_ids) and timestamp > '00:01:00'
        group by matches.id, players.name
        ) as uses
        full join
                (select matches.id, players.name, players.number
                from matches join players on matches.id=players.match_id
                where {where}
                )
        as total on uses.name=total.name and uses.id = total.id
    """
    return query, 'round(sum(case when trained = \'yes\' then 1 else 0 end)::decimal/count(match_id)::decimal, 2)', dict(object_ids=object_ids)

def duration():
    query = """
        select players.match_id, duration, players.name as name, players.number as number
        from matches join players on matches.id=players.match_id
        where {where}
    """
    return query, 'avg(duration)::interval(0)', dict()

def bad_lure():
    query = """
        select x.match_id, players.name as name, players.number as number, oi.destroyed as timestamp
        from (
        select instance_id, min(timestamp), match_id from object_instance_states
                join matches on match_id=matches.id
                        where class_id=70 and {where} and
                        object_id = any(:boar_ids)
                group by instance_id, match_id
        ) as x join object_instances as oi on oi.match_id=x.match_id and oi.instance_id=x.instance_id
        join players on players.match_id=x.match_id
        where sqrt(power(oi.destroyed_x-players.start_x, 2) + power(oi.destroyed_y-players.start_y,2)) < 5 and
        ((players.start_x-oi.destroyed_x) > 2 or (oi.destroyed_y - players.start_y) > 2)
    """
    return query, 'count(match_id)', dict(boar_ids=BOAR_IDS)

def color():
    query = """
        select players.match_id, players.name, players.number, player_colors.name as color
        from matches join players on matches.id=players.match_id
        join player_colors on player_colors.id=players.color_id
        where {where}
    """
    return query, 'mode() within group (order by color)', dict()


def lost_techs():
    query = """
        select s.match_id, players.name, players.number, destroyed as timestamp, technologies.name as technology
        from object_instance_states as ois join
        (
            select max(object_instance_states.id) as id, match_id, instance_id
            from object_instance_states
            join matches on match_id=matches.id
            where class_id=80 and {where}
            group by instance_id, match_id
        ) as s on ois.id=s.id and ois.match_id=s.match_id
        join object_instances as oi on ois.instance_id=oi.instance_id and oi.match_id=ois.match_id
        join technologies on ois.researching_technology_id=technologies.id and ois.dataset_id=technologies.dataset_id
        join players on players.match_id=ois.match_id and players.number = ois.player_number
        where oi.destroyed is not null and ois.researching_technology_id > 0
    """
    return query, 'count(*)', dict()


def wrap(query, aggregation):
    wrapped = """
        select hc.person_name as name, {aggregation} as value
        from ({query}) as inside
        join hc on inside.name=hc.hc_name
        group by hc.person_name
    """
    return wrapped.format(query=query, aggregation=aggregation)

async def players(database, filters):
    where, values = filters
    query = """
        select distinct hc.person_name as name, string_agg(distinct hc.hc_name, ', ') as names
        from players join matches on players.match_id=matches.id
        join hc on hc.hc_name=players.name
        where {where} group by hc.person_name
    """
    return [dict(r) for r in await database.fetch_all(query.format(where=where), values=values)]


def add_header(data):
    return ['', *[v['name'] for v in sorted(data, key=lambda k: k['name'].lower())]]


async def get_result(database, qd, filters):
    query, values = qd
    f, f_v = filters
    params = dict(values, **f_v)
    return [dict(r) for r in await database.fetch_all(query.format(where=f), values=params)]


async def add_row(label, database, qd, players, filters):
    data = await get_result(database, qd, filters)
    filled = {}
    by_name = {v['name']: v['value'] for v in data}
    for x in players:
        filled[x['name']] = by_name.get(x['name'], '')
    f2 = [{'name': n, 'value': v} for n,v in filled.items()]
    return [label, *[str(v['value']) for v in sorted(f2, key=lambda k: k['name'].lower())]]


async def add_wrapped(database, p, filters, *args):
    return await asyncio.gather(
        *[
            add_row(x[0], database, (wrap(x[1][0], x[1][1]), x[1][2]), p, filters)
            for x in args
        ]
    )

def wrap_evidence(query):
    wrapped = """
        select hc.person_name as player, civilizations.name as civilization, series_metadata.name as series, matches.map_name as map, inside.*
        from ({query}) as inside
        join hc on inside.name=hc.hc_name
        join matches on inside.match_id=matches.id
        join series_metadata on matches.series_id=series_metadata.series_id
        join players on matches.id=players.match_id and players.number=inside.number
        join civilizations on players.civilization_id=civilizations.id and matches.dataset_id=civilizations.dataset_id
        order by matches.series_id, inside.match_id, inside.name
    """
    return wrapped.format(query=query)


def serialize(v):
    if isinstance(v, datetime.timedelta):
        return str(v)
    if isinstance(v, Decimal):
        return float(v)
    return v

async def add_evidence(metric, sh, database, filters):
    title, query, note = metric
    wks = sh.add_worksheet(title)
    wks.clear()
    wks.update_value((1, 1), note)
    q, a, f = query
    values = [None]
    for row in await get_result(database, (wrap_evidence(q), f), filters):
        if values[0] == None:
            values[0] = list(row.keys())
        values.append([serialize(v) for v in row.values()])
    wks.insert_rows(row=1, values=values)
    wks.adjust_column_width(0, len(values[0]))


METRICS = [
    ('# matches', matches(), 'Number of matches played'),
    ('color', color(), 'Color most chosen'),
    ('win ratio', win_ratio(), 'Win Ratio (wins/total)'),
    ('housed', housed(), 'Average seconds housed per match'),
    ('wolved', lost_to_gaia(PREDATOR_IDS), 'Number of villagers lost to predators'),
    ('boar steals', stealers(BOAR_IDS), 'Number of boars successfully stolen'),
    ('sheep steals', stealers(HERDABLE_IDS), 'Number of sheep successfully stolen'),
    ('exploration', exploration(), 'Average percent explored per match'),
    ('relics', relics(), 'Average number of relics captured per match'),
    ('wheelbarrow', wheelbarrow(), 'Average wheelbarrow research start time'),
    ('dark age tc idle', tc_idle(), 'Average dark age town center idle time per match'),
    ('floating res', floating(), 'Average floating resources per match'),
    ('trushes', near_buildings([79, 566]), 'Number of matches where player trushed'),
    ('castle drop', near_buildings([82]), 'Number of matches where player castle-dropped opponent'),
    ('imperial bow saw', imperial_bowsaw(), 'Number of time bowsaw was researched in imperial age'),
    ('fast castle', fast_castle(), 'Number of fast castles'),
    ('tc count', tc_count(), 'Average number of town centers per match'),
    ('daut castle', daut_castle(), 'Number of daut castles (deleted after at least 10% construction)'),
    ('deer lures', deer_lures(), 'Number of deer lured to town center'),
    ('boared', lost_to_gaia(BOAR_IDS), 'Number of villagers lost to boars'),
    ('scout war', scout_war(), 'Number of scout wars won (when initial scouts fight to the death)'),
    ('archers', trained_unit([4]), 'Number of matches played with archers'),
    ('scouts', trained_unit([448]), 'Number of matches played with scouts'),
    ('maa', trained_unit([75]), 'Number of matches played with men-at-arms'),
    #('drush', trained_unit([74]), 'Numer of matches played with militia but not men-at-arms'),
    ('duration', duration(), 'Average duration of matches'),
    ('bad lure', bad_lure(), 'Number of bad boar lures (boar killed outside town center)'),
    ('lost techs', lost_techs(), 'Number of buildings destroyed while a technology was researching')
]

async def run():
    coloredlogs.install(level='DEBUG' if DEBUG else 'INFO', fmt='%(asctime)s %(name)s %(levelname)s %(message)s')
    database = databases.Database(DATABASE_URL)
    await database.connect()
    rows = []
    filters = ('matches.event_id=any(:event_id)', dict(event_id=['hc', 'hc2']))
    p = await players(database, filters)
    rows.append(add_header(p))
    #rows += await asyncio.gather(
    #    add_row('color', database, color(), p, filters),
    #)
    client = pygsheets.authorize(service_file='gsheet_credentials.json')
    #sh = client.open('HC2 Recorded Game Statistics')
    sh = client.open('HC3 Player Recorded Game Statistics')
    rows += await add_wrapped(database, p, filters, *METRICS)
    wks = sh.worksheet_by_title('Summary')
    wks.clear(fields='*')
    values = list(map(list, zip(*rows)))
    wks.insert_rows(row=0, values=values)
    wks.adjust_column_width(0, len(values[0]))
    headers = wks.get_row(1, returnas='cell')
    #wks.cell((1, 2)).note = 'Color most chosen'
    for i, metric in enumerate(METRICS):
        headers[i + 1].note = metric[2]
    pcol = wks.get_col(1, returnas='cell')
    for i, player in enumerate(p):
        pcol[i + 1].note = player['names']


    for w in sh.worksheets()[1:]:
        sh.del_worksheet(w)
    for metric in METRICS:
        await add_evidence(metric, sh, database, filters)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
