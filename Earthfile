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

formatter:
    FROM +poetry
    RUN poetry run black --diff aptsign/ tests/

pytest:
    FROM +poetry
    RUN pytest --cov=aptsign --cov-fail-under=90 ./tests -v --ignore=venv --junit-xml pytest.xml

build:
    FROM +poetry
    RUN poetry build
    SAVE ARTIFACT dist/* AS LOCAL dist/

test:
    BUILD +linter
    BUILD +formatter
    BUILD +pytest

all:
    BUILD +test
    BUILD +build
