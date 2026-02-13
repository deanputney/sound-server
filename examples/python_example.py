#!/usr/bin/env python3
"""
Example: Python Application with Sound Notifications

This module demonstrates how to integrate Sound Server into Python applications.
Includes a reusable SoundNotifier class and usage examples.
"""

import requests
import time
from typing import Optional
from contextlib import contextmanager


class SoundNotifier:
    """
    A simple client for the Sound Server.

    Usage:
        notifier = SoundNotifier()
        notifier.play('success.mp3')
        notifier.play('alert.mp3', volume=0.7)
    """

    def __init__(self, server_url: str = "http://localhost:48291", silent_on_error: bool = True):
        """
        Initialize the sound notifier.

        Args:
            server_url: URL of the sound server
            silent_on_error: If True, failures are logged but don't raise exceptions
        """
        self.server_url = server_url.rstrip('/')
        self.silent_on_error = silent_on_error

    def play(self, sound: str, volume: float = 1.0, timeout: float = 2.0) -> bool:
        """
        Play a sound file.

        Args:
            sound: Name of the sound file (e.g., 'notification.mp3')
            volume: Volume level from 0.0 to 1.0 (default: 1.0)
            timeout: Request timeout in seconds (default: 2.0)

        Returns:
            True if successful, False otherwise
        """
        try:
            response = requests.post(
                f'{self.server_url}/play',
                json={'sound': sound, 'volume': volume},
                timeout=timeout
            )
            response.raise_for_status()
            result = response.json()
            return result.get('status') == 'playing'
        except Exception as e:
            if not self.silent_on_error:
                raise
            print(f"Warning: Failed to play sound '{sound}': {e}")
            return False

    def list_sounds(self) -> list[str]:
        """
        Get a list of available sounds.

        Returns:
            List of sound filenames
        """
        try:
            response = requests.get(f'{self.server_url}/sounds', timeout=2.0)
            response.raise_for_status()
            return response.json().get('sounds', [])
        except Exception as e:
            if not self.silent_on_error:
                raise
            print(f"Warning: Failed to list sounds: {e}")
            return []

    def is_available(self) -> bool:
        """
        Check if the sound server is running.

        Returns:
            True if server is reachable, False otherwise
        """
        try:
            response = requests.get(f'{self.server_url}/health', timeout=1.0)
            return response.status_code == 200
        except:
            return False

    @contextmanager
    def task_notification(self, start_sound: str = "start.mp3",
                         success_sound: str = "success.mp3",
                         error_sound: str = "error.mp3"):
        """
        Context manager for automatic task notifications.

        Usage:
            notifier = SoundNotifier()
            with notifier.task_notification():
                # Do some work
                process_data()
        """
        self.play(start_sound)
        try:
            yield
            self.play(success_sound)
        except Exception as e:
            self.play(error_sound)
            raise


# Example 1: Basic usage
def example_basic():
    """Basic sound notification example"""
    print("Example 1: Basic Usage")
    print("-" * 50)

    notifier = SoundNotifier()

    # Check if server is available
    if not notifier.is_available():
        print("⚠️  Sound server is not running!")
        print("Start it with: sound-server")
        return

    # Play a notification
    print("Playing notification sound...")
    notifier.play('notification.mp3')
    time.sleep(1)

    # Play with custom volume
    print("Playing alert at 50% volume...")
    notifier.play('alert.mp3', volume=0.5)
    time.sleep(1)

    # List available sounds
    sounds = notifier.list_sounds()
    print(f"\nAvailable sounds: {', '.join(sounds[:5])}...")


# Example 2: Long-running task with notifications
def example_long_task():
    """Example of notifying on task completion"""
    print("\nExample 2: Long-Running Task")
    print("-" * 50)

    notifier = SoundNotifier()

    print("Starting task...")
    notifier.play('start.mp3')

    # Simulate work
    for i in range(3):
        print(f"Processing step {i+1}/3...")
        time.sleep(1)

    print("✅ Task complete!")
    notifier.play('success.mp3')


# Example 3: Error handling with notifications
def example_error_handling():
    """Example of notifying on errors"""
    print("\nExample 3: Error Handling")
    print("-" * 50)

    notifier = SoundNotifier()

    try:
        print("Attempting risky operation...")
        notifier.play('start.mp3')

        # Simulate an operation that might fail
        import random
        if random.random() > 0.5:
            raise ValueError("Simulated error!")

        print("✅ Operation succeeded!")
        notifier.play('success.mp3')

    except Exception as e:
        print(f"❌ Operation failed: {e}")
        notifier.play('error.mp3')


# Example 4: Context manager usage
def example_context_manager():
    """Example using the context manager for automatic notifications"""
    print("\nExample 4: Context Manager")
    print("-" * 50)

    notifier = SoundNotifier()

    try:
        with notifier.task_notification():
            print("Processing data...")
            time.sleep(2)
            print("✅ Processing complete!")
    except Exception as e:
        print(f"❌ Processing failed: {e}")


# Example 5: Docker container usage
def example_docker():
    """Example for use from Docker containers"""
    print("\nExample 5: Docker Container Usage")
    print("-" * 50)

    # When running inside Docker, use host.docker.internal
    notifier = SoundNotifier(server_url="http://host.docker.internal:48291")

    if notifier.is_available():
        print("✅ Sound server reachable from Docker!")
        notifier.play('notification.mp3')
    else:
        print("❌ Cannot reach sound server from Docker")
        print("Make sure sound-server is running on the host")


if __name__ == '__main__':
    print("Sound Server Python Examples")
    print("=" * 50)
    print()

    # Run all examples
    example_basic()
    time.sleep(1)

    example_long_task()
    time.sleep(1)

    example_error_handling()
    time.sleep(1)

    example_context_manager()
    time.sleep(1)

    # Uncomment to test Docker example:
    # example_docker()

    print("\n" + "=" * 50)
    print("Examples complete!")
