#!/usr/bin/env python
import os
import sys
import subprocess

import click

from content.app import create_app
from content.blueprints.content.util import get_s3_client, generate_key, prepare_content

app = create_app()


@app.cli.command(context_settings=dict(
    ignore_unknown_options=True,
))
@click.argument('pytest_args', nargs=-1, type=click.UNPROCESSED)
def tests(pytest_args):
    """ Runs the test suite. """
    def get_app_env_keys():
        for k in os.environ.keys():
            if k.startswith('APP_'):
                yield k
    # Reset environment before tests
    for k in list(get_app_env_keys()):
        del os.environ[k]
    del os.environ['FLASK_DEBUG']
    os.environ['FLASK_TESTING'] = '1'
    args = ('pytest',) + pytest_args + ('tests/',)
    r = subprocess.run(args)
    sys.exit(r.returncode)


@app.cli.command()
@click.argument('source', type=click.File('r'))
@click.argument('section')
@click.argument('sub_section')
@click.argument('fragment')
def upload(source, section, sub_section, fragment):
    client = get_s3_client(app.config)
    key = generate_key(app.config, section, sub_section, fragment)
    content_ready_for_upload = prepare_content(source.read())
    client.upload_fileobj(content_ready_for_upload, app.config['BUCKET_NAME'], key)
