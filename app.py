from flask import Flask, render_template, jsonify, request
import docker
import json
import threading
import time
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

docker_client = docker.DockerClient(base_url='unix:///var/run/docker.sock')

container_stats = {}
container_history = {}
MAX_HISTORY = 20

def get_container_stats(container):
    try:
        stats = container.stats(stream=False)
        
        cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - stats['precpu_stats']['cpu_usage']['total_usage']
        system_delta = stats['cpu_stats']['system_cpu_usage'] - stats['precpu_stats']['system_cpu_usage']
        
        if system_delta > 0 and cpu_delta > 0:
            cpu_percent = (cpu_delta / system_delta) * len(stats['cpu_stats']['cpu_usage'].get('percpu_usage', [0])) * 100
        else:
            cpu_percent = 0.0
        
        mem_used = stats['memory_stats'].get('usage', 0)
        mem_limit = stats['memory_stats'].get('limit', 1)
        mem_percent = (mem_used / mem_limit) * 100 if mem_limit > 0 else 0
        
        return {
            'cpu_percent': round(cpu_percent, 2),
            'memory_used': mem_used,
            'memory_limit': mem_limit,
            'memory_percent': round(mem_percent, 2)
        }
    except Exception as e:
        return {'cpu_percent': 0, 'memory_used': 0, 'memory_limit': 1, 'memory_percent': 0}

def get_ports(container):
    try:
        ports = []
        port_bindings = container.ports or {}
        for container_port, host_bindings in port_bindings.items():
            if host_bindings:
                for host_binding in host_bindings:
                    ports.append(f"{host_binding['HostIp']}:{host_binding['HostPort']}->{container_port}")
            else:
                ports.append(f"{container_port}")
        return ports
    except:
        return []

def get_directories(container):
    try:
        dirs = []
        mounts = container.attrs.get('Mounts', [])
        for mount in mounts:
            if mount.get('Type') in ['bind', 'volume']:
                dirs.append({
                    'source': mount.get('Source', mount.get('Name', 'Unknown')),
                    'destination': mount.get('Destination', 'Unknown'),
                    'mode': mount.get('Mode', ''),
                    'rw': mount.get('RW', False)
                })
        return dirs
    except:
        return []

def get_storage_used(container):
    try:
        total_size = 0
        mounts = container.attrs.get('Mounts', [])
        for mount in mounts:
            if mount.get('Type') == 'volume':
                try:
                    volume = docker_client.volumes.get(mount.get('Name', ''))
                    usage = docker_client.api.inspect_volume(mount.get('Name', ''))
                    if usage and 'UsageData' in usage:
                        total_size += usage['UsageData'].get('Size', 0)
                except:
                    pass
        return total_size
    except:
        return 0

def format_bytes(size):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} PB"

def collect_container_data():
    global container_stats, container_history
    
    while True:
        try:
            containers = docker_client.containers.list(all=True)
            logger.info(f"Found {len(containers)} containers")
            
            for container in containers:
                try:
                    stats = get_container_stats(container)
                    container_id = container.id
                    
                    if container_id not in container_history:
                        container_history[container_id] = {'cpu': [], 'memory': []}
                    
                    container_history[container_id]['cpu'].append(stats['cpu_percent'])
                    container_history[container_id]['memory'].append(stats['memory_percent'])
                    
                    if len(container_history[container_id]['cpu']) > MAX_HISTORY:
                        container_history[container_id]['cpu'] = container_history[container_id]['cpu'][-MAX_HISTORY:]
                    if len(container_history[container_id]['memory']) > MAX_HISTORY:
                        container_history[container_id]['memory'] = container_history[container_id]['memory'][-MAX_HISTORY:]
                    
                    image_name = container.attrs.get('Config', {}).get('Image', '') or str(container.image)
                    
                    container_stats[container_id] = {
                        'id': container.id,
                        'short_id': container.short_id,
                        'name': container.name,
                        'image': image_name,
                        'status': container.status,
                        'state': container.attrs.get('State', {}).get('Status', 'unknown'),
                        'created': container.attrs.get('Created', ''),
                        'ports': get_ports(container),
                        'directories': get_directories(container),
                        'storage_used': get_storage_used(container),
                        'stats': stats,
                        'history': container_history[container_id]
                    }
                except Exception as e:
                    logger.error(f"Error getting container {container.name}: {e}")
        except Exception as e:
            logger.error(f"Error connecting to Docker: {e}")
        
        time.sleep(3)

collector_thread = threading.Thread(target=collect_container_data, daemon=True)
collector_thread.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/containers')
def get_containers():
    network = request.args.get('network', '')
    sort_by = request.args.get('sort_by', 'name')
    sort_order = request.args.get('sort_order', 'asc')
    
    containers = list(container_stats.values())
    
    if network:
        try:
            net = docker_client.networks.get(network)
            container_names = [c.attrs['Name'] for c in net.containers]
            containers = [c for c in containers if c['name'].lstrip('/') in container_names]
        except:
            pass
    
    def get_sort_key(c):
        name = c.get('name', '')
        if sort_by == 'name':
            return name.lower()
        elif sort_by == 'status':
            return c.get('state', '')
        elif sort_by == 'cpu':
            return c.get('stats', {}).get('cpu_percent', 0)
        elif sort_by == 'ram':
            return c.get('stats', {}).get('memory_percent', 0)
        elif sort_by == 'storage':
            return c.get('storage_used', 0)
        elif sort_by == 'date':
            return c.get('created', '')
        return name.lower()
    
    containers.sort(key=get_sort_key, reverse=(sort_order == 'desc'))
    
    for c in containers:
        c['storage_display'] = format_bytes(c.get('storage_used', 0))
        c['memory_display'] = format_bytes(c.get('stats', {}).get('memory_used', 0))
        c['memory_limit_display'] = format_bytes(c.get('stats', {}).get('memory_limit', 1))
        c['history_json'] = json.dumps(c.get('history', {'cpu': [], 'memory': []}))
    
    return jsonify(containers)

@app.route('/api/networks')
def get_networks():
    try:
        networks = docker_client.networks.list()
        return jsonify([{'id': n.id, 'name': n.name} for n in networks])
    except:
        return jsonify([])

@app.route('/api/networks/<network_id>')
def get_network_containers(network_id):
    try:
        net = docker_client.networks.get(network_id)
        containers = net.containers
        return jsonify([{'id': c.attrs['Id'], 'name': c.attrs['Name']} for c in containers])
    except:
        return jsonify([])

@app.route('/api/status')
def get_status():
    return jsonify({
        'container_count': len(container_stats),
        'containers': [{'name': c['name'], 'state': c['state']} for c in container_stats.values()]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
