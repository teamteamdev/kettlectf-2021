#!/bin/sh
python3 create_db.py "$1/state"
exec gunicorn -b "unix:$2/app.sock" "server:make_app(\"$1/state\")"