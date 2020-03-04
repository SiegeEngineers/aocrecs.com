"""Utilities."""
from collections import defaultdict


def by_key(results, keys, defaults=None):
    """Group rows by specified key."""
    if not isinstance(keys, tuple):
        keys = (keys,)
    output = defaultdict(list)
    if defaults:
        for key in defaults:
            output[key] = []
    for row in results:
        key = list(row[k] for k in keys)
        if len(key) == 1:
            key = key[0]
        else:
            key = tuple(key)
        output[key].append(dict(row))
    return output


def compound_where(keys, fields):
    """Create a filter on compound keys."""
    args = {}
    ors = []
    for i, key in enumerate(keys):
        ands = []
        for field, value in zip(fields, key):
            bind_name = '{}_{}'.format(field.replace('.', '_'), i)
            ands.append('{} = :{}'.format(field, bind_name))
            args[bind_name] = value
        ors.append(ands)
    return ' or '.join([' and '.join(a) for a in ors]), args
