FROM python:3.12-slim
LABEL authors="raulett"

RUN apt-get update && apt-get install -y curl && apt-get clean
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry
WORKDIR /app
COPY pyproject.toml poetry.lock /app/
RUN poetry install --no-root
COPY main.py README.md 00000002.BIN.gpx 2023-06-30_11-54-52.txt /app/
ENV POETRY_VIRTUALENVS_CREATE=false