# Release Process

This document describes how to create and publish a new release of sound-server.

## Prerequisites

- [mise](https://mise.jdx.dev/) installed
- PyPI credentials configured for `uv publish`
- GitHub CLI (`gh`) authenticated
- Write access to the repository

## Quick Release

### Option 1: Auto-bump patch version

```bash
mise run release
```

This will:
- Auto-detect the last version (e.g., `2.0.0`)
- Bump the patch version (e.g., to `2.0.1`)
- Update `pyproject.toml`
- Commit and push
- Create and push a git tag
- Create a GitHub release

### Option 2: Specify version

```bash
mise run release 2.1.0
```

This will create version `2.1.0` instead of auto-bumping.

## Dry Run

Preview what the next release would be without creating it:

```bash
mise run release:dry-run
```

## Complete Release Workflow

### 1. Prepare the release

```bash
# Preview changes
mise run release:dry-run

# Create the release
mise run release          # Auto-bump patch
# or
mise run release 2.1.0    # Specific version
```

This creates:
- ✅ Version bump commit in `pyproject.toml`
- ✅ Git tag (e.g., `v2.1.0`)
- ✅ GitHub release with changelog

### 2. Publish to PyPI

```bash
mise run publish
```

This:
- ✅ Builds the package with `uv build`
- ✅ Publishes to PyPI with `uv publish`

**OR** manually:

```bash
uv build
uv publish
```

### 3. Homebrew Tap Auto-Update

After publishing to PyPI:
- ✅ GitHub Action automatically triggers
- ✅ Downloads tarball and calculates SHA256
- ✅ Updates formula in `deanputney/homebrew-tap`
- ✅ Users can immediately: `brew upgrade deanputney/tap/sound-server`

No manual intervention needed!

## Manual Steps (if needed)

If the GitHub Action fails or you need to manually update the tap:

1. Get the SHA256:
   ```bash
   VERSION=2.1.0
   curl -Ls "https://files.pythonhosted.org/packages/source/s/sound-server/sound-server-${VERSION}.tar.gz" | shasum -a 256
   ```

2. Update `deanputney/homebrew-tap`:
   ```bash
   cd ~/path/to/homebrew-tap

   # Edit Formula/sound-server.rb
   # Update version and SHA256

   git add Formula/sound-server.rb
   git commit -m "Update sound-server formula to v${VERSION}"
   git push
   ```

## Troubleshooting

### PyPI upload fails

Check your PyPI credentials:
```bash
# Ensure ~/.pypirc is configured or use environment variables
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-...
```

### GitHub Action doesn't trigger

- Verify the release was created (not just a tag)
- Check the Actions tab for errors
- Ensure `HOMEBREW_TAP_TOKEN` secret is set

### Version already exists

If you need to re-release a version:
```bash
# Delete the tag locally and remotely
git tag -d v2.1.0
git push origin :refs/tags/v2.1.0

# Delete the GitHub release
gh release delete v2.1.0

# Try again
mise run release 2.1.0
```

## Release Checklist

- [ ] All tests pass
- [ ] Documentation is up to date
- [ ] CHANGELOG is updated (if applicable)
- [ ] Version number follows semver
- [ ] Run `mise run release:dry-run` to preview
- [ ] Run `mise run release [version]`
- [ ] Run `mise run publish`
- [ ] Verify GitHub release created
- [ ] Wait for Homebrew tap to auto-update (~1 minute)
- [ ] Test installation: `brew upgrade deanputney/tap/sound-server`

## Version Numbering

Follow [Semantic Versioning](https://semver.org/):

- **Major** (X.0.0): Breaking changes
- **Minor** (x.Y.0): New features, backwards compatible
- **Patch** (x.y.Z): Bug fixes, backwards compatible

Examples:
- `2.0.0` → `2.0.1`: Bug fix
- `2.0.1` → `2.1.0`: New feature
- `2.1.0` → `3.0.0`: Breaking change
