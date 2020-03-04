"""Caching."""
from collections import defaultdict

import asyncio
import logging
from aiocache import cached as aio_cached, multi_cached


LOGGER = logging.getLogger(__name__)
CACHEABLE_TYPES = [int, str, dict, list, tuple, defaultdict]
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

    def __init__(self, warm=False, **kwargs):
        """Initialize."""
        if 'ttl' not in kwargs:
            kwargs['ttl'] = DEFAULT_TTL
        self.warm = warm
        self.ttl = kwargs['ttl']
        aio_cached.__init__(self, key_builder=key_builder, **kwargs)

    def __call__(self, func):
        """Register with cache warmer if requested."""
        wrapped = aio_cached.__call__(self, func)
        if self.warm:
            CacheWarmer.register(wrapped, self.ttl, self.warm)
        return wrapped


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


class Warmer:
    """Schedule period cache warming based on TTL."""

    def __init__(self):
        """Initialize registry."""
        self._disable = False
        self._database = None
        self._registry = {}
        self._tasks = []

    def __call__(self, database, disable=False):
        """Set database."""
        self._database = database
        self._disable = disable
        return self

    def register(self, func, interval, args):
        """Register a function with interval."""
        if interval:
            LOGGER.info("registering %s to warm every %d minutes", func_name(func), interval/60)
        else:
            LOGGER.info("registering %s to warm once", func_name(func))
        self._registry[func] = dict(interval=interval, args=args)

    async def schedule(self, func, data):
        """Schedule a function with interval."""
        while True:
            if not isinstance(data['args'], list):
                data['args'] = [[]]
            for arg in data['args']:
                LOGGER.info("warming cache for %s", key_builder(func, *arg))
                await func(self._database, *arg)
            if data['interval']:
                await asyncio.sleep(data['interval'])
            else:
                break

    async def setup(self):
        """Connect database and schedule registry."""
        if not self._database:
            raise RuntimeError('call with database prior to setup')
        await self._database.connect()
        if self._disable:
            LOGGER.info("cache warming is disabled")
            return
        for func, data in self._registry.items():
            self._tasks.append(asyncio.get_event_loop().create_task(self.schedule(func, data)))

    async def teardown(self):
        """Cancel scheduled tasks and stop and disconnect database."""
        for task in self._tasks:
            task.cancel()
        LOGGER.info("canceled warming tasks")
        await self._database.disconnect()


CacheWarmer = Warmer() # pylint: disable=invalid-name
