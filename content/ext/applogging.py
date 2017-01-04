import time
import logging

DEFAULT_LOG_FORMAT = '[%(asctime)s] %(levelname)s: %(name)s: %(message)s'


class AppLogging(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        if not app.debug and not app.testing:
            ch = logging.StreamHandler()
            log_fmt = app.config.get('APPLOGGING_FORMAT', DEFAULT_LOG_FORMAT)
            formatter = logging.Formatter(log_fmt)
            formatter.converter = time.gmtime
            ch.setFormatter(formatter)
            app.logger.addHandler(ch)
            app.logger.setLevel(logging.INFO)
