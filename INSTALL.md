# Installation Guide

## Install as a uv Tool

The easiest way to use Sound Server is to install it as a `uv` tool:

```bash
# Navigate to the project directory
cd ~/projects/RESEARCH/sound_server

# Install as a uv tool
uv tool install .
```

This will:
- Install all dependencies in an isolated environment
- Make the `sound-server` command available globally
- Allow you to run it from anywhere

## Running

Once installed, simply run:

```bash
sound-server
```

The server will start on `http://localhost:48291`

## Updating

If you make changes to the code and want to reinstall:

```bash
uv tool install --force .
```

## Uninstalling

```bash
uv tool uninstall sound-server
```

## Troubleshooting

### Command not found

If `sound-server` is not found after installation, make sure uv's tool bin directory is in your PATH:

```bash
# Add to your ~/.zshrc or ~/.bashrc:
export PATH="$HOME/.local/bin:$PATH"
```

Then reload your shell:
```bash
source ~/.zshrc  # or source ~/.bashrc
```

### Port already in use

If port 48291 is already in use, you'll need to either:
1. Stop the process using that port
2. Modify `sound_server.py` to use a different port

Find what's using port 48291:
```bash
lsof -i :48291
```

## Testing

After starting the server, test it:

```bash
# Health check
curl http://localhost:48291/health

# List available sounds
curl http://localhost:48291/sounds

# Play a sound
curl -X POST http://localhost:48291/play \
  -H 'Content-Type: application/json' \
  -d '{"sound":"strong_minded.mp3"}'
```
