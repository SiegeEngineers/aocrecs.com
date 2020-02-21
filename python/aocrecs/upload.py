"""Provide rec file uploads."""

import os
import tempfile

import boto3

from mgzdb import platforms
from mgzdb.api import API
from mgzdb.util import path_components

from aocrecs.consts import S3_BUCKET


def add_rec(filename, contents, database_url, voobly_username, voobly_password):
    """Upload recorded game files."""
    s3_client = boto3.client('s3')
    sessions = platforms.factory(voobly_username=voobly_username, voobly_password=voobly_password)
    with tempfile.TemporaryDirectory() as rec_path:
        path = os.path.join(rec_path, filename)
        with open(path, 'wb') as rec:
            rec.write(contents)
        with tempfile.TemporaryDirectory() as store_path:
            file_hash, payload = API(database_url, store_path, sessions).add_file(path, 'upload')
            if file_hash is False:
                return dict(success=False, message=payload)
            if file_hash is not None:
                object_path = os.path.join(*path_components(file_hash) + [file_hash + '.mgc'])
                with open(os.path.join(store_path, object_path), 'rb') as data:
                    s3_client.upload_fileobj(data, S3_BUCKET, object_path)
            return dict(success=True, match_id=payload)
