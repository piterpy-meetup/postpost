#!/bin/sh

pipenv run python $PYTHONPATH/manage.py migrate
exec 2>&1 pipenv run uwsgi --ini uwsgi.ini --home $(pipenv --venv)
