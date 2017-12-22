import os
import multiprocessing

if os.environ.get('GUNICORN_USER'):
    user = os.environ['GUNICORN_USER']
if os.environ.get('GUNICORN_GROUP'):
    group = os.environ['GUNICORN_GROUP']
bind = os.environ.get('GUNICORN_BIND', '0.0.0.0:5000')

if os.environ.get('GUNICORN_ACCESSLOG'):
    accesslog = os.environ['GUNICORN_ACCESSLOG']
if os.environ.get('GUNICORN_LOGLEVEL'):
    loglevel = os.environ['GUNICORN_LOGLEVEL']

workers = int(os.environ.get('GUNICORN_WORKERS', multiprocessing.cpu_count() * 2 + 1))
worker_class = os.environ.get('GUNICORN_WORKER_CLASS', 'gevent')
if os.environ.get('GUNICORN_WORKER_CONNECTIONS'):
    worker_connections = int(os.environ['GUNICORN_WORKER_CONNECTIONS'])
if os.environ.get('GUNICORN_MAX_REQUESTS'):
    max_requests = int(os.environ.get('GUNICORN_MAX_REQUESTS'))
max_requests_jitter = int(os.environ.get('GUNICORN_MAX_REQUESTS_JITTER', 100))
