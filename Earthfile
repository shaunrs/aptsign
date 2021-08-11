FROM debian:buster
WORKDIR /

RUN apt-get update
RUN apt-get install -y python3-pip

poetry:
    RUN pip3 install poetry
    COPY pyproject.toml ./
    RUN poetry install
    COPY --dir aptsign tests ./

linter:
    FROM +poetry
    RUN poetry run pylint aptsign/ tests/
    RUN poetry run black --diff aptsign/ tests/

format:
    FROM +poetry
    RUN poetry run black aptsign/ tests/
    SAVE ARTIFACT aptsign/ AS LOCAL ./
    SAVE ARTIFACT tests/ AS LOCAL ./

pytest:
    FROM +poetry
    RUN pytest --cov=aptsign --cov-fail-under=90 ./tests -v --ignore=venv --junit-xml pytest.xml

build:
    FROM +poetry
    RUN poetry build
    SAVE ARTIFACT dist/* AS LOCAL dist/

test:
    BUILD +linter
    BUILD +pytest

all:
    BUILD +test
    BUILD +build
