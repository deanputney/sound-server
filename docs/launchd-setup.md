# Sound Server as a macOS LaunchAgent

This guide explains how to run the sound-server as a permanent background service using macOS LaunchAgent.

## What is a LaunchAgent?

LaunchAgent is macOS's built-in system for managing user-level background services. Once configured:

- **Persistent** - Runs continuously in the background
- **Auto-start** - Starts automatically when you log in
- **Self-healing** - Automatically restarts if it crashes
- **System-integrated** - Managed with standard `launchctl` commands
- **Logged** - Output captured to log files

## Installation

### 1. Copy the plist file

The LaunchAgent configuration is defined in a plist (property list) file:

```bash
cp ~/projects/RESEARCH/sound_server/com.deanputney.soundserver.plist \
   ~/Library/LaunchAgents/
```

This places the configuration where macOS expects to find user LaunchAgents.

### 2. Load the service

```bash
launchctl load ~/Library/LaunchAgents/com.deanputney.soundserver.plist
```

This command:
- Registers the service with launchd
- Starts it immediately
- Ensures it starts automatically on future logins

### 3. Verify it's running

```bash
# Check if the service is loaded
launchctl list | grep soundserver

# Or use the built-in health check
sound-server --check

# Should output: ✅ Sound server is running
```

## Configuration File Explained

The `com.deanputney.soundserver.plist` file contains:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <!-- Unique identifier for the service -->
    <key>Label</key>
    <string>com.deanputney.soundserver</string>

    <!-- Command to run -->
    <key>ProgramArguments</key>
    <array>
        <string>/Users/deanputney/.local/bin/sound-server</string>
    </array>

    <!-- Start when loaded (at login) -->
    <key>RunAtLoad</key>
    <true/>

    <!-- Restart if it crashes -->
    <key>KeepAlive</key>
    <true/>

    <!-- Log stdout to file -->
    <key>StandardOutPath</key>
    <string>/Users/deanputney/Library/Logs/sound-server.out.log</string>

    <!-- Log stderr to file -->
    <key>StandardErrorPath</key>
    <string>/Users/deanputney/Library/Logs/sound-server.err.log</string>

    <!-- Set PATH environment variable -->
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/Users/deanputney/.local/bin:/usr/local/bin:/usr/bin:/bin</string>
    </dict>

    <!-- Working directory -->
    <key>WorkingDirectory</key>
    <string>/Users/deanputney</string>
</dict>
</plist>
```

**Important:** The file contains hardcoded paths to `/Users/deanputney`. If your username is different, you'll need to update these paths in the plist file.

## Managing the Service

### Start
```bash
launchctl start com.deanputney.soundserver
```

### Stop
```bash
launchctl stop com.deanputney.soundserver
```

### Restart
```bash
launchctl stop com.deanputney.soundserver
launchctl start com.deanputney.soundserver
```

### Check status
```bash
launchctl list | grep soundserver
# Shows PID if running, or "-" if stopped

sound-server --check
# Shows friendly status message
```

### Disable (unload)
```bash
launchctl unload ~/Library/LaunchAgents/com.deanputney.soundserver.plist
```

This stops the service and prevents it from starting at login.

### Re-enable (load)
```bash
launchctl load ~/Library/LaunchAgents/com.deanputney.soundserver.plist
```

### Completely remove
```bash
# First unload
launchctl unload ~/Library/LaunchAgents/com.deanputney.soundserver.plist

# Then delete the plist file
rm ~/Library/LaunchAgents/com.deanputney.soundserver.plist

# Optionally remove logs
rm ~/Library/Logs/sound-server.*.log
```

## Viewing Logs

The service logs are written to `~/Library/Logs/`:

```bash
# View recent stdout (server output)
tail -f ~/Library/Logs/sound-server.out.log

# View recent stderr (errors)
tail -f ~/Library/Logs/sound-server.err.log

# View both logs
tail -f ~/Library/Logs/sound-server.*.log

# View all stdout
cat ~/Library/Logs/sound-server.out.log

# Search logs for errors
grep -i error ~/Library/Logs/sound-server.*.log
```

## Updating After Code Changes

When you update the sound-server code:

```bash
# 1. Navigate to project directory
cd ~/projects/RESEARCH/sound_server

# 2. Reinstall with uv
uv tool install --force .

# 3. Restart the service
launchctl stop com.deanputney.soundserver
launchctl start com.deanputney.soundserver

# 4. Verify it's working
sound-server --check
```

## Troubleshooting

### Service won't start

**Check the error log:**
```bash
cat ~/Library/Logs/sound-server.err.log
```

**Common issues:**
- Path to `sound-server` is incorrect in the plist
- Port 9091 is already in use
- Permission issues

**Verify the command works manually:**
```bash
sound-server
# Should start the server without errors
```

### Port already in use

```bash
# Find what's using port 9091
lsof -i :9091

# If it's another sound-server instance:
kill <PID>

# Or stop via launchctl:
launchctl stop com.deanputney.soundserver
```

### Service crashes repeatedly

Check the logs to see why it's crashing:
```bash
tail -50 ~/Library/Logs/sound-server.err.log
```

The `KeepAlive` setting will make launchd keep trying to restart it, so fix the underlying issue.

### Changes to plist not taking effect

After modifying the plist file, you must reload it:
```bash
# Unload old version
launchctl unload ~/Library/LaunchAgents/com.deanputney.soundserver.plist

# Load new version
launchctl load ~/Library/LaunchAgents/com.deanputney.soundserver.plist
```

## Benefits vs Wrapper Command

### LaunchAgent Benefits
- ✅ **No startup delay** - server is always ready
- ✅ **Survives reboots** - auto-starts on login
- ✅ **Auto-recovery** - restarts if it crashes
- ✅ **Simple usage** - just run `yolobox claude --gh-token` directly

### LaunchAgent Drawbacks
- ❌ **Always running** - uses ~20-30MB RAM constantly
- ❌ **Setup required** - more complex than wrapper
- ❌ **Less visible** - can forget it's running

### When to Use LaunchAgent
- You use Claude Code frequently (multiple times per day)
- You want instant sound responses with no delay
- You don't mind a persistent background process

### When to Use Wrapper Instead
- You only use Claude Code occasionally
- You prefer minimal background processes
- You want explicit control over when the server runs

## Advanced Configuration

### Throttle restarts (prevent rapid crash loops)

Add to the plist:
```xml
<key>ThrottleInterval</key>
<integer>60</integer>
```

This prevents the service from restarting more than once per 60 seconds.

### Run only during certain hours

Add to the plist:
```xml
<key>StartCalendarInterval</key>
<dict>
    <key>Hour</key>
    <integer>9</integer>
    <key>Minute</key>
    <integer>0</integer>
</dict>
```

This would start at 9:00 AM. You can add multiple intervals.

### Custom port

To run on a different port, you'd need to:
1. Update `sound_server.py` to accept a port argument
2. Update the plist to pass the port: `<string>--port</string><string>9092</string>`
3. Update Claude hooks to use the new port

## Resources

- [Apple's launchd documentation](https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/CreatingLaunchdJobs.html)
- [launchd.info](https://www.launchd.info/) - Community resource for launchd
- Location of LaunchAgents: `~/Library/LaunchAgents/`
- Location of logs: `~/Library/Logs/`
