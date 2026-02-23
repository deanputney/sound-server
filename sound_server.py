#!/usr/bin/env python3
"""
Sound Server for Docker-based Claude Code
Plays sound files on the host machine via HTTP requests from Docker.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import os
from pathlib import Path
from typing import List
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Sound Server", description="Play sounds on macOS from Docker")

# Add CORS middleware for local access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
SOUNDS_DIR = Path.home() / "scripts/sounds/notification_sounds"
ALLOWED_EXTENSIONS = {".mp3", ".wav", ".aiff", ".m4a"}

# Request/Response models
class PlayRequest(BaseModel):
    sound: str
    volume: float = 1.0  # Optional volume control (0.0 to 1.0)

class PlayResponse(BaseModel):
    status: str
    sound: str
    message: str = None

class HealthResponse(BaseModel):
    status: str
    sounds_directory: str

class SoundsResponse(BaseModel):
    sounds: List[str]


@app.get("/", response_model=dict)
async def root():
    """Root endpoint with API information"""
    return {
        "name": "Sound Server",
        "version": "1.0.0",
        "endpoints": {
            "health": "GET /health",
            "sounds": "GET /sounds",
            "play": "POST /play"
        }
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "sounds_directory": str(SOUNDS_DIR)
    }


@app.get("/sounds", response_model=SoundsResponse)
async def list_sounds():
    """List all available sound files"""
    try:
        if not SOUNDS_DIR.exists():
            raise HTTPException(status_code=500, detail="Sounds directory not found")

        sounds = [
            str(f.relative_to(SOUNDS_DIR)) for f in SOUNDS_DIR.rglob("*")
            if f.is_file() and f.suffix.lower() in ALLOWED_EXTENSIONS
        ]
        sounds.sort()

        logger.info(f"Listed {len(sounds)} available sounds")
        return {"sounds": sounds}

    except Exception as e:
        logger.error(f"Error listing sounds: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/play", response_model=PlayResponse)
async def play_sound(request: PlayRequest):
    """Play a sound file using afplay"""
    sound_name = request.sound

    # Security: prevent directory traversal
    if ".." in sound_name or "\\" in sound_name:
        logger.warning(f"Blocked potential directory traversal attempt: {sound_name}")
        raise HTTPException(status_code=400, detail="Invalid sound name")

    # Construct full path, allowing subdirectory paths
    sound_path = (SOUNDS_DIR / sound_name).resolve()

    # Verify the resolved path is still within SOUNDS_DIR
    if not str(sound_path).startswith(str(SOUNDS_DIR.resolve())):
        logger.warning(f"Blocked path escape attempt: {sound_name}")
        raise HTTPException(status_code=400, detail="Invalid sound name")

    # If exact path not found, search subdirectories by filename
    if not sound_path.exists():
        basename = Path(sound_name).name
        matches = list(SOUNDS_DIR.rglob(basename))
        if matches:
            sound_path = matches[0]
            logger.info(f"Found {basename} at {sound_path.relative_to(SOUNDS_DIR)}")
        else:
            logger.warning(f"Sound file not found: {sound_name}")
            return PlayResponse(
                status="error",
                sound=sound_name,
                message="Sound file not found"
            )

    # Check file extension
    if sound_path.suffix.lower() not in ALLOWED_EXTENSIONS:
        logger.warning(f"Unsupported file extension: {sound_name}")
        return PlayResponse(
            status="error",
            sound=sound_name,
            message="Unsupported file format"
        )

    try:
        # Build afplay command with volume control
        cmd = ["afplay"]

        # Add volume control if not default
        if request.volume != 1.0:
            # afplay uses -v flag for volume (0.0 to 1.0)
            volume = max(0.0, min(1.0, request.volume))  # Clamp between 0 and 1
            cmd.extend(["-v", str(volume)])

        cmd.append(str(sound_path))

        # Non-blocking playback using Popen with detached process
        subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True  # Detach from parent process
        )

        logger.info(f"Playing sound: {sound_name} (volume: {request.volume})")

        return PlayResponse(
            status="playing",
            sound=sound_name,
            message=f"Playing {sound_name}"
        )

    except Exception as e:
        logger.error(f"Error playing sound {sound_name}: {e}")
        return PlayResponse(
            status="error",
            sound=sound_name,
            message=f"Error playing sound: {str(e)}"
        )


def is_server_running(port=9091, host="localhost"):
    """Check if the sound server is already running"""
    import socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception:
        return False


def run_server():
    """Run the sound server"""
    import uvicorn

    logger.info(f"Starting Sound Server on port 9091")
    logger.info(f"Sounds directory: {SOUNDS_DIR}")

    uvicorn.run(
        app,
        host="0.0.0.0",  # Listen on all interfaces (needed for Docker access)
        port=9091,
        log_level="info"
    )


def main():
    """Main entry point for the sound server CLI tool"""
    import argparse
    import sys
    import signal
    import time

    parser = argparse.ArgumentParser(
        description="Sound Server - Play sounds on macOS from Docker",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run server normally
  sound-server

  # Run with a command (starts server, runs command, stops server)
  sound-server -- yolobox claude --gh-token

  # Check if server is running
  sound-server --check
        """
    )
    parser.add_argument(
        '--check',
        action='store_true',
        help='Check if server is already running and exit'
    )
    parser.add_argument(
        'command',
        nargs='*',
        help='Command to run (server will start in background, run command, then stop)'
    )

    args = parser.parse_args()

    # Check mode
    if args.check:
        if is_server_running():
            print("✅ Sound server is running")
            sys.exit(0)
        else:
            print("❌ Sound server is not running")
            sys.exit(1)

    # If a command is provided, run in daemon mode
    if args.command:
        # Check if server is already running
        server_was_running = is_server_running()
        server_process = None

        if server_was_running:
            print("✅ Sound server is already running")
        else:
            print("🎵 Starting sound-server in background...")

            # Start server in background
            server_process = subprocess.Popen(
                [sys.executable, "-c",
                 "from sound_server import run_server; run_server()"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )

            # Wait for server to be ready
            for i in range(30):  # Try for 3 seconds
                time.sleep(0.1)
                if is_server_running():
                    print(f"✅ Sound server started (PID: {server_process.pid})")
                    break
            else:
                print("❌ Failed to start sound server")
                if server_process:
                    server_process.kill()
                sys.exit(1)

        # Run the command
        print(f"🚀 Running: {' '.join(args.command)}")
        print()

        try:
            # Run command and wait for it to complete
            result = subprocess.run(args.command)
            exit_code = result.returncode
        except KeyboardInterrupt:
            print("\n⚠️  Interrupted")
            exit_code = 130
        except Exception as e:
            print(f"❌ Error running command: {e}")
            exit_code = 1

        # Cleanup: stop server only if we started it
        if not server_was_running and server_process:
            print()
            print("🛑 Stopping sound-server...")
            server_process.terminate()
            try:
                server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server_process.kill()
            print("✅ Cleanup complete")

        sys.exit(exit_code)

    # Normal mode: run server in foreground
    else:
        if is_server_running():
            print("⚠️  Warning: Server may already be running on port 9091")
            print("   Use --check to verify, or stop the existing server first")
            print()

        run_server()


if __name__ == "__main__":
    main()
