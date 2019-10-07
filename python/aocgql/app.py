"""Web server test entry point."""

import logging
import coloredlogs

from flask import Flask, request
from flask_caching import Cache
from flask_cors import CORS
from flask_graphql import GraphQLView

from aocgql import get_context
from aocgql.schema import SCHEMA
from aocgql.download import download


def new_app():
    """Entry point."""
    coloredlogs.install(
        level='DEBUG',
        fmt='%(asctime)s %(name)s %(levelname)s %(message)s'
    )
    logging.getLogger('boto').setLevel(logging.CRITICAL)
    logging.getLogger('botocore').setLevel(logging.CRITICAL)
    logging.getLogger('s3transfer').setLevel(logging.CRITICAL)
    logging.getLogger('sqlalchemy').setLevel(logging.INFO)
    app = Flask(__name__)
    cache = Cache(app, config={'CACHE_TYPE': 'simple', 'CACHE_DEFAULT_TIMEOUT': 1600})
    CORS(app)
    app.config['context'] = get_context()
    app.config['DEBUG'] = True

    gql_view = GraphQLView.as_view(
        'graphql',
        schema=SCHEMA,
        get_context=lambda: app.config['context'], # pylint: disable=unnecessary-lambda
        graphiql=True
    )
    cached_gql_view = cache.cached(key_prefix=lambda: request.data)(gql_view)
    app.add_url_rule('/graphql', view_func=cached_gql_view)
    app.add_url_rule(
        '/download/<file_id>',
        'download',
        download,
        methods=['GET', 'POST']
    )
    return app
