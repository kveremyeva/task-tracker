FROM python:3.11-slim

WORKDIR /app


RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*


RUN pip install --upgrade pip && \
    pip install poetry


COPY pyproject.toml poetry.lock ./


RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root


COPY . .


RUN python manage.py collectstatic --noinput

EXPOSE 8000


CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]