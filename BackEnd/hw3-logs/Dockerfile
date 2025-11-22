FROM python:3.11-slim as build_stage

ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH="/app"

ENV PATH="$POETRY_HOME/bin:$PATH"
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -

WORKDIR /app
COPY pyproject.toml poetry.lock ./
COPY src /app
COPY scripts /app/scripts

FROM build_stage AS app

RUN poetry install --no-root --with main
ENTRYPOINT ["poetry", "run", "python", "main.py"]

FROM build_stage AS tests

RUN poetry install --no-root --with dev
COPY tests /app/tests
ENTRYPOINT ["poetry", "run", "pytest", "tests"]
