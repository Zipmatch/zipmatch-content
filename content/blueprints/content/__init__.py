from io import BytesIO

import boto3
from flask import Blueprint
from flask import jsonify
from flask import current_app
from flask import request

blueprint = Blueprint('content', __name__)


@blueprint.route('/content/<section>/<sub_section>/<fragment>', methods=["PUT"])
def add_content(section, sub_section, fragment):
    """ Create or Update a piece of content
    Endpoint to Create or update a piece of Content in S3
    ---
    description: Create or Update a piece of content
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
      - name: body
        in: body
        required: true
        schema:
          $ref: '#/definitions/ContentUpload'
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
    body = request.get_json()
    config = current_app.config
    client = _get_s3_client(config)
    key = _generate_key(config, section, sub_section, fragment)
    content = body['content']
    content_ready_for_upload = _prepare_content(content)
    client.upload_fileobj(content_ready_for_upload, config['BUCKET_NAME'], key)
    return jsonify({"message": "Content Uploaded to {b}/{k}".format(b=config['BUCKET_NAME'], k=key)})


@blueprint.route('/content/<section>/<sub_section>/<fragment>', methods=["GET"])
def content(section, sub_section, fragment):
    """ Get a piece of content
    Endpoint to retrieve content from S3
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
    client = _get_s3_client(config)
    key = _generate_key(config, section, sub_section, fragment)
    kwargs = {"Bucket": config['BUCKET_NAME'], "Key": key}
    content_obj = client.get_object(**kwargs)
    content_length = content_obj['ContentLength']
    content_body = content_obj['Body'].read().decode('utf8')
    return jsonify({"bucket": config['BUCKET_NAME'],
                    "key": key,
                    "content_length": content_length,
                    "body": content_body})


@blueprint.route('/content/paths', methods=["GET"])
def get_paths():
    """ Create and retrieve an 'filepaths' Object
    Endpoint to Create and retrieve an Object that represents all of the filepaths
    in the content store
    ---
    tags:
      - paths
    responses:
      200:
        description: content data
        schema:
          $ref: '#/definitions/FilepathData'
      404:
        description: Content not found
      default:
        description: Unexpected error
        schema:
          $ref: '#/definitions/ApiError'
    """
    client = _get_s3_client(current_app.config)
    objs = client.list_objects_v2(Bucket=current_app.config["BUCKET_NAME"])
    if objs['IsTruncated']:
        paginator = client.get_paginator('list_objects_v2')
        start_after = objs['Contents'][-1]['Key']
        page_iterator = paginator.paginate(Bucket=current_app.config["BUCKET_NAME"],
                                           StartAfter=start_after)
        for page in page_iterator:
            objs['Contents'].append(page['Contents'])
    keys = [x['Key'] for x in objs['Contents']]
    paths = {"sections": {}}
    for key in keys:
        keyparts = key.split("/")
        if keyparts[0] not in paths['sections']:
            paths['sections'][keyparts[0]] = {}
        if keyparts[1] not in paths['sections'][keyparts[0]]:
            paths['sections'][keyparts[0]][keyparts[1]] = []
        if keyparts[2] not in paths['sections'][keyparts[0]][keyparts[1]]:
            paths['sections'][keyparts[0]][keyparts[1]].append(keyparts[2])
    return jsonify(paths)


def _get_s3_client(config):
    kwargs = {'service_name': 's3',
              'aws_access_key_id': config['AWS_KEY'],
              'aws_secret_access_key': config['AWS_SECRET']}
    if 'S3_URL' in config and config['S3_URL']:
        kwargs['endpoint_url'] = "http://{url}".format(url=config['S3_URL'])
    session = boto3.session.Session()
    return session.client(**kwargs)


def _generate_key(config, section, sub_section, fragment):
    if '.' not in fragment:
        return "{sec}/{sub_sec}/{frag}{fext}".format(sec=section,
                                                     sub_sec=sub_section,
                                                     frag=fragment,
                                                     fext=config['CONTENT_FILE_EXTENSTION'])
    else:
        return "{sec}/{sub_sec}/{frag}".format(sec=section, sub_sec=sub_section, frag=fragment)


def _prepare_content(content):
    return BytesIO(bytes(content, 'utf-8'))
