"""GraphQL resolvers."""
from ariadne import QueryType, ObjectType, make_executable_schema, ScalarType, upload_scalar, MutationType

from aocrecs.dataloaders import Loaders
from aocrecs.logic import (
    search, metaladder, report, search_options, events,
    matches, stats as stat, maps, civilizations, users, odds
)
from aocrecs.schema import TYPE_DEFS
from aocrecs.upload import add_rec

# Unhelpful rules for resolver boilerplate.
# pylint: disable=unused-argument, missing-function-docstring, invalid-name, redefined-builtin


loaders = Loaders()
datetime_ = ScalarType('Datetime')
dict_ = ScalarType('Dict')


@datetime_.serializer
def serialize_datetime(value):
    """Serialize a datetime value."""
    return str(value)


query = QueryType()
mutation = MutationType()
map_ = ObjectType('Map')
civilization = ObjectType('Civilization')
stats = ObjectType('Stats')
match = ObjectType('Match')
player = ObjectType('Player')
research = ObjectType('Research')
chat = ObjectType('Chat')
team = ObjectType('Team')
file_ = ObjectType('File')
hits = ObjectType('Hits')
event = ObjectType('Event')
tournament = ObjectType('Tournament')
series = ObjectType('Series')
side = ObjectType('Side')
meta_ladder = ObjectType('Ladder')
user = ObjectType('User')
rank = ObjectType('Rank')
search_options_ = ObjectType('SearchOptions')
search_result = ObjectType('SearchResult')
report_ = ObjectType('Report')
stat_user = ObjectType('StatUser')
person = ObjectType('Person')


@query.field('reports')
async def resolve_reports(obj, info):
    return report.available_reports()


@report_.field('rankings')
async def resolve_report_rankings(obj, info, platform_id, ladder_id, limit):
    return await report.rankings(info.context.database, platform_id, ladder_id, obj['year'], obj['month'], limit)


@report_.field('most_improvement')
async def resolve_report_most_improvement(obj, info, platform_id, ladder_id, limit):
    return await report.most_improvement(
        info.context.database, platform_id, ladder_id, obj['year'], obj['month'], limit
    )


@query.field('report')
async def resolve_report(obj, info, year, month, platform_id, limit): # pylint: disable=too-many-arguments
    return await report.report(info.context.database, platform_id, year, month, limit)


@report_.field('longest_matches')
async def resolve_longest_matches(obj, info):
    return await info.context.loaders.match.load_many(obj['longest_match_ids'])


@query.field('search_options')
async def resolve_search_options(obj, info):
    return {}


@search_options_.field('civilizations')
async def resolve_search_options_civilizations(obj, info, dataset_id):
    return await search_options.civilizations(info.context.database, dataset_id)


@search_options_.field('ladders')
async def resolve_search_options_ladders(obj, info, platform_id):
    return await search_options.ladders(info.context.database, platform_id)


@search_options_.field('general')
async def resolve_search_options_general(obj, info):
    return await search_options.general(info.context.database)


@query.field('user')
async def resolve_user(obj, info, id, platform_id):
    return await users.get_user(info.context.database, id, platform_id)


@user.field('top_map')
async def resolve_top_map(obj, info):
    return await users.get_top_map(info.context.database, obj['id'], obj['platform_id'])


@user.field('top_civilization')
async def resolve_top_civilization(obj, info):
    return await users.get_top_civilization(info.context.database, obj['id'], obj['platform_id'])


@user.field('top_dataset')
async def resolve_top_dataset(obj, info):
    return await users.get_top_dataset(info.context.database, obj['id'], obj['platform_id'])


@user.field('matches')
async def resolve_user_matches(obj, info, offset, limit):
    params = {'players': {'user_id': {'values': [obj['id']]}}}
    return await search.get_hits(info.context, params, offset, limit)


@user.field('meta_ranks')
async def resolve_meta_ranks(obj, info, ladder_ids):
    return await metaladder.get_meta_ranks(info.context.database, obj['id'], obj['platform_id'], ladder_ids)


@query.field('people')
async def resolve_people(obj, info):
    return await users.get_people(info.context.database)


@query.field('person')
async def resolve_person(obj, info, id):
    return await users.get_person(info.context.database, id)


@query.field('meta_ladders')
async def resolve_meta_ladders(obj, info, platform_id, ladder_ids):
    return await metaladder.get_ladders(info.context.database, platform_id, ladder_ids)


@rank.field('streak')
async def resolve_streak(obj, info):
    return await metaladder.get_streak(
        info.context.database, obj['user']['id'], obj['user']['platform_id'], obj['ladder']['id']
    )


@rank.field('rate_by_day')
async def resolve_rate_by_day(obj, info):
    return await metaladder.get_rate_by_day(
        info.context.database, obj['user']['id'], obj['user']['platform_id'], obj['ladder']['id']
    )


@meta_ladder.field('ranks')
async def resolve_ranks(obj, info, limit):
    return await metaladder.get_ranks(info.context.database, obj['platform_id'], obj['id'], limit)


@series.field('matches')
async def resolve_series_matches(obj, info, offset, limit):
    params = {'matches': {'id': {'values': obj['match_ids']}}}
    return await search.get_hits(info.context, params, offset, limit)


@series.field('sides')
async def resolve_sides(obj, info):
    return events.get_sides(await info.context.loaders.match.load_many(obj['match_ids']), obj['participants'])


@query.field('series')
async def resolve_series(obj, info, id):
    return await events.get_series(info.context.database, id)


@query.field('events')
async def resolve_events(obj, info):
    return await events.get_events(info.context.database)


@query.field('event')
async def resolve_event(obj, info, id):
    return await events.get_event(info.context.database, id)


@query.field('search')
async def resolve_search(obj, info):
    return {}


@search_result.field('matches')
async def resolve_search_matches(obj, info, params, offset, limit):
    return await search.get_hits(info.context, params, offset, limit)


@civilization.field('matches')
async def resolve_civilization_matches(obj, info, offset, limit):
    params = {'players': {'civilization_id': {'values': [obj['id']]}, 'dataset_id': {'values': [obj['dataset_id']]}}}
    return await search.get_hits(info.context, params, offset, limit)


@map_.field('matches')
async def resolve_map_matches(obj, info, offset, limit):
    params = {'matches': {'map_name': {'values': [obj['name']]}}}
    return await search.get_hits(info.context, params, offset, limit)


@map_.field('top_civilizations')
async def resolve_map_top_civilizations(obj, info, limit):
    return await maps.get_top_civilizations(info.context.database, obj['name'], limit)


@map_.field('preview_url')
async def resolve_preview_url(obj, info):
    return await maps.get_preview_url(info.context, obj['name'])


@loaders.register('map_events')
def load_map_events(keys, context):
    return maps.get_map_events(keys, context)


@match.field('map_events')
async def resolve_match_map_events(obj, info):
    return await info.context.loaders.map_events.load(obj['map_name'])


@loaders.register('match')
def load_match(keys, context):
    return matches.get_match(keys, context)


@query.field('match')
async def resolve_match(obj, info, id):
    return await info.context.loaders.match.load(id)


@match.field('odds')
async def resolve_odds(obj, info):
    return await odds.get_odds(info.context.database, obj)


@match.field('chat')
async def resolve_chat(obj, info):
    return await matches.get_chat(info.context.database, obj['id'])


@loaders.register('research_by_player')
def load_research_by_player(keys, context):
    return matches.get_research_by_player(keys, context.database)


@player.field('research')
async def resolve_research(obj, info):
    return await info.context.loaders.research_by_player.load((obj['match_id'], obj['number']))


@query.field('map')
async def resolve_map(obj, info, name):
    return dict(name=name)


@query.field('maps')
async def resolve_maps(obj, info):
    return await maps.get_maps(info.context.database)


@query.field('civilization')
async def resolve_civilization(obj, info, id, dataset_id):
    return await civilizations.get_civilization(info.context.database, id, dataset_id)


@query.field('civilizations')
async def resolve_civilizations(obj, info, dataset_id):
    return await civilizations.get_all_civilizations(info.context.database, dataset_id)


@query.field('stats')
async def resolve_stats(obj, info):
    return await stat.summary(info.context.database)


@stats.field('map_count')
async def resolve_map_count(obj, info):
    return await stat.map_count(info.context.database)


@stats.field('datasets')
async def resolve_datasets(obj, info):
    return await stat.rel_agg_query(info.context.database, 'datasets', 'dataset_id')


@stats.field('platforms')
async def resolve_platforms(obj, info):
    return await stat.rel_agg_query(info.context.database, 'platforms', 'platform_id')


@stats.field('diplomacy')
async def resolve_diplomacy(obj, info):
    return await stat.agg_query(info.context.database, 'matches', 'diplomacy_type')


@stats.field('languages')
async def resolve_languages(obj, info):
    return await stat.agg_query(info.context.database, 'files', 'language')


@stats.field('types')
async def resolve_types(obj, info):
    return await stat.rel_agg_query(info.context.database, 'game_types', 'type_id')


@stats.field('by_day')
async def resolve_by_day(obj, info):
    return await stat.by_day(info.context.database)


@person.field('matches')
async def resolve_person_matches(obj, info, offset, limit):
    params = {'players': {'user_id': {'values': [a['id'] for a in obj['accounts']]}}}
    return await search.get_hits(info.context, params, offset, limit)


@mutation.field('upload')
async def resolve_upload(obj, info, rec_file):
    return add_rec(
        rec_file.filename,
        await rec_file.read(),
        str(info.context.request.app.state.database_url),
        info.context.request.app.state.voobly_username,
        str(info.context.request.app.state.voobly_password)
    )


SCHEMA = make_executable_schema(TYPE_DEFS, [
    query, map_, stats, datetime_, research, player, chat, match,
    team, file_, hits, side, series, civilization, event, meta_ladder,
    user, rank, search_options_, stat_user, report_, search_result,
    person, upload_scalar, mutation
])
