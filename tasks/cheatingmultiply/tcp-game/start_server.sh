#!/bin/sh
export PYTHONUNBUFFERED=1
exec socat -T30 "unix-l:$2/app.sock",fork exec:"$(pwd)/game.py $1"
