import os

AWS_KEY = None
AWS_SECRET = None
AWS_REGION = None
BUCKET_NAME = 'some-bucket'

CACHE_TYPE = os.environ.get('APP_CACHE_TYPE', 'null')
CACHE_DEFAULT_TIMEOUT = int(os.environ.get('APP_CACHE_DEFAULT_TIMEOUT', 300))
CACHE_KEY_PREFIX = os.environ.get('APP_CACHE_KEY_PREFIX', 'localdev:contentapi:')
CACHE_REDIS_URL = os.environ.get('APP_CACHE_REDIS_URL', 'redis://')
CACHE_NO_NULL_WARNING = True
