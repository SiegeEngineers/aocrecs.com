"""aocrecs.com Application."""
import coloredlogs
import databases

from ariadne.asgi import GraphQL
from ariadne.contrib.tracing.apollotracing import ApolloTracingExtension
from starlette.applications import Starlette
from starlette.config import Config
from starlette.datastructures import URL
from starlette.middleware import Middleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.routing import Route

from aocrecs import resolvers, routes as aoc_routes
from aocrecs.context import Context


config = Config('./.env') # pylint: disable=invalid-name
DATABASE_URL = config('DATABASE_URL', cast=URL)
DEBUG = config('DEBUG', cast=bool, default=False)


def new_app():
    """Create a new app instance."""
    coloredlogs.install(level='DEBUG' if DEBUG else 'INFO', fmt='%(asctime)s %(name)s %(levelname)s %(message)s')
    database = databases.Database(DATABASE_URL)
    routes = [
        Route('/api', GraphQL(
            resolvers.SCHEMA,
            debug=DEBUG,
            context_value=lambda request: Context(request, database, resolvers.loaders),
            extensions=[ApolloTracingExtension]
        ), name='api'),
        Route('/api/download/{file_id:int}', aoc_routes.download, name='download'),
        Route('/api/map/{match_id:int}', aoc_routes.svg_map, name='minimap')
    ]

    middleware = [
        Middleware(GZipMiddleware),
        Middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])
    ]

    app = Starlette(
        debug=DEBUG,
        routes=routes,
        middleware=middleware,
        on_startup=[database.connect],
        on_shutdown=[database.disconnect]
    )
    app.state.database = database
    return app


APP = new_app()
