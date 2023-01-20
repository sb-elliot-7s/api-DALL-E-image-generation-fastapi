FROM python:3.10.9-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

ENV HOST 0.0.0.0

ENV PORT 8000

CMD uvicorn main:app --reload --host $HOST --port $PORT