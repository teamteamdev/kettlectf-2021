#!/bin/sh
cd "$2"
sed "s,TMPDIR,$2," /app/Caddyfile > Caddyfile
exec caddy run
