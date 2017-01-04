FROM jfloff/alpine-python:latest
# Install packages
RUN apk update

RUN mkdir /code

ADD . /code

ENV PYTHONIOENCODING "utf-8"

WORKDIR /code

RUN ln -s /usr/include/locale.h /usr/include/xlocale.h
RUN pip install -U pip && pip install -r requirements.txt && pip install gevent gunicorn
ADD https://github.com/krallin/tini/releases/download/v0.13.0/tini-static-amd64 /sbin/tini
RUN chmod +x /sbin/tini


EXPOSE 5003

ENTRYPOINT ["/sbin/tini", "--", "/code/docker-config/entrypoint.sh"]
