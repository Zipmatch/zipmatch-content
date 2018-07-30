#!/bin/sh
export FLASK_APP="autoapp.py"
export FLASK_ENV="${FLASK_ENV:=development}"
export FLASK_SKIP_DOTENV="${FLASK_SKIP_DOTENV:=1}"
export FLASK_RUN_PORT=${PORT:=5004}
export FLASK_RUN_HOST=${HOST:=127.0.0.1}
export PYTHONDONTWRITEBYTECODE="1"
exec flask $@
