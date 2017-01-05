import boto3
from flask import Blueprint
from flask import jsonify
from flask import current_app

blueprint = Blueprint('content', __name__)


@blueprint.route('/content/<section>/<sub_section>/<fragment>')
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
    config = current_app.config
    client = _getS3Client(config)
    key = "{sec}/{sub_sec}/{frag}{fext}".format(sec=section, sub_sec=sub_section, frag=fragment, fext=config['CONTENT_FILE_EXTENSTION'])
    kwargs = {"Bucket": config['BUCKET_NAME'], "Key": key}
    content_obj = client.get_object(**kwargs)
    content_length = content_obj['ContentLength']
    content_body = content_obj['Body'].read().decode('utf8')
    return jsonify({"bucket": config['BUCKET_NAME'], "key": key, "content_length": content_length, "body": content_body})


def _getS3Client(config):
    kwargs = {'service_name': 's3', 'aws_access_key_id': config['AWS_KEY'], 'aws_secret_access_key': config['AWS_SECRET']}
    if 'S3_URL' in config and config['S3_URL']:
        kwargs['endpoint_url'] = config['S3_URL']
    session = boto3.session.Session()
    return session.client(**kwargs)
