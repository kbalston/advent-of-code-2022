#!/usr/bin/env bash

set -eux

SCRIPT_DIR="$(cd -P -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
cd "$SCRIPT_DIR"

pre-commit install

# Install git-delete-merged-branches
# https://github.com/hartwork/git-delete-merged-branches/releases
# It would be great to bake this into the container image itself,
# but unfortunately we're currently relying on the Python devcontainer feature
# which is executed after image build
pipx install git-delete-merged-branches==7.2.2

pip install --requirement requirements.txt
