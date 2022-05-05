#!/bin/bash

cd /home/zileni/opSentinel5P
. venv/bin/activate
export FLASK_APP=sentinel5P
flask run -p 5001 -h 0.0.0.0
