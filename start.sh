#!/bin/bash
# Start the Sound Server

echo "Starting Sound Server on port 48291..."
echo "Sounds directory: ~/scripts/sounds/notification_sounds"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Try to run as uv tool first, fall back to direct Python
if command -v sound-server &> /dev/null; then
    sound-server
else
    cd "$(dirname "$0")"
    python3 sound_server.py
fi
