#!/usr/bin/env bash

#SCRIPTS_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
#cd $SCRIPTS_PATH
#cd ../

export $(cat ./local.env)
./scripts/dump.sh > database/dumps/`date +%Y-%m-%d`.dump

source venv/bin/activate
python source.py
deactivate
