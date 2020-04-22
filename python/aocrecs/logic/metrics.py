"""Compute player metrics."""
from aocrecs.consts import VILLAGER_IDS, TC_IDS


def housed():
    """Total time a player spent housed."""
    query = """
    select timeseries.match_id, timeseries.player_number as number, max(total_housed_time)::interval(0) as value,
	max(case when timestamp < (case when feudal.finished is not null then feudal.finished else duration end) then total_housed_time else null end) as dark_housed,
	max(case when timestamp >= feudal.finished and timestamp < (case when castle.finished is not null then castle.finished else duration end) then total_housed_time else null end) -
		max(case when timestamp < (case when feudal.finished is not null then feudal.finished else duration end) then total_housed_time else null end) as feudal_housed,
	max(case when timestamp >= castle.finished and timestamp < (case when imperial.finished is not null then imperial.finished else duration end) then total_housed_time else null end) -
		max(case when timestamp >= feudal.finished and timestamp < (case when castle.finished is not null then castle.finished else duration end) then total_housed_time else null end) as castle_housed,
	max(case when timestamp >= imperial.finished then total_housed_time else null end) -
		max(case when timestamp >= castle.finished and timestamp < (case when imperial.finished is not null then imperial.finished else duration end) then total_housed_time else null end) as imperial_housed
        from timeseries join ({sq}) as sq on timeseries.match_id=sq.id
        join matches on timeseries.match_id=matches.id
        left join research as feudal on feudal.match_id=timeseries.match_id and feudal.player_number=timeseries.player_number and feudal.technology_id=101
        left join research as castle on castle.match_id=timeseries.match_id and castle.player_number=timeseries.player_number and castle.technology_id=102
        left join research as imperial on imperial.match_id=timeseries.match_id and imperial.player_number=timeseries.player_number and imperial.technology_id=103
        group by timeseries.match_id, timeseries.player_number
    """
    return query, dict()


def popcapped():
    """Total time a player spent population-capped."""
    query = """
        select match_id, player_number as number, max(total_popcapped_time)::interval(0) as value, (
            select timestamp
            from timeseries as t
            where t.match_id=timeseries.match_id and t.player_number=timeseries.player_number and total_popcapped_time > '00:00:00'
            order by timestamp
            limit 1
        ) as first_popcapped
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


def floating_by_age():
    query = """
    select timeseries.match_id, timeseries.player_number as number, round(avg(food+wood+stone+gold), 0) as value,

	round(avg(case when timestamp < (case when feudal.finished is not null then feudal.finished else duration end) then food else null end), 0) as dark_food,
	round(avg(case when timestamp >= feudal.finished and timestamp < (case when castle.finished is not null then castle.finished else duration end) then food else null end), 0) as feudal_food,
	round(avg(case when timestamp >= castle.finished and timestamp < (case when imperial.finished is not null then imperial.finished else duration end) then food else null end), 0) as castle_food,
	round(avg(case when timestamp >= imperial.finished then food else null end), 0) as imperial_food,

	round(avg(case when timestamp < (case when feudal.finished is not null then feudal.finished else duration end) then wood else null end), 0) as dark_wood,
	round(avg(case when timestamp >= feudal.finished and timestamp < (case when castle.finished is not null then castle.finished else duration end) then wood else null end), 0) as feudal_wood,
	round(avg(case when timestamp >= castle.finished and timestamp < (case when imperial.finished is not null then imperial.finished else duration end) then wood else null end), 0) as castle_wood,
	round(avg(case when timestamp >= imperial.finished then wood else null end), 0) as imperial_wood,

	round(avg(case when timestamp < (case when feudal.finished is not null then feudal.finished else duration end) then stone else null end), 0) as dark_stone,
	round(avg(case when timestamp >= feudal.finished and timestamp < (case when castle.finished is not null then castle.finished else duration end) then stone else null end), 0) as feudal_stone,
	round(avg(case when timestamp >= castle.finished and timestamp < (case when imperial.finished is not null then imperial.finished else duration end) then stone else null end), 0) as castle_stone,
	round(avg(case when timestamp >= imperial.finished then stone else null end), 0) as imperial_stone,

	round(avg(case when timestamp < (case when feudal.finished is not null then feudal.finished else duration end) then gold else null end), 0) as dark_gold,
	round(avg(case when timestamp >= feudal.finished and timestamp < (case when castle.finished is not null then castle.finished else duration end) then gold else null end), 0) as feudal_gold,
	round(avg(case when timestamp >= castle.finished and timestamp < (case when imperial.finished is not null then imperial.finished else duration end) then gold else null end), 0) as castle_gold,
	round(avg(case when timestamp >= imperial.finished then gold else null end), 0) as imperial_gold

    from timeseries join ({sq}) as sq on timeseries.match_id=sq.id
    join matches on timeseries.match_id=matches.id

    left join research as feudal on feudal.match_id=timeseries.match_id and feudal.player_number=timeseries.player_number and feudal.technology_id=101
    left join research as castle on castle.match_id=timeseries.match_id and castle.player_number=timeseries.player_number and castle.technology_id=102
    left join research as imperial on imperial.match_id=timeseries.match_id and imperial.player_number=timeseries.player_number and imperial.technology_id=103
    group by timeseries.match_id, timeseries.player_number
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


def apm_by_age():
    query = """
    select action_log.match_id, action_log.player_number as number,
	round(count(*)/(extract('epoch' from max(duration))/60)) as value,
    round(count(
		case when timestamp < (case when feudal.finished is not null then feudal.finished else duration end) then true else null end)/max(extract('epoch' from (case when feudal.finished is not null then feudal.finished else duration end))/60
	)) as dark_apm,
	round(count(
		case when timestamp >= feudal.finished and timestamp < (case when castle.finished is not null then castle.finished else duration end) then true else null end)/max(extract('epoch' from (case when castle.finished is not null then castle.finished else duration end)-feudal.finished)/60
	)) as feudal_apm,
	round(count(
		case when timestamp >= castle.finished and timestamp < (case when imperial.finished is not null then imperial.finished else duration end) then true else null end)/max(extract('epoch' from (case when imperial.finished is not null then imperial.finished else duration end)-castle.finished)/60
	)) as castle_apm,
	round(count(
		case when timestamp >= imperial.finished then true else null end)/max(extract('epoch' from duration-imperial.finished)/60
	)) as imperial_apm
from action_log
join ({sq}) as sq on action_log.match_id=sq.id
join matches on action_log.match_id=matches.id
left join research as feudal on feudal.match_id=action_log.match_id and feudal.player_number=action_log.player_number and feudal.technology_id=101
left join research as castle on castle.match_id=action_log.match_id and castle.player_number=action_log.player_number and castle.technology_id=102
left join research as imperial on imperial.match_id=action_log.match_id and imperial.player_number=action_log.player_number and imperial.technology_id=103
group by action_log.match_id, action_log.player_number
    """
    return query, dict()
