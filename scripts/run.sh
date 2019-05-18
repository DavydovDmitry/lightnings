#!/usr/bin/env bash

#SCRIPTS_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
#cd $SCRIPTS_PATH
#cd ../

export $(cat ./local.env)
DB_URI=postgresql+psycopg2://${DB_USER}:${DB_PASSWORD}@${DB_IP}:${DB_PORT}/${DB_NAME}

# upload media
source venv/bin/activate
python source.py
deactivate

# dump current db state
./scripts/dump.sh > database/dumps/`date +%Y-%m-%d`.dump
