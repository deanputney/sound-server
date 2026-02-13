#!/bin/bash
# Wrapper script to run Claude Code with sound-server

set -e

# Start sound-server in the background
echo "🎵 Starting sound-server..."
sound-server &
SOUND_SERVER_PID=$!

# Give it a moment to start up
sleep 1

# Check if sound-server started successfully
if ! kill -0 $SOUND_SERVER_PID 2>/dev/null; then
    echo "❌ Failed to start sound-server"
    exit 1
fi

echo "✅ Sound-server running (PID: $SOUND_SERVER_PID)"
echo "🚀 Starting Claude Code..."
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping sound-server..."
    kill $SOUND_SERVER_PID 2>/dev/null || true
    wait $SOUND_SERVER_PID 2>/dev/null || true
    echo "✅ Cleanup complete"
}

# Register cleanup function to run on exit
trap cleanup EXIT INT TERM

# Run claude with all passed arguments
yolobox claude --gh-token "$@"
