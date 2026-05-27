FROM python:3.12
LABEL authors="enrico"

RUN apt-get update && apt-get install -y binutils gettext postgresql-client

RUN mkdir -p /webapp
WORKDIR /webapp/

COPY ./ ./

ARG MY_ENV="local"
RUN pip install -r ./stack/${MY_ENV}/requirements.txt