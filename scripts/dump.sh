#!/usr/bin/env bash

export $(cat ./config/local.env)

pg_dump \
--dbname=$DB_NAME \
--host=$DB_IP \
--port=$DB_PORT \
--username=$DB_USER > database/db.dump
