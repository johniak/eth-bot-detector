FROM python:3.9.4-slim-buster

RUN apt-get update
RUN apt-get install -y --no-install-recommends \
    build-essential \
    postgresql-client \
    libpq-dev \
    python-psycopg2 \
    curl \
    netcat

RUN apt-get clean
WORKDIR /tmp

ARG APP_ENV=prod
ENV POETRY_VERSION=1.1.6
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH = "${PATH}:/root/.poetry/bin"

ADD pyproject.toml poetry.lock /tmp/
RUN poetry config virtualenvs.create false \
  && poetry install $(test "$APP_ENV" == prod && echo "--no-dev")  --no-interaction --no-ansi

ADD . /code/

WORKDIR /code/
ENTRYPOINT ["./docker-entrypoint.sh"]