# Sound Server for Docker-based Claude Code

## Purpose

A lightweight HTTP server that runs on the host machine to play sound files when requested by Claude Code running inside Docker. This replaces direct `afplay` calls (which don't work from inside Docker) with HTTP requests to a local server.

## Overview

- **Server Location**: Runs on host machine (macOS)
- **Access**: HTTP endpoint accessible from Docker via `host.docker.internal`
- **Port**: 48291 (or configurable)
- **Function**: Receives requests to play sound files and plays them using `afplay`

## API Design

### Endpoint: POST /play

**Request Body (JSON):**
```json
{
  "sound": "strong_minded.mp3"
}
```

**Response:**
```json
{
  "status": "playing",
  "sound": "strong_minded.mp3"
}
```

**Error Response:**
```json
{
  "status": "error",
  "message": "Sound file not found"
}
```

### Endpoint: GET /health

**Response:**
```json
{
  "status": "ok",
  "sounds_directory": "/Users/deanputney/scripts/sounds/notification_sounds"
}
```

### Endpoint: GET /sounds

**Response:**
```json
{
  "sounds": [
    "strong_minded.mp3",
    "just_saying.mp3",
    "you_would_be_glad_to_know.mp3"
  ]
}
```

## Requirements

### System Requirements
- macOS (for `afplay` command)
- Python 3.8+ or Node.js 16+
- Access to sound files directory: `~/scripts/sounds/notification_sounds/`

### Features
- Non-blocking sound playback (don't wait for sound to finish)
- Support for `.mp3`, `.wav`, `.aiff` files
- Configurable sounds directory
- Simple logging
- CORS headers for local access
- Optional: Volume control parameter

## Implementation Suggestions

### Option 1: Python (FastAPI)
```python
from fastapi import FastAPI
import subprocess
import os
from pathlib import Path

app = FastAPI()
SOUNDS_DIR = Path.home() / "scripts/sounds/notification_sounds"

@app.post("/play")
async def play_sound(request: dict):
    sound_name = request.get("sound")
    sound_path = SOUNDS_DIR / sound_name

    if not sound_path.exists():
        return {"status": "error", "message": "Sound not found"}

    # Non-blocking playback
    subprocess.Popen(["afplay", str(sound_path)])
    return {"status": "playing", "sound": sound_name}
```

### Option 2: Node.js (Express)
```javascript
const express = require('express');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

const app = express();
const SOUNDS_DIR = path.join(process.env.HOME, 'scripts/sounds/notification_sounds');

app.post('/play', (req, res) => {
    const soundPath = path.join(SOUNDS_DIR, req.body.sound);

    if (!fs.existsSync(soundPath)) {
        return res.json({ status: 'error', message: 'Sound not found' });
    }

    spawn('afplay', [soundPath], { detached: true });
    res.json({ status: 'playing', sound: req.body.sound });
});
```

## Claude Code Configuration

Update `~/.claude/settings.json` hooks to use curl instead of afplay:

```json
{
  "hooks": {
    "PermissionRequest": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "curl -s -X POST http://host.docker.internal:48291/play -H 'Content-Type: application/json' -d '{\"sound\":\"strong_minded.mp3\"}'"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "AskUserQuestion",
        "hooks": [
          {
            "type": "command",
            "command": "curl -s -X POST http://host.docker.internal:48291/play -H 'Content-Type: application/json' -d '{\"sound\":\"just_saying.mp3\"}'"
          }
        ]
      }
    ],
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "curl -s -X POST http://host.docker.internal:48291/play -H 'Content-Type: application/json' -d '{\"sound\":\"you_would_be_glad_to_know.mp3\"}'"
          }
        ]
      }
    ]
  }
}
```

## Starting the Server

### Python/FastAPI
```bash
cd ~/projects/sound-server
pip install fastapi uvicorn
uvicorn server:app --host 0.0.0.0 --port 48291
```

### Node.js/Express
```bash
cd ~/projects/sound-server
npm install express body-parser
node server.js
```

## Optional Enhancements

1. **Volume Control**: Add volume parameter to `/play` endpoint
2. **Sound Aliases**: Map friendly names to full file paths
3. **Pushover Integration**: Add `/notify` endpoint that also sends Pushover notification
4. **Queue Management**: Prevent overlapping sounds
5. **Configuration File**: YAML/JSON config for sounds directory, port, etc.
6. **Logging**: Log all play requests with timestamps

## Testing

```bash
# Test health endpoint
curl http://localhost:48291/health

# Test playing a sound
curl -X POST http://localhost:48291/play \
  -H 'Content-Type: application/json' \
  -d '{"sound":"strong_minded.mp3"}'

# List available sounds
curl http://localhost:48291/sounds

# Test from Docker
curl -X POST http://host.docker.internal:48291/play \
  -H 'Content-Type: application/json' \
  -d '{"sound":"strong_minded.mp3"}'
```

## Security Considerations

- Server should only listen on `localhost` (0.0.0.0 for Docker access)
- No authentication needed for local-only access
- Validate sound file paths to prevent directory traversal
- Limit sound file extensions to prevent arbitrary command execution
