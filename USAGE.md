# Sound Server Usage

## Basic Usage

### Start the server normally

```bash
sound-server
```

The server will run in the foreground on port 48291.

## Daemon Mode (Run with Command)

The server can automatically start in the background, run your command, and then clean up:

```bash
sound-server -- yolobox claude --gh-token
```

This will:
1. ✅ Check if server is already running
2. 🎵 Start server in background (if not already running)
3. 🚀 Run your command
4. 🛑 Stop the server when command exits (only if we started it)

### Examples

```bash
# Run Claude Code with sound server
sound-server -- yolobox claude --gh-token

# Run any command with sound server
sound-server -- python my_script.py

# Chain multiple commands
sound-server -- bash -c "echo 'Starting...' && yolobox claude --gh-token"
```

## Smart Behavior

**If the server is already running:**
- ✅ It won't start a new one
- ✅ It will just run your command
- ✅ It won't stop the server when done (since it didn't start it)

**If the server is not running:**
- 🎵 It starts the server in background
- 🚀 Runs your command
- 🛑 Stops the server when done

## Check Server Status

```bash
sound-server --check
```

Returns:
- Exit code 0 if running
- Exit code 1 if not running

## Creating an Alias

Add to your `~/.zshrc` or `~/.bashrc`:

```bash
# Simple alias
alias yolo-claude='sound-server -- yolobox claude --gh-token'

# Or as a function for more flexibility
yolo-claude() {
    sound-server -- yolobox claude --gh-token "$@"
}
```

Then reload:
```bash
source ~/.zshrc
```

Now just run:
```bash
yolo-claude
```

## Keep Server Running

If you want the server to keep running between sessions:

```bash
# Start server in one terminal
sound-server

# In another terminal, run your commands normally
yolobox claude --gh-token
```

The server will stay running in the first terminal.

## Tips

- The `--` separator is important - it tells the command parser where the sound-server arguments end and your command begins
- You can pass any arguments to your command after the `--`
- The server checks if it's already running, so it's safe to call multiple times
- Press Ctrl+C to interrupt the command - the server will still be cleaned up properly
