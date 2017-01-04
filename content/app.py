from flask import Flask

from .extensions import envcfg, cors, apierrors, applogging
from .blueprints.status import blueprint as status_bp
from .blueprints.content import blueprint as content_bp
from .blueprints.swagger import blueprint as swagger_bp


def create_app():
    app = Flask('content')
    app.config.from_object('content.default_settings')
    envcfg.init_app(app)
    applogging.init_app(app)
    apierrors.init_app(app)
    cors.init_app(app)
    numpyjson.init_app(app)
    app.register_blueprint(status_bp)
    app.register_blueprint(content_bp, url_prefix='/v1')
    app.register_blueprint(swagger_bp)
    return app
