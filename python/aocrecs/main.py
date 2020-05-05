"""aocrecs.com Application."""
import coloredlogs
import databases

from ariadne.asgi import GraphQL
from ariadne.contrib.tracing.apollotracing import ApolloTracingExtension
from starlette.applications import Starlette
from starlette.config import Config
from starlette.datastructures import Secret, URL
from starlette.middleware import Middleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.routing import Route, WebSocketRoute

from aocrecs import resolvers, routes as aoc_routes
from aocrecs.context import Context
from aocrecs.cache import CacheWarmer


config = Config('./.env') # pylint: disable=invalid-name
DATABASE_URL = config('DATABASE_URL', cast=URL)
VOOBLY_USERNAME = config('VOOBLY_USERNAME')
VOOBLY_PASSWORD = config('VOOBLY_PASSWORD', cast=Secret)
DEBUG = config('DEBUG', cast=bool, default=False)


def new_app():
    """Create a new app instance."""
    coloredlogs.install(level='DEBUG' if DEBUG else 'INFO', fmt='%(asctime)s %(name)s %(levelname)s %(message)s')
    database = databases.Database(DATABASE_URL)
    warmer = CacheWarmer(database, disable=DEBUG)
    graphql = GraphQL(
        resolvers.SCHEMA,
        debug=DEBUG,
        context_value=lambda request: Context(request, database),
        extensions=[ApolloTracingExtension]
    )
    routes = [
        Route('/api', graphql, name='api', methods=['GET', 'POST']),
        WebSocketRoute('/api', graphql, name='ws'),
        Route('/api/download/{file_id:int}', aoc_routes.download, name='download'),
        Route('/api/map/{match_id:int}', aoc_routes.svg_map, name='minimap'),
        Route('/api/portrait/{person_id:int}', aoc_routes.portrait, name='portrait')
    ]

    middleware = [
        Middleware(GZipMiddleware),
        Middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])
    ]

    app = Starlette(
        debug=DEBUG,
        routes=routes,
        middleware=middleware,
        on_startup=[warmer.setup],
        on_shutdown=[warmer.teardown]
    )
    app.state.database = database
    app.state.database_url = DATABASE_URL
    app.state.voobly_username = VOOBLY_USERNAME
    app.state.voobly_password = VOOBLY_PASSWORD
    return app


APP = new_app()
