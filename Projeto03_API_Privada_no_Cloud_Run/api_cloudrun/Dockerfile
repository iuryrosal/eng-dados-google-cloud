FROM python:3.8-slim

COPY requirements.txt /
RUN pip install -r requirements.txt

EXPOSE 8080

WORKDIR /app

COPY main.py /app/

ENV PORT 8080

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 60 main:app