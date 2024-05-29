FROM python:3.8-slim

COPY requirements.txt /
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8080
ENV PORT 8080
ENV HOST 0.0.0.0

WORKDIR /app

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app