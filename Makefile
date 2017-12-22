#!/usr/bin/env bash

DOCKER = $(shell which docker)
DOCKER_REPO := "674578336145.dkr.ecr.ap-southeast-1.amazonaws.com"
DOCKER_TAG ?= latest
IMAGE = zipmatch/zipmatch-content:$(DOCKER_TAG)
REMOTE_IMAGE = $(DOCKER_REPO)/$(IMAGE)
PORT ?= 5004
WORKER_CLASS ?= sync

all: build

build: clean install build-gulp build-docker


build-docker:
	$(DOCKER) build -t $(IMAGE) .

tag-docker:
	$(DOCKER) tag $(IMAGE) $(REMOTE_IMAGE)

push-docker:
	$(DOCKER) push $(REMOTE_IMAGE)

run-docker:
	$(DOCKER) run -i --expose=$(PORT) -p $(PORT):5000 \
	-e GUNICORN_WORKER_CLASS=$(WORKER_CLASS) \
	-t $(IMAGE)

.PHONY: build build-docker tag-docker upload-docker run-docker
