from flask import Flask, jsonify

from botocore.exceptions import ClientError

from .extensions import envcfg, apierrors, applogging, cache
from .blueprints.status import blueprint as status_bp
from .blueprints.content import blueprint as content_bp
from .blueprints.cache import blueprint as cache_bp


def create_app():
    app = Flask('content')
    app.config.from_object('content.default_settings')
    envcfg.init_app(app)
    applogging.init_app(app)
    apierrors.init_app(app)
    cache.init_app(app)
    app.register_blueprint(status_bp)
    app.register_blueprint(content_bp, url_prefix='/v1')
    app.register_blueprint(cache_bp, url_prefix='/cache')
    app.register_error_handler(ClientError, _no_such_key)
    return app


def _no_such_key(error):
    # Boto3 exceptions are idiotic.
    if error.response['Error']['Code'] != "NoSuchEntity":
        return jsonify({'error': 'No such content'}), 404
    else:
        raise error
