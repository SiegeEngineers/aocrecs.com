"""GraphQL Context."""

from aiodataloader import DataLoader


class ContextLoader(DataLoader):
    """Dataloader that provides GraphQL context."""

    def __init__(self, context, func):
        """Create an instance."""
        super(ContextLoader, self).__init__()
        self.context = context
        self.func = func

    async def batch_load_fn(self, keys): # pylint: disable=method-hidden
        """Call batch function and sort output."""
        results = await self.func(keys, self.context)
        return [results.get(ref) for ref in keys]


class Context:
    """Context."""

    def __init__(self, request, database):
        """Initialize context."""
        self.request = request
        self.database = database
        self._funcs = {}

    def register(self, func):
        """Register a dataloader."""
        if func.__name__ not in self._funcs:
            self._funcs[func.__name__] = ContextLoader(self, func)

    def load(self, func, key):
        """Proxy `load` function."""
        self.register(func)
        return self._funcs[func.__name__].load(key)

    def load_many(self, func, keys):
        """Proxy `load_many` function."""
        self.register(func)
        return self._funcs[func.__name__].load_many(keys)
