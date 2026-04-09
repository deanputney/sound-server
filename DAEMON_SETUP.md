# Setting Up Sound Server as a macOS Daemon

This guide shows how to run sound-server as a permanent background service using macOS LaunchAgent.

## Overview

**LaunchAgent** is macOS's built-in system for running background services. Once configured:
- ✅ Starts automatically when you log in
- ✅ Runs persistently in the background
- ✅ Automatically restarts if it crashes
- ✅ Managed with `launchctl` commands
- ✅ Logs to system log

## Setup Steps

### 1. Create the LaunchAgent plist file

The plist file tells macOS how to run the service:

```bash
# Copy the provided plist to LaunchAgents directory
cp ~/projects/RESEARCH/sound_server/com.deanputney.soundserver.plist \
   ~/Library/LaunchAgents/
```

Or create it manually at `~/Library/LaunchAgents/com.deanputney.soundserver.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.deanputney.soundserver</string>

    <key>ProgramArguments</key>
    <array>
        <string>/Users/deanputney/.local/bin/sound-server</string>
    </array>

    <key>RunAtLoad</key>
    <true/>

    <key>KeepAlive</key>
    <true/>

    <key>StandardOutPath</key>
    <string>/Users/deanputney/Library/Logs/sound-server.out.log</string>

    <key>StandardErrorPath</key>
    <string>/Users/deanputney/Library/Logs/sound-server.err.log</string>

    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/Users/deanputney/.local/bin:/usr/local/bin:/usr/bin:/bin</string>
    </dict>
</dict>
</plist>
```

**Important:** Update `/Users/deanputney` to your actual home directory path!

### 2. Load the LaunchAgent

```bash
# Load the service (starts it and enables it for future logins)
launchctl load ~/Library/LaunchAgents/com.deanputney.soundserver.plist
```

The server should now be running!

### 3. Verify it's running

```bash
# Check if service is loaded
launchctl list | grep soundserver

# Or use the built-in check command
sound-server --check
```

## Managing the Service

### Start the service
```bash
launchctl start com.deanputney.soundserver
```

### Stop the service
```bash
launchctl stop com.deanputney.soundserver
```

### Restart the service
```bash
launchctl stop com.deanputney.soundserver
launchctl start com.deanputney.soundserver
```

### Disable (unload) the service
```bash
launchctl unload ~/Library/LaunchAgents/com.deanputney.soundserver.plist
```

### Re-enable the service
```bash
launchctl load ~/Library/LaunchAgents/com.deanputney.soundserver.plist
```

### Remove completely
```bash
# Unload
launchctl unload ~/Library/LaunchAgents/com.deanputney.soundserver.plist

# Delete the plist file
rm ~/Library/LaunchAgents/com.deanputney.soundserver.plist
```

## Viewing Logs

The service logs to files in `~/Library/Logs/`:

```bash
# View stdout log (server output)
tail -f ~/Library/Logs/sound-server.out.log

# View stderr log (errors)
tail -f ~/Library/Logs/sound-server.err.log

# View both
tail -f ~/Library/Logs/sound-server.*.log
```

## Troubleshooting

### Service won't start

1. Check the logs:
   ```bash
   cat ~/Library/Logs/sound-server.err.log
   ```

2. Verify the path to `sound-server` is correct:
   ```bash
   which sound-server
   ```

3. Test running it manually:
   ```bash
   sound-server
   ```

### Port already in use

If you get "port already in use" errors:

```bash
# Find what's using port 48291
lsof -i :48291

# Kill it if needed
kill <PID>
```

### Update after code changes

After updating the sound-server code:

```bash
# Reinstall
cd ~/projects/RESEARCH/sound_server
uv tool install --force .

# Restart the service
launchctl stop com.deanputney.soundserver
launchctl start com.deanputney.soundserver
```

## Comparison: Wrapper vs Daemon

### Current Approach (Wrapper Command)
```bash
sound-server -- yolobox claude --gh-token
```

**Pros:**
- ✅ Server only runs when needed
- ✅ No background processes when not in use
- ✅ Automatic cleanup
- ✅ Simple to understand

**Cons:**
- ❌ Slight startup delay each time
- ❌ Need to use wrapper command

### Daemon Approach (LaunchAgent)
```bash
# Just run your command directly
yolobox claude --gh-token
```

**Pros:**
- ✅ Server always ready (no startup delay)
- ✅ No wrapper needed
- ✅ Automatic restart on crash
- ✅ Survives reboots

**Cons:**
- ❌ Uses resources even when not needed
- ❌ More complex to set up
- ❌ Requires launchctl to manage

## Recommendation

**Use the daemon approach if:**
- You use Claude Code frequently throughout the day
- You want instant sound responses
- You don't mind a background process

**Use the wrapper approach if:**
- You only use Claude Code occasionally
- You prefer minimal background processes
- You want explicit control over when the server runs

## Hybrid Approach

You can even use both:
- Set up the daemon for your primary machine
- Use the wrapper on other machines or for testing
- The wrapper will detect the daemon is running and just use it

```bash
# On your main Mac: daemon always running
launchctl load ~/Library/LaunchAgents/com.deanputney.soundserver.plist

# On other machines or for testing: use wrapper
sound-server -- yolobox claude --gh-token
```
