# Unraid Docker Monitor

A Docker container monitor for Unraid that can view all containers on a custom Docker network.

## Features

- Container name, port number, directory listing
- CPU and RAM usage with sparkline charts
- Storage used for volumes
- Running/not running status with green/red dot indicator
- Sort by name, status, CPU, RAM, storage, or date
- 13 themes (dark/light mode and more)
- Full-width container cards with 50% CPU/RAM columns
- Hide/show toggle button on each card

## Quick Start

```bash
docker run -d \
  --name unraid-docker-monitor \
  -p 5000:5000 \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  ghcr.io/wildfirebill-docker/unraid-docker-monitor:latest
```

Then open http://your-unraid:5000

## Docker Compose

```yaml
version: '3.8'
services:
  unraid-docker-monitor:
    image: ghcr.io/wildfirebill-docker/unraid-docker-monitor:latest
    container_name: unraid-docker-monitor
    ports:
      - "5000:5000"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
    restart: unless-stopped
```

## Build from Source

```bash
docker compose up --build
```

## Requirements

- Unraid with Docker plugin
- Access to Docker socket (`/var/run/docker.sock`)
