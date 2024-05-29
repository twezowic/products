FROM python:3.8-slim

WORKDIR /app

COPY flask_app/. /app

RUN pip install -r requirements.txt

RUN apt-get update && \
    apt-get install -y build-essential

RUN pip install uwsgi