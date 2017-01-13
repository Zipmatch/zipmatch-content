#!/bin/sh

## Make sure you replace [content-bucket] with a real default or you will get
## errors!

cd /code
export APP_BUCKET_NAME="${APP_BUCKET_NAME:=[content-bucket]}"
exec gunicorn -b 0.0.0.0:${PORT:=5004} -w ${WORKERS:=1} -k ${WORKER_CLASS:=sync} \
     --keep-alive ${KEEPALIVE:=2} --max-requests ${MAX_REQUESTS:=0} --access-logfile - \
     --threads ${THREADS:=1} "content.app:create_app()"
