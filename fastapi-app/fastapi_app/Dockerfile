FROM python:3.8-slim

WORKDIR /app

COPY fastapi_app/. /app

RUN pip install -r requirements.txt

RUN pip install uvicorn