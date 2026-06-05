---
name: release
description: Use when preparing a new release — bump version, tag, and publish
user_invocable: true
---

# Release

Prepare and publish a new release of SVD-LLM.

## Step 1: Determine Version

```bash
# Current version
grep 'version' pyproject.toml | head -1

# Recent tags
git tag --sort=-v:refname | head -5

# Changes since last release
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "")
if [ -n "$LAST_TAG" ]; then
    git log "$LAST_TAG"..HEAD --oneline
fi
```

Ask the user what version to release (major.minor.patch).

## Step 2: Update Version

Edit `pyproject.toml` to update the version number.

## Step 3: Pre-release Checks

```bash
# Lint
ruff check .

# Tests
pytest tests/ -m "not integration" -v

# Verify package builds
pip install -e .
```

## Step 4: Create Release

```bash
VERSION="v<new_version>"

git add pyproject.toml
git commit -m "chore: bump version to $VERSION"
git tag "$VERSION"
git push origin master --tags

# Create GitHub release
gh release create "$VERSION" --title "$VERSION" --generate-notes
```

## Step 5: Verify

```bash
gh release view "$VERSION"
```
