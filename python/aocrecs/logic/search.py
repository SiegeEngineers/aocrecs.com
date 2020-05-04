"""Build search query."""
import asyncio
from datetime import datetime
from aocrecs.cache import cached
from aocrecs.logic import matches
from aocrecs.logic.playback import FLAGS


SEARCH_LIMIT = 10
LATEST_DATASETS = [0, 1, 100]


@cached(warm=True, ttl=3600)
async def latest_summary(database):
    latest = []
    query = """
        select dataset_id, datasets.name, datasets.short, max(dataset_version) as version
        from matches join datasets on datasets.id=dataset_id
        where dataset_id = any(:dataset_ids)
        group by dataset_id, datasets.name, datasets.short
    """
    datasets = await database.fetch_all(query, values=dict(dataset_ids=LATEST_DATASETS))
    for dataset in datasets:
        params = {'matches': {
            'dataset_id': {'values': [dataset['dataset_id']]},
            'dataset_version': {'values': [dataset['version']]}
        }}
        _, count_query, values = build_query(params, 0, 0)
        latest.append(database.fetch_one(count_query, values=values))
    output = []
    for dataset, hits in zip(datasets, await asyncio.gather(*latest)):
        version = dataset['version']
        if dataset['short'] == 'de':
            version = version.split('.')[2]
        output.append(dict(
            dataset=dict(
                name=dataset['name'],
                id=dataset['dataset_id']
            ),
            count=hits['count'],
            version=version
        ))
    return output


#@cached(warm=[[0, 0, 8], [1, 0, 8], [100, 0, 8]], ttl=3600)
async def latest(context, dataset_id, offset, limit):
    query = "select max(dataset_version) as version from matches where dataset_id=:dataset_id"
    result = await context.database.fetch_one(query, values=dict(dataset_id=dataset_id))
    params = {'matches': {
        'dataset_id': {'values': [dataset_id]},
        'dataset_version': {'values': [result['version']]}
    }}
    return await get_hits(context, params, offset, limit)


async def get_hits(context, params, offset, limit):
    """Return hits: count and paginated matches."""
    count, result = await _cached_get_hits(context.database, params, offset, limit)
    return dict(count=count['count'], hits=await context.load_many(matches.get_match, map(lambda m: m['id'], result)))


@cached()
async def _cached_get_hits(database, params, offset, limit):
    """Cacheable hits."""
    if limit > SEARCH_LIMIT:
        limit = SEARCH_LIMIT
    result_query, count_query, values = build_query(params, offset, limit)
    return await asyncio.gather(
        database.fetch_one(count_query, values=values),
        database.fetch_all(result_query, values=values)
    )


def add_filter(field, bind, criteria):
    """Generate a filter."""
    if 'values' in criteria:
        return '{0}=any(:{1})'.format(field, bind), criteria['values']
    if 'date' in criteria:
        return '{0}::date=:{1}'.format(field, bind), datetime.strptime(criteria['date'], '%Y-%m-%d').date()
    if 'gte' in criteria:
        return '{0}>=:{1}'.format(field, bind), criteria['gte']
    if 'lte' in criteria:
        return '{0}<=:{1}'.format(field, bind), criteria['lte']
    raise ValueError('criteria not supported')


def build_query(params, offset, limit):
    """Build search query."""
    join = []
    where = []
    args = {}
    for table in ['players', 'files', 'matches']:
        if table != 'matches' and table in params.keys() and params[table]:
            join.append('{0} on {0}.match_id=matches.id'.format(table))

        for field, criteria in params.get(table, {}).items():
            path = '{}.{}'.format(table, field)
            bind_name = path.replace('.', '_')
            where_clause, bind_value = add_filter(path, bind_name, criteria)
            where.append(where_clause)
            args[bind_name] = bind_value

    query = 'from matches {} {}'.format('join' if join else '', ' join '.join(join)) + ' {playback}'
    if where:
        query += ' where {}'.format(' and '.join(where))

    query = append_flags(query, params, args)

    query_template = "select distinct matches.id, matches.played {} order by matches.played desc nulls last limit {} offset {}"
    return query_template.format(query, limit, offset), 'select count(distinct matches.id) {}'.format(query), args


def append_flags(query, params, args):
    """Append flag logic."""
    joins = []
    for alias, _, _, (subquery, values) in FLAGS:
        if alias not in params.get('flags', {}).keys():
            continue

        if '{sq}' in subquery:
            subquery = subquery.format(sq='select distinct matches.id {}'.format(query.format(playback='')))

        new_args = {}
        for key, value in values.items():
            subquery = subquery.replace(':{}'.format(key), ':{}_{}'.format(alias, key))
            new_args['{}_{}'.format(alias, key)] = value

        args.update(new_args)
        joins.append('({subquery}) as {alias} on {alias}.match_id = matches.id'.format(subquery=subquery, alias=alias))

    if joins:
        return query.format(playback='join ' + ' join '.join(joins))
    return query.format(playback='')
