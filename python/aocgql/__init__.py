"""Graphql helpers."""

import os

from mgzdb.api import API
from aocgql.loaders import Loader

def get_context():
    """Get graphql context."""
    db_api = API(
        os.environ.get('MGZ_DB'),
        os.environ.get('MGZ_STORE_PATH')
    )
    return {
        'api': db_api,
        'session': db_api.session,
        'loaders': Loader(db_api.session)
    }
