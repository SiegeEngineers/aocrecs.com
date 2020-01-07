"""Caching."""
from collections import defaultdict

from aiocache import cached as aio_cached, multi_cached


CACHEABLE_TYPES = [int, str, dict, list, defaultdict]
DEFAULT_TTL = 60


def func_name(func):
    """Get a readable name."""
    return '.'.join([func.__module__ or "", func.__name__])


def key_builder(func, *args, **kwargs):
    """Build cache key."""
    return ''.join([
        func_name(func),
        str([arg for arg in args if type(arg) in CACHEABLE_TYPES]), # pylint: disable=unidiomatic-typecheck
        str(sorted(kwargs.items()))
    ])


class cached(aio_cached): # pylint: disable=invalid-name
    """Cache decorator with useful defaults."""

    def __init__(self, **kwargs):
        """Initialize."""
        if 'ttl' not in kwargs:
            kwargs['ttl'] = DEFAULT_TTL
        aio_cached.__init__(self, key_builder=key_builder, **kwargs)


class dataloader_cached(multi_cached): # pylint: disable=invalid-name
    """Multi-cache decorator with useful defaults."""

    def __init__(self, **kwargs):
        """Initialize."""
        if 'ttl' not in kwargs:
            kwargs['ttl'] = DEFAULT_TTL
        multi_cached.__init__(self, keys_from_attr='keys', **kwargs)

    def __call__(self, func):
        """Set namespace based on function name before calling."""
        self._kwargs['namespace'] = func_name(func)
        return multi_cached.__call__(self, func)
