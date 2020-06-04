FROM python:3.7-alpine

WORKDIR /app
COPY . /app

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev git\
    && rm -rf /var/cache/apk/*

RUN pip install --upgrade pip setuptools \
    && pip --no-cache-dir install pipenv \
    && pipenv lock -r --dev > requirements.txt \
    && pip install -r requirements.txt