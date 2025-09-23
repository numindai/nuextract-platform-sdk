#!/usr/bin/env bash

# SDK generation script, to be run from the repository's root directory.

# To extract python template: openapi-generator author template -g python -o path/to/custom-template

# set -e: exit immediately if a command exits with a non-zero status.
set -e

# Go to the root directory of the repo
current_dir=$(basename "$PWD")
if [[ "$current_dir" != "nuextract-platform-sdk" ]]; then
  cd ..
fi

# Constants
openapi_specs_file_url="https://nuextract.ai/docs/docs.yaml"
openapi_specs_file_path="numind_api.yaml"

# PREPARATION
# Fetch OpenAPI specs file from the API and save as a temporary file
curl --output $openapi_specs_file_path $openapi_specs_file_url
# Moving the openapi-generator-ignore file at the root of the output directory. For
# whatever reason, using the --ignore-file-override flag pointing to a file in another
# location ignores all its content.
cp sdk_generation/.openapi-generator-ignore src/.openapi-generator-ignore

# Fix edit the OpenAPI specs file to remove the models not required for the SDK
python sdk_generation/remove_unused_models_from_openapi_spec_file.py --openapi-file-path=$openapi_specs_file_path --output-file-path=$openapi_specs_file_path

# Delete the current api client packages
if [ -d src/numind/openapi_client ]; then
  rm -r src/numind/openapi_client
fi
if [ -d tests/openapi_client ]; then
  rm -r tests/openapi_client
fi
if [ -d docs ]; then
  rm -r docs
fi
# Create a copy of the base numind __init__.py file as it'll be overwritten by the
# `openapi-generator generate` command
mv src/numind/__init__.py src/numind/__init__save.py

# SDK GENERATION
# Two clients are generated:
# - a sync one: tests, docs, README
# - an async one: tests, pyproject
# The only differences between the two are the .api package and the api_client.py file
# (must keep both versions in the final package). The models and configuration are
# identical. There will be a `NuMind` and a `NuMindAsync` classes
# Support files (gitlab, travis, git_push.sh, requirements, setup.cfg/py,
# tox.ini...) are ignored and not generated as specified in the
# .openapi-generator-ignore file present in the output directory.
openapi-generator-cli generate \
  -i $openapi_specs_file_path \
  -g python \
  --config sdk_generation/config.json \
  --additional-properties=packageName=numind.openapi_client \
  -o src
mv src/numind/openapi_client src/numind/openapi_client_tmp

# Copy generated documentation into the base README.md file
python sdk_generation/collate_documentation_readme.py

# Copying the tests and docs files.
mv src/test tests/openapi_client
mv src/docs .

# Generate the async client
# We use the same package name as previously (after that the first package has been
# renamed) so that all imports have the same name
openapi-generator-cli generate \
  -i $openapi_specs_file_path \
  -g python \
  --config sdk_generation/config.json \
  --additional-properties=packageName=numind.openapi_client,asyncio=true \
  -o src

# Copy async files to main client package
mv src/numind/openapi_client/api src/numind/openapi_client_tmp/api_async
mv src/numind/openapi_client/api_client.py src/numind/openapi_client_tmp/api_client_async.py

# Add async imports to openapi_client package (api, ApiClient)
python sdk_generation/adapt_openapi_client_init.py --init-path=src/numind/openapi_client_tmp/__init__.py

# Rename the temporary working package name to its real name
rm -r src/numind/openapi_client
mv src/numind/openapi_client_tmp src/numind/openapi_client

# Copy async tests
mv src/test tests/openapi_client_async

# Deduplicate test files
DIR1="tests/openapi_client"
DIR2="tests/openapi_client_async"
for file1 in "$DIR1"/*; do
    # Skip if not a regular file
    if [ ! -f "$file1" ]; then
        continue
    fi

    # Get the filename without path
    filename=$(basename "$file1")
    # Corresponding file in second directory
    file2="$DIR2/$filename"

    # Compare file contents
    if ! cmp -s "$file1" "$file2"; then
        # Files are different, create async version
        # Extract filename and extension
        if [[ "$filename" == *.* ]]; then
            # Has extension
            stem="${filename%.*}"
            extension="${filename##*.}"
            async_filename="${stem}_async.${extension}"
        else
            # No extension
            async_filename="${filename}_async"
        fi

        async_path="$DIR1/$async_filename"

        # Copy file2 to directory1 with async suffix
        # Read file and replace imports, then write to destination
        sed 's/^from numind\.openapi_client\.api/from numind.openapi_client.api_async/g' "$file2" > "$async_path"
        echo "Files differ: copied '$file2' to '$async_path' (with import modifications)"
    else
        echo "Files identical: '$filename' - no action needed"
    fi
done
rm -r $DIR2

# Clean up remaining directory that cannot be ignored in .openapi-generator-ignore.
rm -r src/.openapi-generator
rm src/numind/__init__.py  # copy back base __init__.py file
mv src/numind/__init__save.py src/numind/__init__.py

# Integrate client dependencies and client pyproject tools into project pyproject
python sdk_generation/adapt_pyproject.py --project-pyproject-path=sdk_generation/pyproject_base.toml --client-pyproject-path=src/pyproject.toml --client-requirements-path src/requirements.txt
rm src/pyproject.toml
rm src/*requirements.txt
rm src/README.md  # already used the one from sync client gen
rm -r src/docs  # already used the one from sync client gen

# TODO rewrite the package version in the pyproject as in the config.json, or find an
#  other way to fetch the define and fetch the package version in one place

# Run ruff to lint as much as possible
uvx ruff format
uvx ruff check --fix --exit-zero
uvx ruff format  # second pass to catch more fixable cases

# Delete OpenAPI specs file
rm $openapi_specs_file_path
rm src/.openapi-generator-ignore