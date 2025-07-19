#!/usr/bin/env bash

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"

if [ "$#" -lt 1 ]; then
  >&2 echo "usage: ./bin/dev.sh <command>"
  exit 0
fi

docs () {
  poetryRun sphinx-build --builder html --fail-on-warning docs/source/ docs/build/
}

_lint () {
  poetryRun black "$@" docs/ src/ tests/
  poetryRun isort "$@" src/ tests/
}

lint () {
  _lint --check
}

lintFix () {
  _lint
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
  'docs:reqs') poetry --directory="$ROOT" export --format 'requirements.txt' --only 'docs' --output 'docs/requirements.txt';;
  lint) lint;;
  'lint:fix') lintFix;;
  ship) lint; typecheck; testCover; TOX_SKIP_ENV='py39' poetryRun tox; docs; echo 'Ship it!';;
  test) poetryRun pytest;;
  'test:cover') testCover;;
  'test:tox') poetryRun tox;;
  typecheck) typecheck;;
  *) echo "unsupported command: $1"; exit 1;;
esac
