#!/usr/bin/env -S bash -euET -o pipefail -O inherit_errexit

export statedir="$1"

export project_name="$(tr -dc A-Za-z0-9 </dev/urandom | head -c 13)"

compose() {
  docker-compose -p "$project_name" "$@"
}

cleanup() {
  compose down
}
trap cleanup EXIT

# Add your own state directories here.
mkdir -p "$statedir/redis" "$statedir/state"

compose up --build --abort-on-container-exit --renew-anon-volumes --remove-orphans
