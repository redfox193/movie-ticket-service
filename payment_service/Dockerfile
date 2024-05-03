FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY fast_ticket/ fast_ticket/
COPY payment_service/ payment_service/
COPY manage.py manage.py
COPY data/ data/