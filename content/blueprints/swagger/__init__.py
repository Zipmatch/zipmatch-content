from functools import lru_cache

import yaml

from flask import Blueprint, jsonify, current_app
from flask_swagger import swagger

blueprint = Blueprint('swagger', __name__)


@blueprint.route("/swagger.json")
@lru_cache(maxsize=1)
def spec():
    with blueprint.open_resource('template.yaml') as f:
        template = yaml.load(f)
    return jsonify(swagger(current_app, template=template))
