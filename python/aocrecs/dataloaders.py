"""Dataloaders."""
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


class Loaders:
    """ContextLoader factory."""

    def __init__(self):
        """Initialize."""
        self.funcs = {}

    def __call__(self, context):
        """Setup.

        Call after registration is complete.
        """
        for name, func in self.funcs.items():
            setattr(self, name, ContextLoader(context, func))
        return self

    def register(self, name):
        """Register an asynchronous resolver."""
        def decorator(func):
            """Wrap the function."""
            self.funcs[name] = func
        return decorator
