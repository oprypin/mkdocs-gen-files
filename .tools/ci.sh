#!/bin/sh
set -e

cd "$(dirname "$0")/.."

with_groups() {
    echo "::group::$@"
    "$@" && echo "::endgroup::"
}

"$@" autoflake -i -r --remove-all-unused-imports --remove-unused-variables mkdocs_gen_files
"$@" isort -q mkdocs_gen_files
"$@" black -q mkdocs_gen_files
python -c 'import sys, os; sys.exit((3,8) <= sys.version_info < (3,10) and os.name == "posix")' ||
"$@" pytype mkdocs_gen_files
