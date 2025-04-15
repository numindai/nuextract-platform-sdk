#!/usr/bin/env bash

# To extract python template: openapi-generator author template -g python -o path/to/custom-template

# Constants
openapi_specs_file_url="https://nuextract.ai/docs/docs.yaml"
openapi_specs_file_path="numind_api.yaml"

# PREPARATION
# Fetch OpenAPI specs file from the API and save as a temporary file
curl --output $openapi_specs_file_path $openapi_specs_file_url

# Fix edit the OpenAPI specs file to remove the models not required for the SDK
python src/remove_unused_models_from_openapi_spec_file.py --openapi-file-path=$openapi_specs_file_path --output-file-path=$openapi_specs_file_path

# Delete the current api client package
rm -r src/numind/openapi_client
# Create a copy of the base numind __init__.py file as it'll be overwritten by the
# `openapi-generator generate` command
mv src/numind/__init__.py src/numind/__init__save.py

# SDK GENERATION
# Generate the sdk.
# Support files (gitlab, travis, git_push.sh, README, requirements, setup.cfg/py,
# tox.ini...) are ignored and not generated as specified in the
# .openapi-generator-ignore file present in the output directory.
openapi-generator generate \
  -i $openapi_specs_file_path \
  -g python \
  --config config.json \
  -o src
  # --template-dir openapi-generator-template \

# Run ruff to lint as much as possible
uvx ruff check --fix
uvx ruff format

# Clean up remaining directory that cannot be ignored in .openapi-generator-ignore.
rm -r src/.openapi-generator
rm src/numind/__init__.py  # copy back base __init__.py file
mv src/numind/__init__save.py src/numind/__init__.py

# Copying the tests, docs and pyproject.toml files.
if [ -d tests ]; then
  rm -r tests/openapi_client
fi
mv src/test tests/openapi_client
if [ -d docs ]; then
  rm -r docs
fi
mv src/docs .
#if [ -f pyproject.toml ]; then
#  rm pyproject.toml
#fi
#mv src/pyproject.toml .
rm src/pyproject.toml
# TODO relying on a 100% generated pyproject isn't sustainable/flexible. Using a fixed
#  pyproject file makes the project vulnerable to dependency changes. A custom script
#  extracting the dependencies in the generated pyproject.toml file and write them in
#  the base pyproject.toml file seems a good alternative to handle this problem.
# TODO rewrite the package version in the pyproject as in the config.json, or find an
#  other way to fetch the define and fetch the package version in one place

# Delete OpenAPI specs file
rm $openapi_specs_file_path
