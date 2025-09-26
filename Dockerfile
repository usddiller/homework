FROM python:3.13.7-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends\
    libpq-dev build-essential supervisor

RUN python -m venv /venv

ENV PATH="/venv/bin:$PATH"

COPY requirements.txt .

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

RUN pip install -r requirements.txt

COPY . .

RUN chmod +x /app/entrypoint.sh