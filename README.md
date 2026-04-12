# Unraid Docker Monitor

A Docker container monitor for Unraid.

## Quick Start

```bash
docker run -d \
  --name unraid-docker-monitor \
  -p 5000:5000 \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  ghcr.io/wildfirebill-docker/unraid-docker-monitor:latest
```

Then open http://your-unraid:5000
