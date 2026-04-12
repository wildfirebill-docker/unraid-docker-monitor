# Unraid Docker Monitor - Specification

## Project Overview
- **Project Name**: Unraid Docker Monitor
- **Type**: Web Application (Docker Container)
- **Core Functionality**: Real-time monitoring of Docker containers on Unraid with metrics visualization
- **Target Users**: Unraid users who want to monitor their Docker containers

## UI/UX Specification

### Layout Structure
- **Header**: Logo, theme toggle (dark/light), network selector
- **Main Content**: Container cards grid with metrics
- **Sidebar**: Sort options, theme selector
- **Responsive Breakpoints**:
  - Mobile: < 768px (single column)
  - Tablet: 768px - 1024px (2 columns)
  - Desktop: > 1024px (3 columns)

### Visual Design

#### Dark Theme (Default)
- **Background**: #0d1117 (deep dark)
- **Card Background**: #161b22
- **Border**: #30363d
- **Primary Text**: #e6edf3
- **Secondary Text**: #8b949e
- **Accent**: #58a6ff
- **Success (Running)**: #3fb950
- **Error (Stopped)**: #f85149
- **Warning**: #d29922

#### Light Theme
- **Background**: #f6f8fa
- **Card Background**: #ffffff
- **Border**: #d0d7de
- **Primary Text**: #1f2328
- **Secondary Text**: #656d76
- **Accent**: #0969da
- **Success (Running)**: #1a7f37
- **Error (Stopped)**: #cf222e
- **Warning**: #9a6700

#### Typography
- **Font Family**: 'JetBrains Mono', 'Fira Code', monospace (tech aesthetic)
- **Headings**: 1.5rem - 2rem, weight 600
- **Body**: 0.875rem - 1rem, weight 400
- **Metrics**: 0.75rem, weight 500

#### Spacing System
- **Base unit**: 8px
- **Card padding**: 16px
- **Grid gap**: 16px
- **Section margin**: 24px

#### Visual Effects
- **Card shadow**: 0 4px 12px rgba(0,0,0,0.15)
- **Hover transition**: transform 0.2s ease, shadow 0.2s ease
- **Status dot animation**: pulse 2s infinite

### Components

#### Container Card
- Status indicator (green/red pulsing dot)
- Container name
- Image name
- Port numbers (exposed ports)
- Mounted directories list
- CPU usage chart (sparkline)
- RAM usage chart (sparkline)
- Storage used
- Created date

#### Header Bar
- Logo/Title
- Network dropdown selector
- Theme toggle button (sun/moon icon)
- Refresh button
- Auto-refresh toggle

#### Sort Controls
- Dropdown: Name, Status, CPU, RAM, Storage, Date
- Order: Ascending/Descending

#### Charts
- CPU: Line chart with fill, shows last 20 data points
- RAM: Line chart with fill, shows last 20 data points
- Both use Chart.js sparkline style

## Functionality Specification

### Core Features
1. **Container Discovery**: List all containers on specified Docker network
2. **Real-time Metrics**: CPU %, RAM (used/limit), Storage (volume sizes)
3. **Port Detection**: Show all exposed ports
4. **Directory Listing**: Show mounted volumes/directories
5. **Status Monitoring**: Running/Stopped with live updates
6. **History Charts**: 20-point rolling history for CPU/RAM
7. **Sorting**: By name, status, CPU, RAM, storage, date
8. **Filtering**: By network selection
9. **Theme Switching**: Dark/Light mode with persistence

### Data Handling
- Docker socket mounted for container inspection
- Stats collected via Docker Stats API
- LocalStorage for theme preference
- 30-second auto-refresh interval (configurable)

### Edge Cases
- Handle container restarts gracefully
- Show "N/A" for missing metrics
- Handle disconnected containers
- Graceful error handling for Docker unavailability

## Acceptance Criteria
1. All containers on selected network displayed with cards
2. Green pulsing dot for running, red static for stopped
3. CPU/RAM charts render with historical data
4. Sorting works for all fields
5. Dark/Light theme toggle works and persists
6. Port numbers displayed correctly
7. Directory/volume mounts listed
8. Storage usage shown for volumes
9. Responsive layout works on all screen sizes
10. Auto-refresh updates data without page reload