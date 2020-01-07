"""GraphQL Context."""

class Context: # pylint: disable=too-few-public-methods
    """Context.

    Convenience wrapper so that dot-notation can be used in resolvers.
    """

    def __init__(self, request, database, loaders):
        """Initialize context."""
        self.request = request
        self.database = database
        self.loaders = loaders(self)
