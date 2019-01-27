# postpost [![Build Status](https://travis-ci.com/PiterPy-Meetup/postpost.svg?branch=master)](https://travis-ci.com/PiterPy-Meetup/postpost)

metameta. Service for posting to social media

## Required
python3.6, redis

## Quick Start
`pipenv install`

`export PYTHONPATH=/full/path/postpost`

`export DJANGO_SETTINGS_MODULE=main.settings`

`pipenv run python manage.py migrate`

`pipenv run python manage.py runserver`

`pipenv run celery -A main worker -B`

Add basic user

`python manage.py createsuperuser`

Login to [admin interface](http://localhost:8000/admin/oauth2_provider/application/) and create OAuth Application with
these params:

 - User: `1`
 - Client type: `Public`
 - Grant type: `Resource owner password based`
 - Name: e.g. `frontend`

Congrats! Now, there your [swagger](http://localhost:8000/swagger) and [redoc](http://localhost:8000/redoc)

