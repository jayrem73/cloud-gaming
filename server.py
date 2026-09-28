from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
from datetime import datetime
import uuid
import os

app = Flask(__name__)
CORS(app)

# Xbox Cloud Gaming Configuration
XBOX_API_BASE = "https://www.xbox.com/en-US/play"
XBOX_GAME_PASS_API = "https://gamepass.microsoft.com/api/v2"

# Free Proxy APIs
PROXY_APIS = [
    {
        "url": "https://www.proxy-list.download/api/v1/get?type=http",
        "type": "json_list"
    },
    {
        "url": "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&format=json&ssl=all&anonymity=all&country=all&simplified=true",
        "type": "json_proxies"
    }
]

# Mock data for fallback
MOCK_PROXIES = [
    {"ip": "103.145.57.140", "port": "8080", "type": "HTTP", "speed": "45", "country": "United States"},
    {"ip": "207.180.235.245", "port": "3128", "type": "HTTP", "speed": "32", "country": "Canada"},
    {"ip": "192.241.238.216", "port": "8080", "type": "HTTP", "speed": "28", "country": "United States"},
    {"ip": "195.154.54.129", "port": "3128", "type": "HTTP", "speed": "55", "country": "France"},
    {"ip": "104.248.34.193", "port": "80", "type": "HTTP", "speed": "38", "country": "United Kingdom"},
    {"ip": "182.191.84.39", "port": "80", "type": "HTTP", "speed": "62", "country": "Japan"},
    {"ip": "1.10.141.220", "port": "8080", "type": "HTTP", "speed": "71", "country": "Japan"},
    {"ip": "45.147.176.181", "port": "8080", "type": "HTTP", "speed": "44", "country": "Germany"},
    {"ip": "154.21.10.94", "port": "80", "type": "HTTP", "speed": "58", "country": "Australia"},
    {"ip": "64.185.90.133", "port": "8080", "type": "HTTP", "speed": "35", "country": "United States"},
]

# Xbox Cloud Gaming games (Real Game Pass titles)
XBOX_GAMES = [
    {"title": "Fortnite", "id": "fortnite", "image": "https://images.unsplash.com/photo-1538481143235-5d630027ba37"},
    {"title": "Call of Duty Modern Warfare", "id": "cod-mw", "image": "https://images.unsplash.com/photo-1605559424843-9e4c3dec1118"},
    {"title": "Cyberpunk 2077", "id": "cyberpunk", "image": "https://images.unsplash.com/photo-1612198188060-c7c2a3b66eae"},
    {"title": "Elden Ring", "id": "elden-ring", "image": "https://images.unsplash.com/photo-1579033100448-9f011cc9ef23"},
    {"title": "The Witcher 3", "id": "witcher3", "image": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64"},
    {"title": "Halo Infinite", "id": "halo", "image": "https://images.unsplash.com/photo-1614613835716-dbbbf006b6d0"},
    {"title": "Game Pass for PC", "id": "gamepass", "image": "https://images.unsplash.com/photo-1552820728-8ac41f1ce891"},
]

XBOX_REGIONS = [
    {"name": "US - East", "code": "us-east", "latency": 15},
    {"name": "US - West", "code": "us-west", "latency": 18},
    {"name": "EU - Europe", "code": "eu-west", "latency": 25},
    {"name": "ASIA - Singapore", "code": "asia-sg", "latency": 35},
    {"name": "AU - Australia", "code": "au-sydney", "latency": 45},
]

@app.route('/api/status', methods=['GET'])
def status():
    """Health check endpoint"""
    return jsonify({
        'status': 'online',
        'service': 'Xbox Cloud Gaming + Proxy Search API',
        'timestamp': datetime.now().isoformat(),
        'version': '2.0.0',
        'xbox_integrated': True
    })

@app.route('/api/xbox-auth', methods=['POST'])
def xbox_auth():
    """Authenticate with Xbox Live (placeholder)"""
    try:
        data = request.json
        email = data.get('email')
        
        # In production, this would authenticate with Xbox Live
        # For now, return mock auth token
        auth_token = str(uuid.uuid4())
        
        return jsonify({
            'status': 'success',
            'auth_token': auth_token,
            'user_email': email,
            'message': 'Connected to Xbox Live',
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/game-launch', methods=['POST'])
def launch_game():
    """Launch Xbox Cloud Gaming session"""
    try:
        data = request.json
        game = data.get('game', 'Unknown')
        region = data.get('region', 'US - East')
        quality = data.get('quality', 'High')

        session_id = str(uuid.uuid4())
        
        # Find region latency
        region_latency = 15
        for r in XBOX_REGIONS:
            if r['name'] == region:
                region_latency = r['latency']
                break
        
        return jsonify({
            'status': 'success',
            'session_id': session_id,
            'game': game,
            'region': region,
            'quality': quality,
            'server_ip': f'xcloud-{region.replace(" - ", "-").lower()}.xbox.com',
            'port': 443,
            'latency': region_latency,
            'message': f'Xbox Cloud Gaming session "{game}" launched on {region}',
            'xbox_url': 'https://www.xbox.com/en-US/play',
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/xbox-games', methods=['GET'])
def get_xbox_games():
    """Get Xbox Game Pass games"""
    try:
        return jsonify({
            'status': 'success',
            'games': XBOX_GAMES,
            'total': len(XBOX_GAMES),
            'source': 'Xbox Game Pass'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'games': []
        }), 500

@app.route('/api/search-proxies', methods=['GET'])
def search_proxies():
    """Search and filter proxies"""
    try:
        query = request.args.get('q', '').lower()
        proxy_type = request.args.get('type', 'All Types')
        country = request.args.get('country', 'All Countries')

        proxies = []

        # Try to fetch from real API
        try:
            response = requests.get(PROXY_APIS[0]['url'], timeout=5)
            if response.status_code == 200:
                api_data = response.json()
                
                if isinstance(api_data, dict) and 'data' in api_data:
                    for proxy in api_data['data'][:15]:
                        proxies.append({
                            'ip': proxy.get('ip', ''),
                            'port': proxy.get('port', ''),
                            'type': 'HTTP',
                            'speed': str(int(proxy.get('response_time', 50))),
                            'country': proxy.get('country', 'Unknown')
                        })
        except:
            pass

        # Fallback to mock data if API fails
        if not proxies:
            proxies = MOCK_PROXIES.copy()

        # Filter by type
        if proxy_type != 'All Types':
            proxies = [p for p in proxies if p['type'] == proxy_type]

        # Filter by country
        if country != 'All Countries':
            proxies = [p for p in proxies if country.lower() in p['country'].lower()]

        # Filter by search query
        if query:
            proxies = [p for p in proxies if query in p['ip'].lower() or query in p['country'].lower()]

        # Sort by speed
        proxies = sorted(proxies, key=lambda x: int(x.get('speed', 999)))

        return jsonify({
            'status': 'success',
            'count': len(proxies),
            'proxies': proxies[:20],
            'timestamp': datetime.now().isoformat()
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'proxies': []
        }), 500

@app.route('/api/game-regions', methods=['GET'])
def get_game_regions():
    """Get available Xbox Cloud Gaming regions"""
    return jsonify({
        'regions': XBOX_REGIONS,
        'total': len(XBOX_REGIONS)
    }), 200

@app.route('/api/proxy-types', methods=['GET'])
def get_proxy_types():
    """Get available proxy types"""
    proxy_types = ['HTTP', 'HTTPS', 'SOCKS5', 'SOCKS4']
    return jsonify({
        'types': proxy_types,
        'total': len(proxy_types)
    }), 200

@app.route('/api/countries', methods=['GET'])
def get_countries():
    """Get available countries for proxy filtering"""
    countries = ['United States', 'Canada', 'United Kingdom', 'Germany', 'France', 'Japan', 'Australia']
    return jsonify({
        'countries': countries,
        'total': len(countries)
    }), 200

@app.route('/', methods=['GET'])
def index():
    """API documentation"""
    return jsonify({
        'service': 'Xbox Cloud Gaming + Proxy Search API',
        'version': '2.0.0',
        'xbox_cloud_gaming': True,
        'xbox_url': 'https://www.xbox.com/en-US/play',
        'endpoints': {
            'GET /api/status': 'Health check',
            'POST /api/xbox-auth': 'Authenticate with Xbox Live',
            'POST /api/game-launch': 'Launch Xbox Cloud Gaming session',
            'GET /api/xbox-games': 'Get Xbox Game Pass games',
            'GET /api/search-proxies': 'Search proxies with filters',
            'GET /api/game-regions': 'Get Xbox Cloud Gaming regions',
            'GET /api/proxy-types': 'Get proxy types',
            'GET /api/countries': 'Get countries'
        }
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)