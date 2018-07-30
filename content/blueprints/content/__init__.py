from flask import Blueprint, jsonify, current_app, request

from .util import get_s3_client, generate_key, prepare_content
from ...extensions import cache

blueprint = Blueprint('content', __name__)


@blueprint.route('/content/<path:path>', methods=["PUT"])
def add_content(path):
    """ Create or Update a piece of content
    Endpoint to Create or update a piece of Content in S3
    """
    body = request.get_json()
    config = current_app.config
    client = get_s3_client(config)
    key = generate_key(config, path)
    content = body['content']
    content_ready_for_upload = prepare_content(content)
    client.upload_fileobj(content_ready_for_upload, config['BUCKET_NAME'], key)
    return jsonify({"message": "Content Uploaded to {b}/{k}".format(b=config['BUCKET_NAME'], k=key)})


@blueprint.route('/content/<path:path>', methods=["GET"])
@cache.cached
def get_content(path):
    """ Get a piece of content
    Endpoint to retrieve content from S3
    """
    config = current_app.config
    client = get_s3_client(config)
    key = generate_key(config, path)
    kwargs = {"Bucket": config['BUCKET_NAME'], "Key": key}
    content_obj = client.get_object(**kwargs)
    content_length = content_obj['ContentLength']
    content_body = content_obj['Body'].read().decode('utf8')
    content = {"bucket": config['BUCKET_NAME'],
                "key": key,
                "content_length": content_length,
                "body": content_body}
    return jsonify(content)


@blueprint.route('/content/paths', methods=["GET"])
@cache.cached
def get_paths():
    """ Create and retrieve an 'filepaths' Object
    Endpoint to Create and retrieve an Object that represents all of the filepaths
    in the content store
    """
    client = get_s3_client(current_app.config)
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
