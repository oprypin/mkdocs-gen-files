#!/bin/bash

set -e -u -x
cd "$(dirname "$0")/.."

git diff --staged --quiet
git diff --quiet HEAD pyproject.toml
poetry version "$1"
poetry install
poetry build
git add pyproject.toml
git commit -m "v$1"
git tag -a -m "" "v$1"
poetry publish
echo git push origin master --tags
