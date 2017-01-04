from flask import Blueprint
from flask import jsonify

blueprint = Blueprint('content', __name__)


@blueprint.route('/content/<str:section>/<str:sub_section>/<str:fragment>')
def content(section, sub_section, fragment):
    """ Piece of Content
    ---
    tags:
      - content
    parameters:
      - name: section
        in: path
        description: The section that the content is for
        type: string
        required: true
      - name: sub_section
        in: path
        description: The sub_section that the content is for
        type: string
        required: true
      - name: fragment
        in: path
        description: The actual fragment of content
        type: string
        required: true
    responses:
      200:
        description: content data
        schema:
          $ref: '#/definitions/ContentData'
      404:
        description: Content not found
      default:
        description: Unexpected error
        schema:
          $ref: '#/definitions/ApiError'
    """
