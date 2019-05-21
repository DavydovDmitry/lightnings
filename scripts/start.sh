#!/usr/bin/env bash

export $(cat ./local.env)
export DB_URI=postgresql+psycopg2://${DB_USER}:${DB_PASSWORD}@${DB_IP}:${DB_PORT}/${DB_NAME}

# upload media
source venv/bin/activate
python database/sqlalchemy_declarative.py
python source.py
deactivate

# dump current database state
if !([ -d "./database/dumps" ])
then
     mkdir "database/dumps"   
fi
./scripts/dump.sh > database/dumps/`date +%Y-%m-%d`.dump