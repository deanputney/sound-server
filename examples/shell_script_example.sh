#!/bin/bash
#
# Example: Shell Script with Sound Notifications
#
# This script demonstrates how to add audio feedback to shell scripts.
# Perfect for long-running tasks, deployments, or automation scripts.

set -e  # Exit on error

SOUND_SERVER="http://localhost:9091"

# Function to play a sound
play_sound() {
    local sound_name=$1
    local volume=${2:-1.0}

    curl -s -X POST "$SOUND_SERVER/play" \
        -H 'Content-Type: application/json' \
        -d "{\"sound\":\"$sound_name\", \"volume\":$volume}" \
        > /dev/null 2>&1 || true  # Don't fail if sound server is down
}

# Function to notify on script completion
notify_complete() {
    if [ $? -eq 0 ]; then
        echo "✅ Task completed successfully"
        play_sound "success.mp3"
    else
        echo "❌ Task failed"
        play_sound "error.mp3"
    fi
}

# Trap exit to play completion sound
trap notify_complete EXIT

# Example 1: Simple notification
echo "Starting task..."
play_sound "start.mp3"

# Simulate a long-running task
echo "Processing..."
sleep 2

# Example 2: Conditional notifications
if [ -f "/tmp/important_file.txt" ]; then
    echo "File found!"
    play_sound "notification.mp3" 0.7
else
    echo "File not found, creating it..."
    touch /tmp/important_file.txt
fi

# Example 3: Progress notifications
for i in {1..3}; do
    echo "Step $i/3..."
    sleep 1
    if [ $i -eq 3 ]; then
        play_sound "complete.mp3"
    else
        play_sound "tick.mp3" 0.5
    fi
done

echo "All tasks completed!"

# The trap will play the success sound automatically
