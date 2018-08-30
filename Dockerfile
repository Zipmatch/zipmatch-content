FROM python:3.6-alpine

RUN apk update && apk add --update tini build-base
RUN pip install -U pip && pip install pipenv
COPY Pipfile Pipfile.lock /tmp/
RUN PIPENV_PIPFILE=/tmp/Pipfile pipenv install --system --deploy && \
    pip --no-cache-dir install gevent==1.2.2 gunicorn==19.7.1 newrelic==4.2.0.100

COPY ./ /code

WORKDIR /code

EXPOSE 5004

ENTRYPOINT ["/sbin/tini", "--"]
CMD ["/usr/local/bin/newrelic-admin", "run-program", "/usr/local/bin/gunicorn", "-c", "docker-config/gunicorn.py", "content.app:create_app()"]
