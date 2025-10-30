FROM python:3.13-alpine

ENV PYTHONUNBUFFERED=1
WORKDIR /app

RUN pip install poetry --no-cache-dir
RUN poetry config virtualenvs.create false
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-interaction --no-cache

COPY . .
CMD ["python", "src/main.py"]
