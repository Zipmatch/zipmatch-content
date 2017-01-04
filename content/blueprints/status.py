from flask import Blueprint
from flask import jsonify

blueprint = Blueprint('status', __name__)


@blueprint.route('/status')
def status():
    """ Status endpoint
    ---
    tags:
      - status
    definitions:
      - schema:
          id: Status
          description: Service status
          properties:
            message:
              type: string
              description: The status message
    responses:
      200:
        description: Everything is fine and dandy
        schema:
          $ref: '#/definitions/Status'
    """
    return jsonify({'message': 'Let the Content Flow!'})
