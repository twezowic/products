FROM python:3.8-slim

WORKDIR /app

COPY flask_app/. /app

RUN pip install -r requirements.txt

RUN pip install gunicorn