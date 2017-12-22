FROM python:3.6-alpine

RUN apk update && apk add --update tini build-base
COPY requirements.txt /tmp/
RUN pip --no-cache-dir install -r /tmp/requirements.txt && \
    pip --no-cache-dir install gevent==1.2.2 gunicorn==19.7.1

COPY ./ /code

WORKDIR /code

EXPOSE 5004

ENTRYPOINT ["/sbin/tini", "--"]
CMD ["/usr/local/bin/gunicorn", "-c", "docker-config/gunicorn.py", "content.app:create_app()"]
