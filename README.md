# zipmatch-content #
Content Framework for storing / retrieving long-form content in S3

## Requirements ##
  - Python >= 3.5.1

## Installing requirements (in a virtualenv, preferably) ##
```shell
$ pip install -r requirements.txt
```

### Installing all requirements ###
```shell
$ pip install -r dev-requirements.txt
$ pip-sync requirements.txt dev-requirements.txt test-requirements.txt
```

## Running ##
```shell
$ ./cli.py run -p 5004
```

## Configuration
Done using environment variables:

### AWS Credentials (Key and Secret) ###

**APP_AWS_KEY**

**APP_AWS_SECRET**

**APP_AWS_REGION**

**APP_BUCKET_NAME**

### Local Development Only - Env Var for local "fake" S3 service. ###

**APP_S3_URL**

This Env Variable MUST be supplied in any environment where "Fake" S3 service is being used.

It MUST NOT be supplied in any environment where REAL AWS S3 is being used.

### Configuring the docker container

**N.B. Make sure you edit ./docker-config/entrypoint.sh to have a sane default for S3 Bucket!**

**PORT**
The port to listen on. Default `5004`.

**WORKERS**
Number of worker processes. Default `1`.

**WORKER_CLASS**
The worker class. Default `sync`.

**MAX_REQUESTS**
The number of requests to handle before restarting a worker. Defaults to `0` (never restart)

## Swagger specification
```shell
$ curl http://127.0.0.1:5004/swagger.json
```
