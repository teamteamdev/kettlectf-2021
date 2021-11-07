#!/usr/bin/env -S bash -euET -o pipefail -O inherit_errexit

dockerfile="Dockerfile.generator"
generator="generator.py"

workdir="$2"

container="$(docker build -qf "$dockerfile" .)"
exec docker run --rm \
  -v "$PWD/:$PWD/:ro" \
  -v "$workdir/:$workdir/" \
  -e HOME=/tmp \
  -- "$container" "$PWD/$generator" "$@"
