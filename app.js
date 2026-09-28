// Configuration
const API_BASE_URL = 'https://cloud-gaming-api.jayrem73.repl.co';
let gameSessionActive = false;
let gameSessionTimer = null;

// Cloud Gaming Functions
async function launchGame() {
    const game = document.getElementById('gameSelect').value;
    const region = document.getElementById('serverRegion').value;
    const quality = document.getElementById('quality').value;
    const statusDiv = document.getElementById('gameStatus');
    const statsDiv = document.getElementById('gameStats');

    statusDiv.innerHTML = '<div class="status-box active"><div class="loading"></div> Initializing game server...</div>';

    try {
        // Call backend API
        const response = await fetch(`${API_BASE_URL}/api/game-launch`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ game, region, quality })
        });

        if (!response.ok) throw new Error('API Error');
        
        const data = await response.json();

        gameSessionActive = true;
        statsDiv.style.display = 'grid';

        statusDiv.innerHTML = `
            <div class="status-box active">
                ✅ Game Session Active!
            </div>
            <div class="game-server-info">
                <strong>Server Details:</strong><br>
                Game: ${data.game}<br>
                Region: ${data.region}<br>
                Server IP: ${data.server_ip}<br>
                Port: ${data.port}<br>
                Session ID: ${data.session_id}<br>
                Status: <span style="color:#00ff00;">🟢 ONLINE</span>
            </div>
            <button onclick="stopGame()" style="background:linear-gradient(45deg, #ff4444, #ff0000);">🛑 Stop Game</button>
        `;

        // Simulate game stats updates
        let uptime = 0;
        let latency = 15;
        gameSessionTimer = setInterval(() => {
            uptime++;
            latency = 15 + Math.random() * 10;
            document.getElementById('statUptime').textContent = uptime + 's';
            document.getElementById('statLatency').textContent = Math.round(latency) + 'ms';
            document.getElementById('statFPS').textContent = '60';
        }, 1000);

    } catch (error) {
        statusDiv.innerHTML = `<div class="error-box active">❌ Error: ${error.message}<br>Make sure backend is running</div>`;
        console.error('Game launch error:', error);
    }
}

function stopGame() {
    gameSessionActive = false;
    clearInterval(gameSessionTimer);
    document.getElementById('gameStatus').innerHTML = '<div class="status-box" style="background:rgba(255, 100, 0, 0.1);border-color:#ff6400;color:#ff9900;">⏸️ Game session stopped</div>';
    document.getElementById('gameStats').style.display = 'none';
}

// Proxy Search Functions
async function searchProxies() {
    const query = document.getElementById('searchQuery').value || 'http';
    const type = document.getElementById('proxyType').value;
    const country = document.getElementById('country').value;
    const resultsDiv = document.getElementById('proxyResults');
    const statsDiv = document.getElementById('proxyStats');

    resultsDiv.innerHTML = '<div class="status-box active"><div class="loading"></div> Searching proxies...</div>';

    try {
        const response = await fetch(`${API_BASE_URL}/api/search-proxies?q=${encodeURIComponent(query)}&type=${type}&country=${country}`);
        
        if (!response.ok) throw new Error('API Error');
        
        const data = await response.json();

        if (data.proxies && data.proxies.length > 0) {
            let html = '';
            let totalSpeed = 0;

            data.proxies.forEach((proxy, index) => {
                const speed = parseInt(proxy.speed) || 0;
                totalSpeed += speed;

                html += `
                    <div class="result">
                        <strong>${proxy.ip}:${proxy.port}</strong>
                        <div class="result-row">
                            <div>Type: ${proxy.type}</div>
                            <div>Speed: ${proxy.speed}ms</div>
                            <div>Country: ${proxy.country}</div>
                            <div>Status: <span style="color:#00ff00;">✓ Active</span></div>
                        </div>
                        <div style="margin-top:10px; font-size:0.85em;">
                            <button onclick="copyToClipboard('${proxy.ip}:${proxy.port}')" style="width:100%; margin:5px 0;">📋 Copy</button>
                        </div>
                    </div>
                `;
            });

            resultsDiv.innerHTML = html;
            statsDiv.style.display = 'grid';
            document.getElementById('statFound').textContent = data.proxies.length;
            document.getElementById('statAverage').textContent = Math.round(totalSpeed / data.proxies.length) + 'ms';

        } else {
            resultsDiv.innerHTML = '<div class="error-box active">⚠️ No proxies found. Try a different search term.</div>';
            statsDiv.style.display = 'none';
        }

    } catch (error) {
        resultsDiv.innerHTML = `<div class="error-box active">❌ Error: ${error.message}<br>Backend API may be offline. Check console for details.</div>`;
        console.error('Proxy search error:', error);
    }
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        alert('Copied to clipboard: ' + text);
    });
}

// Check API status on load
window.addEventListener('load', async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/api/status`);
        if (response.ok) {
            document.getElementById('apiStatus').textContent = 'Connected';
            document.getElementById('apiStatus').style.color = '#00ff00';
            document.getElementById('proxyApiStatus').textContent = 'Ready';
            document.getElementById('proxyApiStatus').style.color = '#00ff00';
        }
    } catch {
        document.getElementById('apiStatus').textContent = 'Offline - Local Mode';
        document.getElementById('apiStatus').style.color = '#ff9900';
        document.getElementById('proxyApiStatus').textContent = 'Offline - Using Mock Data';
        document.getElementById('proxyApiStatus').style.color = '#ff9900';
    }
});

// Allow Enter key to search
document.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        if (document.activeElement.id === 'searchQuery') {
            searchProxies();
        }
    }
});