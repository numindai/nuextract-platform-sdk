#!/usr/bin/env bash

# To extract python template: openapi-generator author template -g python -o path/to/custom-template
# TODO fetch OpenAPI specs file from API itself and save as tmp file

# Generate the sdk.
# Support files (gitlab, travis, git_push.sh, README, requirements, setup.cfg/py,
# tox.ini...) are ignored and not generated as specified in the
# .openapi-generator-ignore file present in the output directory.
openapi-generator generate \
  -i ../data/numind_api.yaml \
  -g python \
  --config config.json \
  -o src
  # --template-dir template \

# Clean up remaining directory that cannot be ignored in .openapi-generator-ignore.
rm -r src/.openapi-generator

# Copying the tests, docs and pyproject.toml files.
if [ -d tests ]; then
  rm -r tests
fi
mv src/test tests
if [ -d docs ]; then
  rm -r docs
fi
mv src/docs .
#if [ -f pyproject.toml ]; then
#  rm pyproject.toml
#fi
#mv src/pyproject.toml .
# TODO relying on a 100% generated pyproject isn't sustainable/flexible. Using a fixed
#  pyproject file makes the project vulnerable to dependency changes. A custom script
#  extracting the dependencies in the generated pyproject.toml file and write them in
#  the base pyproject.toml file seems a good alternative to handle this problem.
