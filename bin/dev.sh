#!/usr/bin/env bash

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"

if [ "$#" -lt 1 ]; then
  >&2 echo "usage: ./bin/dev.sh <command>"
fi

docs () {
  poetryRun sphinx-build --builder html --fail-on-warning docs/source/ docs/build/
}

lint () {
  poetryRun black "$@" docs/ src/ tests/
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

typecheck () {
  poetryRun mypy src/ tests/
}

case "$1" in
  docs) docs;;
  lint) lint --check;;
  'lint:fix') lint;;
  ship) lint; typecheck; testCover; TOX_SKIP_ENV='py39' poetryRun tox; docs; echo 'Ship it!';;
  test) poetryRun pytest;;
  'test:cover') testCover;;
  'test:tox') poetryRun tox;;
  typecheck) typecheck;;
  *) echo "unsupported command: $1"; exit 1;;
esac
