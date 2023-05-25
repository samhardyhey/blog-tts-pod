FROM python:3.10-slim-buster

RUN apt-get update

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt