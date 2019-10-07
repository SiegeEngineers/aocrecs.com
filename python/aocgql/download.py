"""Provide rec file downloads."""

import io
import os
from zipfile import ZIP_DEFLATED, ZipFile

import boto3
from flask import make_response, current_app

from mgzdb.util import path_components
from mgzdb.compress import decompress
from mgzdb.schema import File


def download(file_id):
    """Download route."""
    mgz_file = current_app.config['context']['session'].query(File).get(file_id)
    s3_client = boto3.client('s3')
    input_file = io.BytesIO()
    parts = path_components(mgz_file.hash) + [mgz_file.hash + '.mgc']
    s3_client.download_fileobj('aoc-recs', os.path.join(*parts), input_file)

    input_file.seek(0)
    mgz_bytes = decompress(input_file)

    output_file = io.BytesIO()
    with ZipFile(output_file, 'w', ZIP_DEFLATED) as zip_file:
        zip_file.writestr(mgz_file.original_filename, mgz_bytes)

    response = make_response(output_file.getvalue())
    response.headers['Content-Type'] = 'application/zip'
    return response
