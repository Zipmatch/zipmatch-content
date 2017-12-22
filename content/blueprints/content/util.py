from os.path import splitext
from io import BytesIO

import boto3

DEFAULT_CONTENT_EXTENSION = '.md'


def get_s3_client(config):
    kwargs = {'service_name': 's3',
              'aws_access_key_id': config['AWS_KEY'],
              'aws_secret_access_key': config['AWS_SECRET']}
    if 'S3_URL' in config and config['S3_URL']:
        kwargs['endpoint_url'] = "http://{url}".format(url=config['S3_URL'])
    session = boto3.session.Session()
    return session.client(**kwargs)


def generate_key(config, path):
    if not splitext(path)[1]:
        return '{}{}'.format(path, DEFAULT_CONTENT_EXTENSION)
    return path


def prepare_content(content):
    return BytesIO(bytes(content, 'utf-8'))
