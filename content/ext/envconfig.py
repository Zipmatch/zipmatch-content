import ast
from os import environ

DEFAULT_ENV_PREFIX = 'APP_'


class EnvConfig(object):
    """Configure Flask from environment variables."""

    def __init__(self, app=None, prefix=DEFAULT_ENV_PREFIX):
        self.app = app
        if app is not None:
            self.init_app(app, prefix)

    def init_app(self, app, prefix=DEFAULT_ENV_PREFIX):
        for key, value in environ.items():
            if key.startswith(prefix):
                key = key[len(prefix):]
                try:
                    value = ast.literal_eval(value)
                except (ValueError, SyntaxError):
                    value = str(value)
                app.config[key] = value
