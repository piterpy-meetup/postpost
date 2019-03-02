FROM python:3.6-alpine

ENV PYTHONPATH=/app/postpost \
    DJANGO_SETTINGS_MODULE=main.settings \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PIP_NO_CACHE_DIR=off

RUN apk --no-cache add gcc build-base linux-headers jpeg-dev zlib-dev postgresql-dev musl-dev && \
    pip install pipenv

WORKDIR /app
COPY Pipfile Pipfile.lock /app/
RUN pipenv sync

COPY . /app

CMD sh /app/run-app.sh
