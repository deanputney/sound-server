# Homebrew Formula for sound-server

This document explains how to use and publish the Homebrew formula for sound-server.

## Formula Location

The formula is in `sound-server.rb` in this repository.

## Prerequisites

Before you can use this formula, you need to:

1. **Upload the package to PyPI** - The formula references a PyPI source distribution
2. **Update the SHA256 hash** - After uploading to PyPI, update the `sha256` field in the formula

## Publishing to Your Tap

To publish this formula to your tap at https://github.com/deanputney/homebrew-tap:

1. Clone your tap repository:
   ```bash
   git clone https://github.com/deanputney/homebrew-tap.git
   ```

2. Create a `Formula` directory if it doesn't exist:
   ```bash
   cd homebrew-tap
   mkdir -p Formula
   ```

3. Copy the formula:
   ```bash
   cp /path/to/sound-server.rb Formula/
   ```

4. **Important**: Update the SHA256 hash in the formula after uploading to PyPI:
   ```bash
   # After uploading to PyPI, get the hash:
   curl -s https://pypi.org/pypi/sound-server/1.1.0/json | \
     python3 -c "import sys, json; data = json.load(sys.stdin); \
     sdist = [f for f in data['urls'] if f['packagetype'] == 'sdist'][0]; \
     print(sdist['digests']['sha256'])"
   ```

5. Commit and push:
   ```bash
   git add Formula/sound-server.rb
   git commit -m "Add sound-server formula"
   git push
   ```

## Installing from Your Tap

Once published, users can install sound-server with:

```bash
# Add your tap (only needed once)
brew tap deanputney/tap

# Install sound-server
brew install sound-server
```

Or in one command:
```bash
brew install deanputney/tap/sound-server
```

## Testing the Formula Locally

Before publishing, you can test the formula locally:

```bash
# Test syntax and basic checks
brew audit --new-formula sound-server.rb

# Install from local file (requires PyPI upload first)
HOMEBREW_NO_INSTALL_FROM_API=1 brew install --build-from-source sound-server.rb

# Run tests
brew test sound-server
```

## Formula Details

The formula:
- Uses Python 3.12
- Installs into a virtual environment (following PEP 668)
- Includes all required dependencies as resource blocks:
  - fastapi (0.115.0)
  - uvicorn (0.34.0)
  - pydantic (2.10.0)
  - And all transitive dependencies
- Makes the `sound-server` command available

## Updating the Formula

When releasing a new version:

1. Update the `version` and `url` in the formula
2. Calculate the new SHA256:
   ```bash
   curl -sL <new-url> | shasum -a 256
   ```
3. Update the `sha256` field
4. Test the formula locally
5. Commit and push to your tap

## Dependencies Structure

The formula includes these Python packages:
- annotated-types (0.7.0)
- click (8.1.7)
- fastapi (0.115.0)
- h11 (0.14.0)
- pydantic (2.10.0)
- pydantic-core (2.27.0)
- starlette (0.52.1)
- typing-extensions (4.15.0)
- uvicorn (0.34.0)

## References

- [Homebrew Python Formula Documentation](https://docs.brew.sh/Python-for-Formula-Authors)
- [Homebrew Formula Cookbook](https://docs.brew.sh/Formula-Cookbook)
- [Simon Willison's Guide to Packaging Python CLI for Homebrew](https://til.simonwillison.net/homebrew/packaging-python-cli-for-homebrew)
