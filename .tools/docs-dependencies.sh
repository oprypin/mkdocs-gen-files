#!/bin/sh
set -e

hatch env show --json | jq -r ".docs.dependencies | .[]" | pip-compile -U - -o docs/requirements.txt
