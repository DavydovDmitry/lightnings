#!/usr/bin/env bash

SCRIPTS_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $SCRIPTS_PATH
cd ../
export $(cat ./config/local.env)
cd scripts

docker-compose up -d

source ../venv/bin/activate
python ../database/sqlalchemy_declarative.py
deactivate
