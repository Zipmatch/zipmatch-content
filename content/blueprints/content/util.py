from io import BytesIO

import boto3


def get_s3_client(config):
    kwargs = {'service_name': 's3',
              'aws_access_key_id': config['AWS_KEY'],
              'aws_secret_access_key': config['AWS_SECRET']}
    if 'S3_URL' in config and config['S3_URL']:
        kwargs['endpoint_url'] = "http://{url}".format(url=config['S3_URL'])
    session = boto3.session.Session()
    return session.client(**kwargs)


def generate_key(config, section, sub_section, fragment):
    if '.' not in fragment:
        return "{sec}/{sub_sec}/{frag}{fext}".format(sec=section,
                                                     sub_sec=sub_section,
                                                     frag=fragment,
                                                     fext=config['CONTENT_FILE_EXTENSTION'])
    else:
        return "{sec}/{sub_sec}/{frag}".format(sec=section, sub_sec=sub_section, frag=fragment)


def prepare_content(content):
    return BytesIO(bytes(content, 'utf-8'))
