"""Provide rec file downloads."""

import io
import os

import boto3

from mgzdb.util import path_components
from mgzdb.compress import decompress

from aocrecs.consts import S3_BUCKET


def get_rec(file_hash, file_name, version):
    """Download route."""
    s3_client = boto3.client('s3')
    input_file = io.BytesIO()
    parts = path_components(file_hash) + [file_hash + '.mgc']
    s3_client.download_fileobj(S3_BUCKET, os.path.join(*parts), input_file)
    input_file.seek(0)
    mgz_bytes = decompress(input_file, version=version)
    return mgz_bytes
