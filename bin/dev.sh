#!/usr/bin/env bash

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"

if [ "$#" -lt 1 ]; then
  >&2 echo "usage: ./bin/dev.sh <command>"
fi

lint () {
  poetryRun black "$@" src/ tests/
  poetryRun isort "$@" src/ tests/
}

poetryRun () {
  poetry --directory="$ROOT" run "$@"
}

testCover () {
  poetryRun coverage run --module 'pytest'
  poetryRun coverage report
  poetryRun coverage html
}

case "$1" in
  lint) lint;;
  'lint:fix') lint --check;;
  ship) lint; testCover; TOX_SKIP_ENV='py39' poetryRun tox; echo 'Ship it!';;
  test) poetryRun pytest;;
  'test:cover') testCover;;
  'test:tox') poetryRun tox;;
  *) echo "unsupported command: $1"; exit 1;;
esac
