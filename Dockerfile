FROM python:3.8-slim-buster

WORKDIR /home/lightnings

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt --no-cache-dir

COPY . .

EXPOSE ${REST_PORT}
