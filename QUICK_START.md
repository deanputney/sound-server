# Sound Server - Quick Start Guide

## You Have Two Options

### Option 1: Wrapper Command (Current - Recommended for Testing)

**What it does:** Starts server when needed, runs your command, stops server when done.

**Setup:**
```bash
# Already installed! Just use it:
sound-server -- yolobox claude --gh-token

# Or create an alias:
echo "alias yolo-claude='sound-server -- yolobox claude --gh-token'" >> ~/.zshrc
source ~/.zshrc

# Then run:
yolo-claude
```

**Pros:**
- ✅ Zero setup (already works!)
- ✅ Server only runs when needed
- ✅ Automatic cleanup

**Cons:**
- ❌ ~1 second startup delay

---

### Option 2: macOS Daemon (LaunchAgent)

**What it does:** Server runs permanently in background, always ready.

**Setup:**
```bash
# 1. Copy plist file
cp ~/projects/RESEARCH/sound_server/com.deanputney.soundserver.plist \
   ~/Library/LaunchAgents/

# 2. Load the service
launchctl load ~/Library/LaunchAgents/com.deanputney.soundserver.plist

# 3. Verify it's running
sound-server --check

# Done! Now just run directly:
yolobox claude --gh-token
```

**Pros:**
- ✅ Instant (no startup delay)
- ✅ Auto-starts on login
- ✅ Auto-restarts on crash

**Cons:**
- ❌ Always running (uses ~20MB RAM)
- ❌ More setup steps

---

## Which Should You Use?

### Start with Option 1 (Wrapper)
- Easy to test and verify everything works
- No commitment
- Works immediately

### Switch to Option 2 (Daemon) if:
- You use Claude Code all day
- You want instant sound responses
- You're happy with how it works

---

## Quick Commands

### Check if server is running
```bash
sound-server --check
```

### Using the wrapper
```bash
sound-server -- <any-command-here>
```

### Managing the daemon
```bash
# Start
launchctl start com.deanputney.soundserver

# Stop
launchctl stop com.deanputney.soundserver

# View logs
tail -f ~/Library/Logs/sound-server.*.log
```

---

## Files Reference

- `USAGE.md` - Detailed wrapper command usage
- `DAEMON_SETUP.md` - Complete daemon setup guide
- `com.deanputney.soundserver.plist` - LaunchAgent configuration file
