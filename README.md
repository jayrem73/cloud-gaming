![Cloud Gaming Hub](https://img.shields.io/badge/Cloud%20Gaming-Hub%20v1.0-blue)
![Status](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-MIT-green)

# ☁️ Cloud Gaming Hub + Proxy Search Engine

A full-featured web application for cloud gaming sessions and proxy searching. Built with HTML5, JavaScript, and Flask backend.

## 🚀 Live Demo

**Frontend:** https://jayrem73.github.io/cloud-gaming
**Backend API:** Deploy on Replit (instructions below)

## ✨ Features

### 🎮 Cloud Gaming Console
- Launch game sessions from your browser
- Select from multiple games (Fortnite, Call of Duty, Cyberpunk 2077, Elden Ring, The Witcher 3)
- Choose server regions (US-East, US-West, EU, Asia, Australia)
- Adjust graphics quality (4K Ultra, 1440p High, 1080p Medium, 720p Low)
- Real-time session monitoring with latency and FPS stats
- Live session counter and performance metrics

### 🔍 Proxy Search Engine
- Search through thousands of active proxies
- Filter by proxy type (HTTP, HTTPS, SOCKS5)
- Filter by country location
- Real-time speed metrics
- One-click copy-to-clipboard functionality
- Dual proxy API sources for redundancy
- Average speed calculations

### 📊 Dashboard
- Beautiful glassmorphic UI with gradients
- Responsive design (desktop & mobile)
- Real-time API status indicators
- Performance stats dashboard
- Smooth animations and transitions

## 🛠️ Tech Stack

**Frontend:**
- HTML5
- CSS3 (Glassmorphism, Gradients, Animations)
- Vanilla JavaScript (ES6+)

**Backend:**
- Python 3
- Flask
- Flask-CORS
- Requests library

**Hosting:**
- GitHub Pages (Frontend)
- Replit (Backend API)

## 📋 Project Structure

```
cloud-gaming/
├── index.html          # Main web interface
├── app.js              # Frontend JavaScript logic
├── server.py           # Flask backend API
├── requirements.txt    # Python dependencies
├── .replit             # Replit configuration
└── README.md           # This file
```

## 🚀 Quick Start

### Step 1: Frontend is Already Live!
Your site is live at: **https://jayrem73.github.io/cloud-gaming**

### Step 2: Deploy Backend on Replit

1. Go to https://replit.com and sign in
2. Click **"Create Repl"** → Select **"Import from GitHub"**
3. Enter: `jayrem73/cloud-gaming`
4. Click **"Run"** button to start the server
5. Copy your Replit URL (looks like: `https://cloud-gaming.jayrem73.repl.co`)
6. Edit `app.js` line 2 and update `API_BASE_URL` with your Replit URL:
   ```javascript
   const API_BASE_URL = 'https://your-project.jayrem73.repl.co';
   ```
7. Push the change to GitHub

## 🔌 API Endpoints

### Base URL
```
https://your-replit-url.repl.co
```

### Endpoints

#### Health Check
```
GET /api/status
```
Response:
```json
{
  "status": "online",
  "service": "Cloud Gaming API",
  "timestamp": "2024-01-15T10:30:00",
  "version": "1.0.0"
}
```

#### Launch Game Session
```
POST /api/game-launch
Content-Type: application/json

{
  "game": "Fortnite",
  "region": "US - East",
  "quality": "Ultra (4K @ 60fps)"
}
```
Response:
```json
{
  "status": "success",
  "session_id": "uuid-string",
  "game": "Fortnite",
  "region": "US - East",
  "server_ip": "game-us-east.cloud-gaming.io",
  "port": 8080,
  "message": "Game session launched successfully"
}
```

#### Search Proxies
```
GET /api/search-proxies?q=http&type=HTTP&country=United%20States
```
Response:
```json
{
  "status": "success",
  "count": 20,
  "proxies": [
    {
      "ip": "103.145.57.140",
      "port": "8080",
      "type": "HTTP",
      "speed": "45",
      "country": "United States"
    }
  ]
}
```

#### Get Available Games
```
GET /api/games
```

#### Get Available Regions
```
GET /api/game-regions
```

#### Get Proxy Types
```
GET /api/proxy-types
```

#### Get Countries
```
GET /api/countries
```

## 🎨 UI Features

- **Glassmorphic Design:** Modern frosted glass effect backgrounds
- **Gradient Text:** Eye-catching animated headers
- **Smooth Animations:** Slide-in and fade effects
- **Responsive Layout:** Works on desktop, tablet, and mobile
- **Dark Theme:** Eye-friendly dark mode throughout
- **Status Indicators:** Real-time connection status
- **Copy to Clipboard:** One-click proxy copying
- **Performance Metrics:** Live stats dashboard

## 🔧 Configuration

### Update API URL
Edit `app.js` line 2:
```javascript
const API_BASE_URL = 'https://your-replit-url.repl.co';
```

### Add More Games
Edit `server.py`:
```python
MOCK_GAMES = ["Fortnite", "Your Game"]
```

### Add More Regions
Edit `server.py`:
```python
MOCK_REGIONS = ["Region 1", "Region 2"]
```

## 🔐 Security Notes

⚠️ **Important:**
- This is a demonstration project
- Proxy sources are from free public APIs
- Use responsibly and follow local laws
- Never use proxies for illegal activities
- Always respect websites' terms of service

## 📈 Performance

- **Frontend Load Time:** < 2 seconds
- **API Response Time:** < 1 second
- **Proxy Search Speed:** < 2 seconds
- **Mobile Optimized:** Responsive design

## 🤝 Contributing

Feel free to fork and submit pull requests!

### Areas for Enhancement:
- Real game server integration
- User authentication system
- Database for proxy validation
- Advanced filtering options
- Payment integration
- Real-time multiplayer support

## 📝 License

MIT License - Feel free to use for personal and commercial projects

## 👨‍💻 Author

**jayrem73** - Cloud Gaming & Proxy Search Platform

## 🎯 Roadmap

- [ ] User accounts and authentication
- [ ] Proxy validation and uptime tracking
- [ ] Game library expansion
- [ ] Advanced analytics dashboard
- [ ] Mobile app version
- [ ] Real cloud gaming integration (NVIDIA GeForce NOW API)
- [ ] Discord bot integration
- [ ] Multiplayer session support

## 📞 Support

For issues or questions:
1. Check existing GitHub issues
2. Create a new issue with details
3. Include screenshots and error logs

## 🙏 Acknowledgments

- Proxy data from free public APIs
- Flask community for excellent documentation
- GitHub Pages for free hosting

---

**Made with ❤️ by jayrem73**

Last Updated: September 2026