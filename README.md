# zipmatch-content
Content Framework for storing / retrieving long-form content in S3

## Requirements
  - Python >= 3.5.1

## Installing requirements (in a virtualenv, preferably)
```shell
$ pip install -r requirements.txt
```

### Installing all requirements
```shell
$ pip install -r dev-requirements.txt
$ pip-sync requirements.txt dev-requirements.txt test-requirements.txt
```

## Running
```shell
$ ./cli.py run -p 5004
```

## Configuration
Done using environment variables:

AWS Credentials (Key and Secret)

### Configuring the docker container

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
