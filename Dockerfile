FROM python:3.8-slim-buster

COPY . /HOME/lightnings
WORKDIR /HOME/lightnings
RUN pip install -r requirements.txt --no-cache-dir

EXPOSE 5000
