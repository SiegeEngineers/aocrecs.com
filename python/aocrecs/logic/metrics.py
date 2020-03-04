"""Compute player metrics."""
from aocrecs.consts import VILLAGER_IDS, TC_IDS


def housed():
    """Total time a player spent housed."""
    query = """
        select match_id, player_number as number, max(total_housed_time)::interval(0) as value
        from timeseries join ({sq}) as sq on timeseries.match_id=sq.id
        group by match_id, player_number
    """
    return query, dict()


def popcapped():
    """Total time a player spent population-capped."""
    query = """
        select match_id, player_number as number, max(total_popcapped_time)::interval(0) as value
        from timeseries join ({sq}) as sq on timeseries.match_id=sq.id
        group by match_id, player_number
    """
    return query, dict()


def villagers_idle():
    """Total time villagers spent idle."""
    query = """
        select oi.match_id, oi.initial_player_number as number, sum(oi.total_idle_time)::interval(0) as value
        from object_instances as oi join ({sq}) as sq on oi.match_id=sq.id
        where initial_object_id = any(:villager_ids) and oi.total_idle_time is not null
        group by oi.match_id, oi.initial_player_number
    """
    return query, dict(villager_ids=VILLAGER_IDS)


def tc_idle():
    """Total time town center spent idle in Dark Age."""
    query = """
        select match_id, player_number as number, (extract(\'epoch\' from started)::int % 25) * interval '1 sec' as value
        from research
        where research.technology_id=101
    """
    return query, dict()


def tc_count():
    """Number of town centers a player completed, including any initial town centers."""
    query = """
        select oi.match_id, oi.initial_player_number as number, count(distinct instance_id) as value
        from object_instances as oi
        where initial_object_id = any(:tc_ids) and (
            (building_started is not null and building_completed is not null) or
            created < '00:01:00'
        )
        group by oi.match_id, oi.initial_player_number
    """
    return query, dict(tc_ids=TC_IDS)


def floating():
    """Average amount of floating resources (sum of all four types)."""
    query = """
        select match_id, player_number as number, round(avg(food+wood+stone+gold), 0) as value
        from timeseries join ({sq}) as sq on timeseries.match_id=sq.id
        group by match_id, player_number
    """
    return query, dict()


def apm():
    """Average actions per (game time-)minute."""
    query = """
        select match_id, player_number as number, round(count(*)/(extract('epoch' from max(duration))/60)) as value
        from action_log join matches on action_log.match_id=matches.id
        group by match_id, player_number
    """
    return query, dict()
