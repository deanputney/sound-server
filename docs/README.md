# Sound Server Documentation

## Overview

Sound Server is a lightweight HTTP server that enables Claude Code running in Docker to play sound files on your macOS host machine.

## Documentation Index

### Setup & Usage

- **[../README.md](../README.md)** - Main project README with quick start
- **[../QUICK_START.md](../QUICK_START.md)** - Quick comparison of wrapper vs daemon approaches
- **[../USAGE.md](../USAGE.md)** - Detailed wrapper command usage

### LaunchAgent (Background Service)

- **[launchd-setup.md](./launchd-setup.md)** - Complete guide for running as a macOS LaunchAgent

### Configuration Files

- **[../com.deanputney.soundserver.plist](../com.deanputney.soundserver.plist)** - LaunchAgent plist file
- **[../pyproject.toml](../pyproject.toml)** - Python package configuration

## Quick Reference

### Install as uv tool
```bash
cd ~/projects/RESEARCH/sound_server
uv tool install .
```

### Run with wrapper (recommended)
```bash
sound-server -- yolobox claude --gh-token
```

### Run as daemon (advanced)
```bash
# Install LaunchAgent
cp com.deanputney.soundserver.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.deanputney.soundserver.plist

# Then just run:
yolobox claude --gh-token
```

### Check status
```bash
sound-server --check
```

## Architecture

- **Server**: FastAPI-based HTTP server (port 48291)
- **Client**: Claude Code running in Docker
- **Connection**: `host.docker.internal:48291` from Docker to host
- **Sound playback**: `afplay` command on macOS

## Endpoints

- `GET /health` - Server health check
- `GET /sounds` - List available sound files
- `POST /play` - Play a sound file with optional volume control

## Files

```
sound_server/
├── sound_server.py          # Main server code
├── pyproject.toml           # Package configuration
├── requirements.txt         # Python dependencies
├── com.deanputney.soundserver.plist  # LaunchAgent config
├── README.md                # Main README
├── QUICK_START.md          # Quick comparison guide
├── USAGE.md                # Wrapper usage guide
├── INSTALL.md              # Installation guide
└── docs/
    ├── README.md           # This file
    └── launchd-setup.md    # LaunchAgent setup guide
```
