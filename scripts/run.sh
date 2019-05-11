#!/usr/bin/env bash

#SCRIPTS_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
#cd $SCRIPTS_PATH
#cd ../
export $(cat ./config/local.env)

source venv/bin/activate
python database/sqlalchemy_declarative.py
python source.py
deactivate
