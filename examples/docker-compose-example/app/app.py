#!/usr/bin/env python3
"""
Example application running in Docker that uses Sound Server on the host.
"""

import requests
import os
import time
import signal
import sys

SOUND_SERVER = os.getenv('SOUND_SERVER_URL', 'http://host.docker.internal:9091')

def play_sound(sound, volume=1.0):
    """Play a sound on the host machine"""
    try:
        response = requests.post(
            f'{SOUND_SERVER}/play',
            json={'sound': sound, 'volume': volume},
            timeout=2.0
        )
        if response.status_code == 200:
            print(f"🔊 Played: {sound}")
        else:
            print(f"⚠️  Failed to play {sound}: {response.status_code}")
    except Exception as e:
        print(f"❌ Error playing sound: {e}")

def check_sound_server():
    """Check if sound server is reachable"""
    try:
        response = requests.get(f'{SOUND_SERVER}/health', timeout=2.0)
        return response.status_code == 200
    except:
        return False

def signal_handler(sig, frame):
    """Handle shutdown gracefully"""
    print("\n🛑 Shutting down...")
    play_sound('goodbye.mp3', volume=0.6)
    time.sleep(1)
    sys.exit(0)

def main():
    """Main application logic"""
    print("=" * 60)
    print("Sound Server Docker Example")
    print("=" * 60)
    print(f"Sound Server URL: {SOUND_SERVER}")
    print()

    # Check if sound server is reachable
    if not check_sound_server():
        print("⚠️  WARNING: Sound server not reachable!")
        print("Make sure sound-server is running on the host:")
        print("  sound-server")
        print()
        print("Continuing anyway...")
    else:
        print("✅ Sound server is reachable!")
        play_sound('startup.mp3', volume=0.7)

    # Register signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    print("\n🚀 Application started!")
    print("Processing events... (Ctrl+C to stop)")
    print()

    # Simulate application doing work
    events = [
        ('data_received', 'notification.mp3', 0.5),
        ('processing', 'tick.mp3', 0.3),
        ('validation', 'tick.mp3', 0.3),
        ('success', 'success.mp3', 0.8),
    ]

    try:
        iteration = 0
        while True:
            iteration += 1
            print(f"\n--- Iteration {iteration} ---")

            for event_name, sound, volume in events:
                print(f"Event: {event_name}")
                play_sound(sound, volume)
                time.sleep(2)

            print(f"✅ Cycle {iteration} complete!")
            time.sleep(3)

    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)

if __name__ == '__main__':
    main()
