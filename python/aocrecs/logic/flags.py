"""Compute flagged events."""
from aocrecs.consts import VILLAGER_IDS, BOAR_IDS, HUNT_IDS, SCOUT_IDS, SPLASH_DAMAGE_IDS


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
            players.match_id, players.number, destroyed_building_percent as deleted_at_percent, destroyed::interval(0) as timestamp
        from object_instances as oi join players on oi.match_id=players.match_id and oi.initial_player_number=players.number
        where
            oi.initial_object_id=82 and
            oi.deleted is true and oi.destroyed_building_percent > 0.1
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


def research_order(technology_id, after_technology_id):
    """Report research that began after a specified research finished."""
    query = """
        select x.match_id, x.player_number as number, started::interval(0) as timestamp, imp.finished as imp_time
        from research as x
        join (
            select match_id, player_number, finished from research
            where technology_id=:after_technology_id
        ) as imp on imp.match_id=x.match_id and imp.player_number=x.player_number
        where technology_id=:technology_id and started > imp.finished
    """
    return query, dict(technology_id=technology_id, after_technology_id=after_technology_id)


def trained_unit(object_ids, before_tech):
    """Returns matches where only *1* of the object ids is played prior to before_tech."""
    query = """
        select oi.match_id, oi.initial_player_number as number, (case when count(distinct initial_object_id) = 1 then true else false end) as val
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
        select match_id, player_number as number, timestamp::interval(0), actions.name as value
        from ({sq}) as m join transactions on m.id=transactions.match_id join actions on transactions.action_id=actions.id
    """
    return query, dict()
