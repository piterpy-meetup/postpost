# postpost [![Build Status](https://travis-ci.com/PiterPy-Meetup/postpost.svg?branch=master)](https://travis-ci.com/PiterPy-Meetup/postpost)

metameta. Service for posting to social media

## Required
python3.6, redis

## Quick Start
`pipenv install`

`export PYTHONPATH=/full/path/postpost`

`export DJANGO_SETTINGS_MODULE=postpost.settings`

`pipenv run python manage.py migrate`

`pipenv run python manage.py runserver`

`pipenv run celery -A postpost worker -B`
