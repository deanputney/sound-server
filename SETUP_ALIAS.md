# Setting Up the yolo-claude Command

The `yolo-claude.sh` script automatically starts sound-server in the background, runs Claude Code, and cleans up the sound-server when you exit.

## Option 1: Add to PATH (Recommended)

Create a symlink in your local bin directory:

```bash
# Create ~/.local/bin if it doesn't exist
mkdir -p ~/.local/bin

# Create a symlink
ln -sf ~/projects/RESEARCH/sound_server/yolo-claude.sh ~/.local/bin/yolo-claude

# Make sure ~/.local/bin is in your PATH (add to ~/.zshrc or ~/.bashrc if needed)
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

Then run:
```bash
yolo-claude
```

## Option 2: Shell Alias

Add this to your `~/.zshrc` (or `~/.bashrc`):

```bash
alias yolo-claude='~/projects/RESEARCH/sound_server/yolo-claude.sh'
```

Then reload:
```bash
source ~/.zshrc
```

Run with:
```bash
yolo-claude
```

## Option 3: Shell Function (Most Flexible)

Add this function to your `~/.zshrc` (or `~/.bashrc`):

```bash
yolo-claude() {
    echo "🎵 Starting sound-server..."
    sound-server &
    local sound_pid=$!
    sleep 1

    if ! kill -0 $sound_pid 2>/dev/null; then
        echo "❌ Failed to start sound-server"
        return 1
    fi

    echo "✅ Sound-server running (PID: $sound_pid)"
    echo "🚀 Starting Claude Code..."
    echo ""

    # Run claude
    yolobox claude --gh-token "$@"

    # Cleanup
    echo ""
    echo "🛑 Stopping sound-server..."
    kill $sound_pid 2>/dev/null || true
    wait $sound_pid 2>/dev/null || true
    echo "✅ Cleanup complete"
}
```

Then reload:
```bash
source ~/.zshrc
```

Run with:
```bash
yolo-claude
```

## Usage

All options support passing additional arguments:

```bash
# Basic usage
yolo-claude

# With additional arguments
yolo-claude --some-flag

# With a specific project path
yolo-claude /path/to/project
```

## What It Does

1. ✅ Starts `sound-server` in the background
2. ✅ Verifies it started successfully
3. ✅ Runs `yolobox claude --gh-token` with any additional arguments
4. ✅ Automatically stops `sound-server` when you exit Claude
5. ✅ Cleans up even if you Ctrl+C

## Testing

To verify it's working:

```bash
# Start yolo-claude
yolo-claude

# You should see:
# 🎵 Starting sound-server...
# ✅ Sound-server running (PID: 12345)
# 🚀 Starting Claude Code...
```

Then when you exit Claude, you should see:
```
🛑 Stopping sound-server...
✅ Cleanup complete
```
