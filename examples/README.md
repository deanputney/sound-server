# Sound Server Examples

This directory contains practical examples of integrating Sound Server into various workflows and applications.

## Examples Overview

- **[Shell Script Integration](shell_script_example.sh)** - Add audio notifications to bash scripts
- **[Python Application](python_example.py)** - Use Sound Server from Python code
- **[Docker Compose](docker-compose-example/)** - Play sounds from containerized applications
- **[GitHub Actions](github-actions-example.yml)** - CI/CD pipeline notifications
- **[Makefile Integration](makefile_example.mk)** - Audio feedback for build tasks
- **[Test Suite](test_notifications.sh)** - Notify when tests complete
- **[Claude Code Hooks](claude_code_hooks.json)** - Integrate with Claude Code IDE

## Quick Test

To verify your Sound Server is working with any example:

```bash
# Start the sound server
sound-server

# In another terminal, test it:
curl -X POST http://localhost:48291/play \
  -H 'Content-Type: application/json' \
  -d '{"sound":"notification.mp3"}'
```

## Requirements

All examples assume:
- Sound Server is running on `http://localhost:48291`
- You have sound files in `~/scripts/sounds/notification_sounds/` (or your configured directory)
- For Docker examples, use `http://host.docker.internal:48291` instead

## Getting Started

1. Start the Sound Server: `sound-server`
2. Choose an example that matches your use case
3. Adapt it to your needs
4. Enjoy audio feedback in your workflow!
