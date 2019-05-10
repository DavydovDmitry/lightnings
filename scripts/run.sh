#!/usr/bin/env bash

SCRIPTS_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $SCRIPTS_PATH
cd ../
export $(cat ./config/local.env)
cd scripts

docker-compose up -d

cd ../
source venv/bin/activate
python main.py
deactivate

docker-compose stop
