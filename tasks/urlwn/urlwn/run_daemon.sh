#!/usr/bin/env nix-shell
#!nix-shell -i bash -p python3

exec "$TMPDIR/isolate" ./isolated_run_daemon.sh "$@"
