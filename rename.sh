#!/bin/bash

# Simple script to rename the project and package from template defaults
# Usage: ./rename.sh "new-project-name" "new_package_name"

OLD_PROJECT="dartfx-fairschema"
OLD_PACKAGE="fairschema"

NEW_PROJECT=$1
NEW_PACKAGE=$2

if [ -z "$NEW_PROJECT" ] || [ -z "$NEW_PACKAGE" ]; then
    echo "Usage: ./rename.sh <new-project-name> <new_package_name>"
    echo "Example: ./rename.sh dartfx-mycoolapp mycoolapp"
    exit 1
fi

echo "Renaming project from $OLD_PROJECT to $NEW_PROJECT"
echo "Renaming package from $OLD_PACKAGE to $NEW_PACKAGE"

# 1. Rename the package directory
if [ -d "src/dartfx/$OLD_PACKAGE" ]; then
    mv "src/dartfx/$OLD_PACKAGE" "src/dartfx/$NEW_PACKAGE"
elif [ -d "src/dartfx/hatch_foo" ]; then
    mv "src/dartfx/hatch_foo" "src/dartfx/$NEW_PACKAGE"
fi

# 2. Remove stale lock files and environments if they exist
rm -f uv.lock
rm -rf .hatch/
rm -rf .venv/
rm -rf .mypy_cache/

export LC_ALL=C
export LANG=C

# 3. Replace project & package names across files (including hidden configs like .github/ and .pre-commit-config.yaml)
find . -type f \
  ! -path '*/.git/*' \
  ! -path '*/__pycache__/*' \
  ! -path '*/.venv/*' \
  ! -path '*/.hatch/*' \
  ! -name "*.pyc" \
  ! -name ".DS_Store" \
  ! -name "rename.sh" \
  ! -name "uv.lock" \
  -exec bash -c '
    sedi() {
      if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i "" "$@"
      else
        sed -i "$@"
      fi
    }
    for file; do
      sedi "s/hatch-foo/'"$NEW_PROJECT"'/g" "$file"
      sedi "s/hatch_foo/'"$NEW_PACKAGE"'/g" "$file"
      sedi "s/'"$OLD_PROJECT"'/'"$NEW_PROJECT"'/g" "$file"
      sedi "s/'"$OLD_PACKAGE"'/'"$NEW_PACKAGE"'/g" "$file"
      sedi "s/DataArtifex\/'"$OLD_PROJECT"'/DataArtifex\/'"$NEW_PROJECT"'/g" "$file"
    done
  ' bash {} +

echo "Done! Please verify changes and run 'uv sync'."
