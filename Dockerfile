FROM python:3.12-slim
LABEL authors="raulett"

RUN curl -sSL https://install.python-poetry.org | python3 -
WORKDIR /app
COPY pyproject.toml poetry.lock /app/
RUN poetry install --no-dev
COPY main.py 00000002.BIN.gpx 2023-06-30_11-54-52.txt /app/
ENV POETRY_VIRTUALENVS_CREATE=false
CMD ["python", "main.py"]

ENTRYPOINT ["top", "-b"]