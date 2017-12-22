from flask import Blueprint
from flask import jsonify

blueprint = Blueprint('status', __name__)


@blueprint.route('/status')
def status():
    """ Status endpoint. """
    return jsonify({'message': 'Let the Content Flow!'})
