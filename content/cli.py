#!/usr/bin/env python
import os
import sys
import subprocess

import click
from flask.cli import FlaskGroup

from content.app import create_app


def _parse_envfile(env_file):
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                variable, value = line.split('=')
                if value.startswith('"'):
                    os.environ[variable] = value.strip('"')
                elif value.startswith("'"):
                    os.environ[variable] = value.strip("'")
                else:
                    os.environ[variable] = value


def _create_app(info):
    return create_app()


@click.group(cls=FlaskGroup, create_app=_create_app)
def cli():
    """This is a management script for the application."""


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
    if os.path.exists('.env'):
        _parse_envfile('.env')
    if not os.environ.get('FLASK_DEBUG'):
        os.environ['FLASK_DEBUG'] = '1'
    cli()
