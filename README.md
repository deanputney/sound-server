# Sound Server

A lightweight HTTP server that enables Claude Code running in Docker to play sound files on your macOS host.

## Quick Start

### Installation with uv (Recommended)

Install as a uv tool (installs globally):

```bash
cd ~/projects/RESEARCH/sound_server
uv tool install .
```

Then run from anywhere:
```bash
sound-server
```

To update after changes:
```bash
uv tool install --force .
```

To uninstall:
```bash
uv tool uninstall sound-server
```

### Alternative: Traditional Python Installation

```bash
pip3 install -r requirements.txt
python3 sound_server.py
```

The server will start on `http://localhost:9091`

## API Endpoints

### GET /health
Check server status

```bash
curl http://localhost:9091/health
```

### GET /sounds
List all available sound files

```bash
curl http://localhost:9091/sounds
```

### POST /play
Play a sound file

```bash
curl -X POST http://localhost:9091/play \
  -H 'Content-Type: application/json' \
  -d '{"sound":"strong_minded.mp3"}'
```

With volume control (0.0 to 1.0):
```bash
curl -X POST http://localhost:9091/play \
  -H 'Content-Type: application/json' \
  -d '{"sound":"strong_minded.mp3", "volume":0.5}'
```

## Testing from Docker

```bash
curl -X POST http://host.docker.internal:9091/play \
  -H 'Content-Type: application/json' \
  -d '{"sound":"strong_minded.mp3"}'
```

## Claude Code Integration

Add these hooks to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PermissionRequest": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "curl -s -X POST http://host.docker.internal:9091/play -H 'Content-Type: application/json' -d '{\"sound\":\"strong_minded.mp3\"}'"
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
            "command": "curl -s -X POST http://host.docker.internal:9091/play -H 'Content-Type: application/json' -d '{\"sound\":\"just_saying.mp3\"}'"
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
            "command": "curl -s -X POST http://host.docker.internal:9091/play -H 'Content-Type: application/json' -d '{\"sound\":\"you_would_be_glad_to_know.mp3\"}'"
          }
        ]
      }
    ]
  }
}
```

## Configuration

Edit the `SOUNDS_DIR` variable in `server.py` to change the sounds directory:

```python
SOUNDS_DIR = Path.home() / "scripts/sounds/notification_sounds"
```

## Features

- ✅ Non-blocking sound playback
- ✅ Volume control support
- ✅ Lists available sounds
- ✅ Security: prevents directory traversal
- ✅ CORS enabled for local access
- ✅ Request logging
- ✅ Supports .mp3, .wav, .aiff, .m4a files

## Troubleshooting

**Server won't start:**
- Make sure port 9091 is not already in use
- Check that Python 3.8+ is installed

**Sound won't play:**
- Verify the sound file exists: `ls ~/scripts/sounds/notification_sounds/`
- Check server logs for errors
- Test directly: `afplay ~/scripts/sounds/notification_sounds/strong_minded.mp3`

**Can't access from Docker:**
- Make sure server is running on `0.0.0.0` (not just `localhost`)
- Use `host.docker.internal` instead of `localhost` from inside Docker
- Check firewall settings
