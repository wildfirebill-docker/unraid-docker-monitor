# Unraid Docker Monitor

A real-time monitoring dashboard for Docker containers, designed for Unraid but works anywhere with Docker.

## Features

- **Container Monitoring**: View all containers on your Docker network
- **Metrics**: CPU usage, RAM usage, storage used
- **Charts**: 20-point rolling history for CPU and RAM
- **Status Indicator**: Green pulsing dot (running) / Red dot (stopped)
- **Port Listing**: Shows all exposed ports
- **Directory Listing**: Shows mounted volumes and bind mounts
- **Sorting**: By name, status, CPU, RAM, storage, date
- **Filtering**: Filter by Docker network
- **Themes**: 13 built-in themes (GitHub Dark/Light, Dracula, Nord, Monokai, One Dark, Gruvbox, Tokyo Night, Tokyo Storm, Catppuccin, Solarized, Horizon)
- **Auto-refresh**: Updates every 30 seconds
- **Zero CVEs**: Built with Alpine edge repositories, all security patches applied

## Quick Start

```bash
docker run -d \
  --name unraid-docker-monitor \
  -p 5000:5000 \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  ghcr.io/wildfirebill-docker/unraid-docker-monitor:latest
```

Then open `http://localhost:5000` in your browser.

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

## Unraid Installation

1. Go to Unraid Docker tab
2. Add Container
3. Use the provided XML template or paste the docker run command above
4. Map `/var/run/docker.sock` to the container
5. Access at `http://[unraid-ip]:5000`

## Build from Source

```bash
git clone https://github.com/wildfirebill-docker/unraid-docker-monitor
cd unraid-docker-monitor
docker build -t ghcr.io/wildfirebill-docker/unraid-docker-monitor:latest .
docker run -d -p 5000:5000 -v /var/run/docker.sock:/var/run/docker.sock:ro ghcr.io/wildfirebill-docker/unraid-docker-monitor:latest
```

## Environment Variables

| Variable | Description | Default |
|-----------|-------------|---------|
| `DOCKER_HOST` | Docker socket path | `unix:///var/run/docker.sock` |

## API Endpoints

| Endpoint | Description |
|---------|-------------|
| `GET /` | Web interface |
| `GET /api/containers` | List all containers |
| `GET /api/networks` | List Docker networks |
| `GET /api/networks/<id>` | Containers in a network |

## Theme Selection

Themes persist in localStorage. Select from the dropdown in the header:

- GitHub Dark (default)
- GitHub Light
- Dracula
- Nord
- Monokai
- One Dark
- Gruvbox Dark
- Gruvbox Light
- Tokyo Night
- Tokyo Storm
- Catppuccin
- Solarized Dark
- Horizon

## Container Data Shown

- Container name and image
- Status (running/exited)
- Port mappings
- Mounted directories/volumes
- CPU usage (%)
- RAM usage (used/limit)
- Storage used
- CPU/RAM charts with history

## Requirements

- Docker with API access (socket mounted)
- Web browser

## Security

Built using Alpine Linux edge repositories with all security patches applied:

- Uses `apk upgrade -a` during build to upgrade all packages to latest versions
- Fixed vulnerabilities: OpenSSL, musl, busybox, util-linux
- Zero known CVEs (scanned with Docker Scout)

Docker Scout report:
```
vulnerabilities: 0C 0H 0M 0L
```

## License

MIT
