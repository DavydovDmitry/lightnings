#!/usr/bin/env bash

export $(cat ./local.env)

if !([ -d "./database/dumps" ])
then
     mkdir "database/dumps"   
     echo "Put your dump to ./database/dumps"
else
     psql \
     --dbname=$DB_NAME \
     --host=$DB_IP \
     --port=$DB_PORT \
     --username=$DB_USER < database/dumps/2019-05-17.dump
fi
