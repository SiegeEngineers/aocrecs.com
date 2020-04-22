"""Compute flagged events."""
from aocrecs.consts import VILLAGER_IDS, BOAR_IDS, HUNT_IDS, SCOUT_IDS, SPLASH_DAMAGE_IDS, TC_IDS


def lost_to_gaia(gaia_ids):
    """Find villagers lost to specified gaia object types."""
    query = """
        select units.match_id, units.initial_player_number as number, units.destroyed::interval(0) as timestamp
        from object_instances as gaia join object_instances as units on units.destroyed_by_instance_id=gaia.instance_id and units.match_id=gaia.match_id
        where
            units.initial_object_id = any(:villager_ids) and
            gaia.initial_object_id = any(:gaia_ids)
    """
    return query, dict(
        villager_ids=VILLAGER_IDS,
        gaia_ids=gaia_ids
    )


def thieves(object_ids):
    """Find instances of thievery based on starting position of players and gaia objects."""
    query = """
        select thief.match_id, thief.number, oi.destroyed::interval(0) as timestamp
        from object_instances as oi join matches on oi.match_id=matches.id
        join players as owner on oi.match_id=owner.match_id
        join players as thief on oi.match_id=thief.match_id and owner.number <> thief.number
        where
            oi.initial_object_id = any(:object_ids) and
            oi.initial_class_id = 70 and
            oi.destroyed_by_instance_id > 0 and
            sqrt(power(thief.start_x-oi.destroyed_x, 2) + power(thief.start_y-oi.destroyed_y, 2)) < 5
            and
                sqrt(power(oi.created_x-owner.start_x, 2) + power(oi.created_y-owner.start_y,2))
                < sqrt(power(oi.created_x-thief.start_x, 2) + power(oi.created_y-thief.start_y, 2))
    """
    return query, dict(object_ids=object_ids)


def near_buildings(building_ids):
    """Find buildings built near enemy."""
    query = """
        select rusher.match_id, rusher.number, oi.building_started::interval(0) as timestamp
        from object_instances as oi join players as opp on opp.match_id=oi.match_id and opp.number <> oi.initial_player_number
        join players as rusher on rusher.match_id=oi.match_id and rusher.number = oi.initial_player_number
        where
            oi.initial_class_id=80 and oi.initial_object_id=any(:near_buildings) and
            oi.building_started is not null and oi.building_completed is not null and
            (sqrt(power(created_x-rusher.start_x, 2) + power(created_y-rusher.start_y,2))
            > (sqrt(power(created_x-opp.start_x, 2) + power(created_y-opp.start_y,2))) * 3)
    """
    return query, dict(near_buildings=building_ids)


def daut_castle():
    """Find castles deleted after more than 10% built."""
    query = """
        select
            players.match_id, players.number, destroyed_building_percent as destroyed_at_percent, oi.deleted, destroyed::interval(0) as timestamp
        from object_instances as oi join players on oi.match_id=players.match_id and oi.initial_player_number=players.number
        where
            oi.initial_object_id=82 and
            oi.destroyed_building_percent > 0.1 and oi.destroyed_building_percent < 1.0 and oi.building_completed is null
    """
    return query, dict()


def deer_pushes():
    """Find successfully hunt that was successfully pushed to town center."""
    query = """
        select players.match_id, players.number, destroyed::interval(0) as timestamp
        from object_instances join matches on object_instances.match_id=matches.id
        join players on matches.id=players.match_id
        where
            initial_class_id = 70 and
            initial_object_id = any(:hunt_ids) and
            destroyed_by_instance_id > 0 and
            sqrt(power(players.start_x-destroyed_x, 2) + power(players.start_y-destroyed_y, 2)) < 7
    """
    return query, dict(hunt_ids=HUNT_IDS)


def scout_war():
    """Find players that won a scout war (starting scout kills opponent's starting scout)."""
    query = """
        with subquery as (
            select instance_id, initial_player_number, match_id, destroyed_by_instance_id, destroyed
            from object_instances
            where initial_class_id=70 and initial_object_id=any(:scout_ids) and created < '00:00:10'
        )
        select opp.match_id, opp.initial_player_number as number, x.destroyed::interval(0) as timestamp
        from subquery as x join subquery as opp on x.destroyed_by_instance_id=opp.instance_id and x.match_id=opp.match_id
    """
    return query, dict(scout_ids=SCOUT_IDS)


def bad_lure():
    """Find bad boar lures (when the boar is not killed under town center."""
    query = """
        select players.match_id, players.number, oi.destroyed::interval(0) as timestamp
        from object_instances as oi join players on players.match_id=oi.match_id
        where
            oi.initial_class_id=70 and initial_object_id = any(:boar_ids) and
            sqrt(power(oi.destroyed_x-players.start_x, 2) + power(oi.destroyed_y-players.start_y,2)) < 5 and
            ((players.start_x-oi.destroyed_x) > 2 or (oi.destroyed_y - players.start_y) > 2)
    """
    return query, dict(boar_ids=BOAR_IDS)


def lost_techs():
    """Find research that was canceled due to the building being destroyed."""
    query = """
        select ois.match_id, ois.player_number as number, destroyed::interval(0) as timestamp, technologies.name as value
        from object_instance_states as ois join
        (
            select max(object_instance_states.id) as id, match_id, instance_id
            from object_instance_states join ({sq}) as sq on match_id=sq.id
            where class_id=80
            group by instance_id, match_id
        ) as s on ois.id=s.id and ois.match_id=s.match_id
        join object_instances as oi on ois.instance_id=oi.instance_id and oi.match_id=ois.match_id
        join technologies on ois.researching_technology_id=technologies.id and ois.dataset_id=technologies.dataset_id
        where oi.destroyed is not null and ois.researching_technology_id > 0
    """
    return query, dict()


def fast_castle():
    """Did a fast-castle occur."""
    query = """
        select
            x.match_id, x.player_number as number,
            finished as feudal_time, castle.started::interval(0) as timestamp, castle.started - finished as delay
        from research as x
        join (
            select match_id, player_number, started from research where technology_id=102
        ) as castle on castle.match_id=x.match_id and castle.player_number=x.player_number
        where technology_id=101 and (castle.started - finished) < '00:01:30'
    """
    return query, dict()


def research_order(technology_id, after_technology_id, civ_ids):
    """Report research that began after a specified research finished."""
    query = """
        select
            imp.match_id, imp.player_number as number, imp.finished as imp_time, late.started::interval(0) as timestamp
        from research as imp
        join players on imp.match_id=players.match_id and imp.player_number=players.number
        left join (
            select match_id, player_number, started, finished from research
            where technology_id=:technology_id
        ) as late on late.match_id=imp.match_id and imp.player_number=late.player_number
        where imp.technology_id=:after_technology_id and imp.finished is not null and late.finished is null and not (players.civilization_id = any(:civ_ids))
    """
    return query, dict(technology_id=technology_id, after_technology_id=after_technology_id, civ_ids=civ_ids)


def trained_unit(object_ids, before_tech):
    """Returns matches where only *1* of the object ids is played prior to before_tech."""
    query = """
        select oi.match_id, oi.initial_player_number as number, (case when count(distinct initial_object_id) = 1 then true else false end) as value
        from object_instances as oi join ({sq}) as sq on oi.match_id=sq.id
        where initial_class_id=70 and initial_object_id=any(:object_ids) and created > '00:01:00'
        and created < (select finished from research where match_id=oi.match_id and player_number=oi.initial_player_number and technology_id=:before_tech)
        group by oi.match_id, oi.initial_player_number
        having (case when count(distinct initial_object_id) = 1 then true else false end)=true
    """
    return (
        query,
        dict(object_ids=object_ids, before_tech=before_tech)
    )


def formation_uses(formation_id):
    query = """
        select players.match_id, players.number, count(formations.formation_id) as value
        from players left join formations on players.match_id=formations.match_id and players.number=formations.player_number and formations.formation_id=:formation_id
        group by players.match_id, players.number
    """
    return query, dict(formation_id=formation_id)


def maa():
    query = """
        select oi.match_id, oi.initial_player_number as number, case when count(*) > 0 then true else false end as value
        from object_instances as oi join ({sq}) as sq on oi.match_id=sq.id
        join research as maa on oi.match_id=maa.match_id and oi.initial_player_number=maa.player_number and maa.technology_id=222
        left join research as castle on oi.match_id=castle.match_id and oi.initial_player_number=castle.player_number and castle.technology_id=102
        where initial_class_id=70 and initial_object_id in(74, 75) and created > '00:01:00' and maa.started < castle.started and created < castle.started
group by oi.match_id, oi.initial_player_number
    """
    return query, dict()


def drush():
    query = """
        select oi.match_id, oi.initial_player_number as number, case when count(*) > 0 then true else false end as value
        from object_instances as oi join ({sq}) as sq on oi.match_id=sq.id
        left join research as maa on oi.match_id=maa.match_id and oi.initial_player_number=maa.player_number and maa.technology_id=222
        left join research as castle on oi.match_id=castle.match_id and oi.initial_player_number=castle.player_number and castle.technology_id=102
        where initial_class_id=70 and initial_object_id in(74) and created > '00:01:00' and (maa.started is null or maa.started > castle.started) and created < castle.started
group by oi.match_id, oi.initial_player_number
    """
    return query, dict()


def badaboom():
    """Returns splash damage attacks that kill more than 5 units."""
    query = """
        select
            mangos.match_id, mangos.initial_player_number as number, oi.destroyed::interval(0) as timestamp,
            objects.name || ' kills ' || count(distinct oi.instance_id) as value
        from object_instances as mangos
        join object_instances as oi on mangos.instance_id=oi.destroyed_by_instance_id and mangos.match_id=oi.match_id
        join ({sq}) as sq on mangos.match_id=sq.id
        join objects on mangos.initial_object_id=objects.id and mangos.dataset_id=objects.dataset_id
        where mangos.initial_object_id = any(:splash_damage_ids) and oi.initial_class_id=70 and oi.destroyed is not null
        group by mangos.match_id, mangos.initial_player_number, oi.destroyed, mangos.instance_id, objects.name
        having count(distinct oi.instance_id) >= 5
    """
    return query, dict(splash_damage_ids=SPLASH_DAMAGE_IDS)


def castle_race():
    """Report winner when two castles are placed at the same time in the same place. Loser deletes."""
    query = """
        with subquery as (
            select match_id, initial_player_number as number, created, created_x, created_y, deleted, destroyed
            from object_instances as oi
            where initial_object_id=82
        )
        select distinct p1.match_id, p1.number, p2.destroyed::interval(0) as timestamp
        from subquery as p1 join subquery as p2 on
            p1.match_id=p2.match_id and
            p1.number != p2.number and
            sqrt(power(p1.created_x-p2.created_x, 2) + power(p1.created_y-p2.created_y, 2)) < 10 and
            (p1.created-p2.created < '00:01:00' and p1.created-p2.created > '00:00:00' or
            p2.created-p1.created < '00:01:00' and p2.created-p1.created > '00:00:00') and
            p1.deleted = false and p2.deleted = true
    """
    return query, dict()


def market_usage():
    """Buying and selling resources at the market."""
    query = """
        select
            players.match_id, timestamp::interval(0),
            player_number as number,
            case when action_id=123 then 'Gold' else resources.name end as sold_resource,
            (amount * 100) as sold_amount,
            case when action_id=123 then resources.name else 'Gold' end as bought_resource
        from players left join transactions on transactions.match_id=players.match_id and transactions.player_number = players.number
        join resources on transactions.resource_id=resources.id
    """
    return query, dict()


def scout_lost_to_tc(before_age):
    """Scout lost to opponent's TC."""
    query = """
        select scout.match_id, scout.initial_player_number as number, scout.destroyed::interval(0) as timestamp, research.finished as reached_castle
        from object_instances as scout
        join object_instances as tc on scout.destroyed_by_instance_id=tc.instance_id and scout.match_id=tc.match_id and scout.initial_player_number <> tc.initial_player_number
        left join research on research.match_id=scout.match_id and research.player_number=scout.initial_player_number
        where scout.initial_object_id = any(:scout_ids) and scout.created < '00:00:10' and tc.initial_object_id = any(:tc_ids) and tc.created < '00:00:10'
        and research.technology_id = :before_age
        and scout.destroyed < research.finished
    """
    return query, dict(scout_ids=SCOUT_IDS, tc_ids=TC_IDS, before_age=before_age)


def gaia_killed_by_tc(gaia_ids):
    """Gaia killed by TC."""
    query = """
        select tc.match_id, tc.initial_player_number as number, boar.destroyed::interval(0) as timestamp
        from object_instances as boar
        join object_instances as tc on boar.destroyed_by_instance_id=tc.instance_id and boar.match_id=tc.match_id
        where boar.initial_object_id = any(:gaia_ids) and tc.initial_object_id = any(:tc_ids) and tc.created < '00:00:10'
    """
    return query, dict(gaia_ids=gaia_ids, tc_ids=TC_IDS)
