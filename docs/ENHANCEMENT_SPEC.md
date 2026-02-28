# Sound Server Enhancement Specification

## Current State Analysis

### What It Is
Sound Server is an HTTP server that plays audio files on macOS via `afplay` command. It was originally designed to enable Claude Code running in Docker to play sounds on the host machine, but it's useful for any Docker-based or remote workflow that needs audio notifications.

### Current Features
- ✅ FastAPI HTTP server on port 48291
- ✅ Three endpoints: POST /play, GET /health, GET /sounds
- ✅ Volume control (0.0 to 1.0)
- ✅ Security: directory traversal prevention
- ✅ Non-blocking sound playback
- ✅ CORS enabled
- ✅ Smart wrapper command (starts server if needed)
- ✅ LaunchAgent support for background service

### Current Limitations
1. **Hardcoded path**: `~/scripts/sounds/notification_sounds` (line 35 of sound_server.py)
2. **Claude Code-focused docs**: README assumes Claude Code use case
3. **Installation**: Only uv tool install, no Homebrew
4. **Configuration**: Must edit source code to change settings
5. **Port**: Hardcoded to 48291
6. **No config file**: Can't persist settings

## Target State

### Goal
Make sound-server a general-purpose tool that anyone can use for audio notifications in:
- Docker-based development workflows
- CI/CD pipelines
- Development environment alerts
- Webhook integrations
- Remote work setups
- Automation scripts

### Key Enhancements

#### 1. Configurable Sounds Directory
**Priority: High**

Allow users to specify their sounds directory via multiple methods (precedence order):
1. CLI argument: `--sounds-dir /path/to/sounds`
2. Environment variable: `SOUND_SERVER_DIR`
3. Config file: `~/.sound-server/config.yaml`
4. Default: `~/Music/Sounds` (or similar generic path)

**Implementation:**
- Add argparse argument for --sounds-dir
- Check environment variable
- Load config file if present
- Fall back to default
- Pass directory to FastAPI app via dependency injection or global config

#### 2. Configurable Port
**Priority: Medium**

Allow port configuration via:
1. CLI argument: `--port 48291`
2. Environment variable: `SOUND_SERVER_PORT`
3. Config file: `port: 48291`
4. Default: 48291

#### 3. Configuration File Support
**Priority: High**

Create `~/.sound-server/config.yaml` support:

```yaml
# Sound Server Configuration

# Directory containing sound files
sounds_dir: ~/Music/Sounds

# Server port
port: 48291

# Allowed file extensions
allowed_extensions:
  - .mp3
  - .wav
  - .aiff
  - .m4a

# Log level (DEBUG, INFO, WARNING, ERROR)
log_level: INFO
```

**Implementation:**
- Add PyYAML dependency (optional)
- Create config loader function
- Merge config with CLI args and env vars
- Create example config file
- Document config file location and format

#### 4. Homebrew Installation
**Priority: High**

Create Homebrew formula for https://github.com/deanputney/homebrew-tap

Formula should:
- Install Python package and dependencies
- Create `sound-server` command
- Optionally install LaunchAgent plist
- Show post-install instructions

**Installation flow:**
```bash
brew tap deanputney/tap
brew install sound-server
sound-server --sounds-dir ~/Music/Sounds
```

#### 5. General-Purpose Documentation
**Priority: High**

Rewrite README.md:
- **Audience**: Developers, not just Claude Code users
- **Structure**:
  - What is this?
  - Installation (Homebrew first)
  - Quick start
  - Configuration
  - Use cases with examples
  - API reference
  - Troubleshooting

Move Claude Code-specific content to `docs/claude-code-integration.md`

#### 6. Examples Directory
**Priority: Medium**

Create `examples/` with:
- `docker-integration/` - Docker Compose setup
- `ci-notifications/` - GitHub Actions workflow
- `development-alerts/` - Test completion, build success hooks
- `webhook-integration/` - Simple webhook endpoint
- `curl-examples.sh` - Quick curl commands

Each example should be:
- Self-contained
- Well-documented
- Copy-paste ready

#### 7. Package Metadata
**Priority: Medium**

Update `pyproject.toml`:
```toml
[project]
name = "sound-server"
version = "2.0.0"
description = "HTTP server for playing audio notifications on macOS"
license = {text = "MIT"}
keywords = ["audio", "notifications", "docker", "macos", "fastapi"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: MacOS",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]

[project.urls]
Homepage = "https://github.com/deanputney/sound-server"
Repository = "https://github.com/deanputney/sound-server"
Issues = "https://github.com/deanputney/sound-server/issues"

[project.optional-dependencies]
config = ["pyyaml>=6.0"]
```

## Implementation Plan

### Phase 1: Core Configuration (Tasks #2, #5, #6)
1. Add CLI argument parsing (--sounds-dir, --port, --config)
2. Add environment variable support
3. Implement YAML config file loading
4. Update pyproject.toml
5. Create example config file

**Owner:** config-developer

### Phase 2: Documentation (Tasks #4, #8)
1. Rewrite README for general audience
2. Move Claude Code docs to docs/claude-code-integration.md
3. Create examples directory with use cases
4. Document all configuration options

**Owner:** docs-writer

### Phase 3: Homebrew Distribution (Task #3)
1. Research Python app packaging for Homebrew
2. Create formula file
3. Test local installation
4. Document tap usage

**Owner:** homebrew-packager

### Phase 4: Licensing & Testing (Tasks #7, #9)
1. Add MIT LICENSE file
2. Create feature branch
3. Test all configuration methods
4. Test Homebrew installation
5. Create PR with comprehensive description

**Owner:** team-lead

## Success Criteria

✅ Users can install via: `brew install deanputney/tap/sound-server`
✅ Users can configure sounds directory without editing code
✅ Configuration persists via config file
✅ Documentation shows multiple use cases (not just Claude Code)
✅ Examples are clear and copy-paste ready
✅ Backwards compatible with existing setups
✅ All tests pass
✅ PR is clean and well-documented

## Backwards Compatibility

Maintain backwards compatibility where possible:
- Default path could check old location first, warn if found
- Existing Claude Code hooks continue to work
- Wrapper command behavior unchanged
- LaunchAgent plist still works

## Timeline

Estimated: 2-3 hours with team of 4
- Phase 1 (Config): 1 hour
- Phase 2 (Docs): 45 minutes
- Phase 3 (Homebrew): 45 minutes
- Phase 4 (Testing/PR): 30 minutes

Parallelized work should complete faster than serial.
