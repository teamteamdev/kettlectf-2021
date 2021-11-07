#!/bin/sh
exec gunicorn -b "unix:$2/rsabasics.sock" "server:make_app(\"$1/state\")"