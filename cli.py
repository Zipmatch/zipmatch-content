#!/usr/bin/env python
import os
import sys
import subprocess

import click
import dotenv
from flask import current_app
from flask.cli import FlaskGroup

from content.app import create_app


@click.group(cls=FlaskGroup, create_app=lambda info: create_app())
def cli():
    """This is a management script for the application."""
    dotenv.load_dotenv('.env')


@cli.command()
@click.option('--host', '-h', default='127.0.0.1', envvar='HOST', help='The interface to bind to.')
@click.option('--port', '-p', default=5000, envvar='PORT', help='The port to bind to.')
def run(host, port):
    """ Runs a local development server. """
    current_app.run(host, port)


@cli.command(context_settings=dict(
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


if __name__ == '__main__':
    cli()
