# Sound Server

A lightweight HTTP server for playing audio files on macOS. Perfect for adding sound notifications to scripts, automation workflows, CI/CD pipelines, Docker containers, or any application that needs to trigger audio playback via HTTP.

## Why Sound Server?

- **Remote Audio Playback**: Play sounds on your Mac from containers, remote scripts, or automation tools
- **Simple HTTP API**: Just send a POST request to play a sound - no complex audio libraries needed
- **Non-blocking**: Sounds play in the background without blocking your HTTP requests
- **Volume Control**: Adjust playback volume per request (0.0 to 1.0)
- **Secure**: Built-in directory traversal protection and file type validation
- **Docker-Friendly**: Designed to work seamlessly with Docker containers using `host.docker.internal`

## Quick Start

### Installation

**Option 1: Install with uv (Recommended)**

```bash
uv tool install sound-server
```

**Option 2: Install from source**

```bash
git clone https://github.com/yourusername/sound-server.git
cd sound-server
uv tool install .
```

**Option 3: Traditional pip**

```bash
pip install sound-server
```

### Running the Server

Simply run:

```bash
sound-server
```

The server starts on `http://localhost:9091` and looks for sound files in `~/scripts/sounds/notification_sounds/` by default.

To check if the server is running:

```bash
sound-server --check
```

## Usage Examples

### Play a Sound

```bash
curl -X POST http://localhost:9091/play \
  -H 'Content-Type: application/json' \
  -d '{"sound":"notification.mp3"}'
```

### Play with Volume Control

```bash
curl -X POST http://localhost:9091/play \
  -H 'Content-Type: application/json' \
  -d '{"sound":"alert.mp3", "volume":0.5}'
```

### List Available Sounds

```bash
curl http://localhost:9091/sounds
```

### Check Server Health

```bash
curl http://localhost:9091/health
```

## Use Cases

### Docker Containers

Play sounds on the host from inside a Docker container:

```bash
curl -X POST http://host.docker.internal:9091/play \
  -H 'Content-Type: application/json' \
  -d '{"sound":"success.mp3"}'
```

### Shell Scripts

Add audio feedback to your automation scripts:

```bash
#!/bin/bash
# deploy.sh

echo "Starting deployment..."
curl -s -X POST http://localhost:9091/play \
  -H 'Content-Type: application/json' \
  -d '{"sound":"start.mp3"}'

# ... deployment steps ...

if [ $? -eq 0 ]; then
  curl -s -X POST http://localhost:9091/play \
    -H 'Content-Type: application/json' \
    -d '{"sound":"success.mp3"}'
else
  curl -s -X POST http://localhost:9091/play \
    -H 'Content-Type: application/json' \
    -d '{"sound":"error.mp3"}'
fi
```

### Python Applications

```python
import requests

def play_sound(sound_name, volume=1.0):
    """Play a sound notification"""
    try:
        response = requests.post(
            'http://localhost:9091/play',
            json={'sound': sound_name, 'volume': volume}
        )
        return response.json()
    except Exception as e:
        print(f"Failed to play sound: {e}")

# Usage
play_sound('notification.mp3', volume=0.7)
```

### GitHub Actions / CI/CD

Notify when builds complete (when running on self-hosted macOS runners):

```yaml
- name: Notify Build Success
  if: success()
  run: |
    curl -X POST http://localhost:9091/play \
      -H 'Content-Type: application/json' \
      -d '{"sound":"build-success.mp3"}'
```

### Temporary Server with Command

Start the server, run a command, then automatically stop the server:

```bash
sound-server -- ./run-tests.sh
```

This is perfect for one-off tasks where you want sound notifications without leaving the server running.

## Configuration

### Custom Sounds Directory

Set the `SOUNDS_DIR` environment variable or edit `sound_server.py`:

```python
SOUNDS_DIR = Path.home() / "your/custom/sounds/directory"
```

### Supported Audio Formats

- `.mp3` - MP3 Audio
- `.wav` - WAV Audio
- `.aiff` - AIFF Audio
- `.m4a` - M4A Audio

### Port Configuration

The server runs on port 9091 by default. To change this, modify the `run_server()` function in `sound_server.py`.

## API Reference

### `GET /health`

Check if the server is running and configured correctly.

**Response:**
```json
{
  "status": "ok",
  "sounds_directory": "/Users/you/scripts/sounds/notification_sounds"
}
```

### `GET /sounds`

List all available sound files.

**Response:**
```json
{
  "sounds": ["alert.mp3", "notification.mp3", "success.mp3"]
}
```

### `POST /play`

Play a sound file.

**Request Body:**
```json
{
  "sound": "notification.mp3",
  "volume": 0.8
}
```

**Parameters:**
- `sound` (required): Name of the sound file to play
- `volume` (optional): Volume level from 0.0 (silent) to 1.0 (full volume), defaults to 1.0

**Response:**
```json
{
  "status": "playing",
  "sound": "notification.mp3",
  "message": "Playing notification.mp3"
}
```

## Running as a Background Service

See [DAEMON_SETUP.md](DAEMON_SETUP.md) for instructions on running the server as a macOS LaunchAgent (auto-start on login).

## Troubleshooting

**Server won't start:**
- Check if port 9091 is already in use: `lsof -i :9091`
- Verify Python 3.8+ is installed: `python3 --version`
- Try running with `sound-server --check` first

**Sound won't play:**
- List available sounds: `curl http://localhost:9091/sounds`
- Verify the sound file exists in your sounds directory
- Test playback directly: `afplay ~/scripts/sounds/notification_sounds/test.mp3`
- Check server logs for error messages

**Can't access from Docker:**
- Make sure server is running on `0.0.0.0` (default), not just `localhost`
- Use `host.docker.internal` instead of `localhost` from inside Docker containers
- Check macOS firewall settings (System Settings → Network → Firewall)

**Permission denied errors:**
- Ensure the sounds directory exists and is readable
- Check file permissions: `ls -la ~/scripts/sounds/notification_sounds/`

## Development

### Running from Source

```bash
git clone https://github.com/yourusername/sound-server.git
cd sound-server
pip install -r requirements.txt
python sound_server.py
```

### Running Tests

```bash
./test.sh
```

## Requirements

- macOS (uses `afplay` for audio playback)
- Python 3.8 or higher
- FastAPI and Uvicorn (installed automatically)

## License

[Your License Here]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## See Also

- [Examples](examples/) - Practical integration examples
- [Daemon Setup](DAEMON_SETUP.md) - Run as a background service
- [Quick Start Guide](QUICK_START.md) - Get up and running in 60 seconds
