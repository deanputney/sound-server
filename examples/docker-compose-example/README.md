# Docker Compose Example

This example demonstrates how to use Sound Server from containerized applications using Docker Compose.

## Overview

The setup includes:
- **Sound Server**: Runs on the macOS host (not containerized)
- **App Container**: Example application that triggers sounds
- **Worker Container**: Example background worker that sends notifications

## Architecture

```
┌─────────────────────────────────────┐
│         macOS Host                  │
│                                     │
│  ┌──────────────────┐              │
│  │  Sound Server    │              │
│  │  :48291           │              │
│  └────────┬─────────┘              │
│           │                         │
│  ┌────────┴─────────────────────┐  │
│  │      Docker Engine           │  │
│  │                              │  │
│  │  ┌──────────┐  ┌──────────┐ │  │
│  │  │   App    │  │  Worker  │ │  │
│  │  │ Container│  │ Container│ │  │
│  │  └──────────┘  └──────────┘ │  │
│  └──────────────────────────────┘  │
└─────────────────────────────────────┘
```

Containers use `host.docker.internal:48291` to reach the Sound Server on the host.

## Prerequisites

1. Sound Server installed on the host:
   ```bash
   uv tool install sound-server
   ```

2. Docker and Docker Compose installed

3. Sound files in your configured sounds directory

## Usage

### Step 1: Start Sound Server on the host

```bash
sound-server
```

Leave this running in a terminal.

### Step 2: Start the containerized applications

In another terminal:

```bash
cd examples/docker-compose-example
docker-compose up
```

You should hear sounds playing as the containers do their work!

### Step 3: Stop everything

Press `Ctrl+C` to stop the containers, then stop the sound server.

## How It Works

### Network Configuration

The key to making this work is the `extra_hosts` configuration in `docker-compose.yml`:

```yaml
extra_hosts:
  - "host.docker.internal:host-gateway"
```

This allows containers to reach the host machine using the special hostname `host.docker.internal`.

### Environment Variable

Containers use an environment variable to find the Sound Server:

```yaml
environment:
  - SOUND_SERVER_URL=http://host.docker.internal:48291
```

### Application Code

The Python applications use this URL to send requests:

```python
SOUND_SERVER = os.getenv('SOUND_SERVER_URL', 'http://host.docker.internal:48291')
```

## Customization

### Add More Containers

Add more services to `docker-compose.yml`:

```yaml
services:
  my-service:
    image: my-image
    environment:
      - SOUND_SERVER_URL=http://host.docker.internal:48291
    extra_hosts:
      - "host.docker.internal:host-gateway"
```

### Use in Existing Projects

Just add the environment variable and extra_hosts to your existing services:

```yaml
services:
  your-existing-service:
    # ... existing config ...
    environment:
      - SOUND_SERVER_URL=http://host.docker.internal:48291
    extra_hosts:
      - "host.docker.internal:host-gateway"
```

Then use the Sound Server client code from the examples.

## Troubleshooting

**Containers can't reach Sound Server:**
- Verify Sound Server is running: `curl http://localhost:48291/health`
- Check firewall settings on the host
- Ensure `extra_hosts` is configured in docker-compose.yml
- Try accessing from inside the container: `docker exec -it sound-client-app curl http://host.docker.internal:48291/health`

**Sounds don't play:**
- Check that sound files exist on the host
- Verify Sound Server logs for errors
- Test with curl from the host: `curl -X POST http://localhost:48291/play -H 'Content-Type: application/json' -d '{"sound":"test.mp3"}'`

**Docker Compose fails to start:**
- Ensure Docker is running
- Check for port conflicts
- Review logs: `docker-compose logs`

## Production Considerations

For production use:

1. **Run Sound Server as a daemon**: See [DAEMON_SETUP.md](../../DAEMON_SETUP.md)
2. **Handle failures gracefully**: Make sound requests non-blocking and ignore failures
3. **Rate limiting**: Avoid overwhelming the sound server with too many requests
4. **Security**: Consider restricting access to the sound server port if needed

## Related Examples

- [Python Application](../python_example.py) - More detailed Python client
- [Shell Script](../shell_script_example.sh) - Shell script integration
- [GitHub Actions](../github-actions-example.yml) - CI/CD integration
