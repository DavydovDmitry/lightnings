#!/usr/bin/env bash

export $(cat ./local.env)

psql \
--dbname=$DB_NAME \
--host=$DB_IP \
--port=$DB_PORT \
--username=$DB_USER < database/dumps/2019-05-17.dump
