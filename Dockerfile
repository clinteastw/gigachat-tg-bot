FROM python:3.10.5-slim

RUN apt-get update && apt-get install -y \
    netcat \
    build-essential \
    libpq-dev \
    postgresql-server-dev-all

WORKDIR /app

ENV PYTHONDONTWRITEBYCODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .