#!/usr/bin/env python3
"""
Example background worker that sends notifications to Sound Server.
This simulates a task queue worker or background job processor.
"""

import requests
import os
import time
import random

SOUND_SERVER = os.getenv('SOUND_SERVER_URL', 'http://host.docker.internal:48291')

def play_sound(sound, volume=1.0):
    """Play a sound on the host machine"""
    try:
        response = requests.post(
            f'{SOUND_SERVER}/play',
            json={'sound': sound, 'volume': volume},
            timeout=2.0
        )
        return response.status_code == 200
    except Exception as e:
        print(f"Warning: Could not play sound: {e}")
        return False

def process_job(job_id):
    """Simulate processing a background job"""
    print(f"📋 Processing job {job_id}...")

    # Random processing time
    processing_time = random.uniform(2, 5)
    time.sleep(processing_time)

    # Random success/failure
    success = random.random() > 0.2  # 80% success rate

    if success:
        print(f"✅ Job {job_id} completed successfully!")
        play_sound('job-success.mp3', volume=0.6)
        return True
    else:
        print(f"❌ Job {job_id} failed!")
        play_sound('job-failed.mp3', volume=0.8)
        return False

def main():
    """Main worker loop"""
    print("🔧 Background Worker Started")
    print(f"Sound Server: {SOUND_SERVER}")
    print("=" * 60)
    print()

    play_sound('worker-start.mp3', volume=0.5)

    job_id = 1
    while True:
        try:
            # Wait for "next job" (simulated)
            wait_time = random.uniform(3, 8)
            print(f"⏳ Waiting {wait_time:.1f}s for next job...")
            time.sleep(wait_time)

            # Process job
            play_sound('job-start.mp3', volume=0.4)
            process_job(job_id)

            job_id += 1

        except KeyboardInterrupt:
            print("\n🛑 Worker shutting down...")
            play_sound('worker-stop.mp3', volume=0.5)
            break

if __name__ == '__main__':
    main()
