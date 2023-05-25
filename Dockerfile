FROM python:3.10-slim-buster

RUN apt-get update

WORKDIR /app

COPY . /app

# TODO: copy common > check python paths

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# TODO: add main command