"""Match searches."""
import logging

from sqlalchemy import func

from mgzdb import schema


LOGGER = logging.getLogger(__name__)


def add_filter(query, table, field, criteria):
    """Add a filter."""
    if 'values' in criteria:
        if not isinstance(criteria['values'], list):
            criteria['values'] = [criteria['values']]

        return query.filter(getattr(table, field).in_(criteria['values']))

    if 'date' in criteria:
        return query.filter(func.date(getattr(table, field)) == criteria['date'])

    if 'gte' in criteria:
        return query.filter(getattr(table, field) >= criteria['gte'])

    if 'lte' in criteria:
        return query.filter(getattr(table, field) <= criteria['lte'])

    return query


def execute(match_query, params):
    """Run a query for matches with the given parameters."""
    if 'player' in params:
        match_query = match_query.join(schema.Player)
        for field, criteria in params['player'].items():
            match_query = add_filter(match_query, schema.Player, field, criteria)

    if 'file' in params:
        match_query = match_query.join(schema.File, schema.File.match_id == schema.Match.id)
        for field, criteria in params['file'].items():
            match_query = add_filter(match_query, schema.File, field, criteria)

    if 'match' in params:
        for field, criteria in params['match'].items():
            match_query = add_filter(match_query, schema.Match, field, criteria)

    return match_query
