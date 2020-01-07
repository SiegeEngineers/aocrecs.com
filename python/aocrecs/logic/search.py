"""Build search query."""
import asyncio
from aocrecs.cache import cached


@cached()
async def get_hits(context, params, offset, limit):
    """Return hits: count and paginated matches."""
    result_query, count_query, values = build_query(params, offset, limit)
    count, result = await asyncio.gather(
        context.database.fetch_one(count_query, values=values),
        context.database.fetch_all(result_query, values=values)
    )
    return dict(count=count['count'], hits=await context.loaders.match.load_many(map(lambda m: m['id'], result)))


def add_filter(field, bind, criteria):
    """Generate a filter."""
    if 'values' in criteria:
        return '{0}=any(:{1})'.format(field, bind), criteria['values']
    if 'date' in criteria:
        return '{0}::date=:{1}'.format(field, bind), criteria['date']
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

    query = 'from matches {} {}'.format('join' if join else '', ' join '.join(join))
    if where:
        query += ' where {}'.format(' and '.join(where))

    query_template = "select distinct matches.id {} order by matches.id desc limit {} offset {}"
    return query_template.format(query, limit, offset), 'select count(distinct matches.id) {}'.format(query), args
