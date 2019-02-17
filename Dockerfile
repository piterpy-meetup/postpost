FROM python:3.6-alpine

ENV PYTHONPATH=/app/postpost \
    DJANGO_SETTINGS_MODULE=main.settings \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PIP_NO_CACHE_DIR=off

RUN apk --no-cache add gcc build-base linux-headers jpeg-dev zlib-dev && \
    pip install pipenv

WORKDIR /app
COPY Pipfile Pipfile.lock /app/
RUN pipenv sync

COPY . /app
RUN pipenv run python $PYTHONPATH/manage.py migrate

CMD pipenv run uwsgi --ini uwsgi.ini --home $(pipenv --venv)
