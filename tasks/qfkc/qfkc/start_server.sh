#!/bin/sh
exec gunicorn -b "unix:$2/app.sock" "server:make_app(\"$1/state\")"
