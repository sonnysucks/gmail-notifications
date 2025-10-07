# SnapStudio Cloudflare Container Deployment Guide

## 🎯 Development + Production Workflow

This guide shows you how to maintain local development while deploying your containerized SnapStudio app to Cloudflare.

## 📋 Prerequisites

- **Local Development**: Python 3.9+, Flask dependencies
- **Container Deployment**: Podman or Docker
- **Cloudflare**: Account with domain managed by Cloudflare
- **Tunnel**: Cloudflare Tunnel for secure connection

## 🚀 Quick Start

### 1. Local Development
```bash
# Start local development server
./deploy.sh dev
```
- Runs Flask app directly on port 5001
- Hot reloading enabled
- Perfect for development and testing

### 2. Build Container
```bash
# Build container image
./deploy.sh build
```
- Creates `snapstudio:latest` image
- Includes all dependencies and optimizations
- Ready for production deployment

### 3. Test Container Locally
```bash
# Test container before deployment
./deploy.sh test
```
- Runs container on localhost:5001
- Tests all functionality
- Verifies health checks

### 4. Deploy to Cloudflare
```bash
# Deploy to Cloudflare (one-time setup required)
./deploy.sh deploy
```

## 🔧 One-Time Cloudflare Setup

### Step 1: Create Cloudflare Tunnel

1. **Go to Cloudflare Dashboard**
   - Navigate to your domain (snapstudio.cc)
   - Go to "Zero Trust" → "Access" → "Tunnels"

2. **Create Tunnel**
   - Click "Create a tunnel"
   - Name: `snapstudio-tunnel`
   - Copy the tunnel token (starts with `eyJ...`)

3. **Configure Public Hostname**
   - Public hostname: `snapstudio.cc`
   - Service: `http://localhost:5001`
   - Save configuration

### Step 2: Set Up Environment

```bash
# Create .env file with tunnel token
echo "CLOUDFLARE_TUNNEL_TOKEN=your-tunnel-token-here" >> .env
echo "SECRET_KEY=$(openssl rand -hex 32)" >> .env
```

### Step 3: Install Cloudflare Tunnel

```bash
# macOS
brew install cloudflared

# Linux
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb
```

## 🔄 Daily Workflow

### Development Mode
```bash
# Start local development
./deploy.sh dev

# Make changes to your code
# Flask auto-reloads on changes
# Test at http://localhost:5001
```

### Deploy Updates
```bash
# When ready to deploy updates
./deploy.sh update

# This will:
# 1. Build new container
# 2. Stop old container
# 3. Start new container
# 4. Tunnel automatically uses new container
```

### Check Status
```bash
# Check deployment status
./deploy.sh status

# View logs
./deploy.sh logs

# Stop everything
./deploy.sh stop
```

## 📊 Deployment Commands

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `./deploy.sh dev` | Local development | Daily coding |
| `./deploy.sh build` | Build container | Before deployment |
| `./deploy.sh test` | Test container | Before deploying |
| `./deploy.sh deploy` | Deploy to Cloudflare | First deployment |
| `./deploy.sh update` | Update deployment | After code changes |
| `./deploy.sh status` | Check status | Monitor deployment |
| `./deploy.sh logs` | View logs | Debug issues |
| `./deploy.sh stop` | Stop container | Cleanup |

## 🌐 Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Your Code     │    │   Container      │    │   Cloudflare    │
│                 │    │                  │    │                 │
│  web_app.py     │───▶│  snapstudio:    │───▶│  Tunnel         │
│  templates/     │    │  latest          │    │                 │
│  static/        │    │  Port: 5001      │    │  snapstudio.cc  │
│  data/          │    │  Health: /health │    │  HTTPS/SSL      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🔒 Security Features

- **Container Security**: Non-root user, minimal base image
- **Cloudflare Protection**: DDoS protection, WAF, SSL/TLS
- **Tunnel Security**: Encrypted connection, no open ports
- **Environment Variables**: Secrets in .env file

## 📈 Benefits

✅ **Local Development**: Fast iteration with Flask dev server  
✅ **Production Ready**: Containerized deployment  
✅ **Global CDN**: Fast access worldwide via Cloudflare  
✅ **Automatic SSL**: HTTPS everywhere  
✅ **Easy Updates**: Simple container rebuild  
✅ **No Server Management**: Cloudflare handles infrastructure  
✅ **Cost Effective**: Pay only for what you use  

## 🛠️ Troubleshooting

### Container Issues
```bash
# Check container status
podman ps

# View container logs
./deploy.sh logs

# Restart container
./deploy.sh stop
./deploy.sh test
```

### Tunnel Issues
```bash
# Check tunnel status
ps aux | grep cloudflared

# Restart tunnel
pkill cloudflared
./deploy.sh deploy
```

### Database Issues
```bash
# Check database
ls -la data/web_app.db

# Reset database (WARNING: loses data)
rm data/web_app.db
./deploy.sh update
```

## 📝 Environment Variables

```bash
# .env file
SECRET_KEY=your-secret-key-here
CLOUDFLARE_TUNNEL_TOKEN=your-tunnel-token-here
FLASK_ENV=production
DATABASE_URL=sqlite:////app/data/web_app.db
```

## 🎉 You're Ready!

Your SnapStudio application is now:
- ✅ **Containerized** and production-ready
- ✅ **Deployed** to Cloudflare with global CDN
- ✅ **Secure** with automatic SSL and DDoS protection
- ✅ **Maintainable** with simple update workflow

**Next Steps:**
1. Set up Cloudflare tunnel (one-time)
2. Use `./deploy.sh dev` for daily development
3. Use `./deploy.sh update` when ready to deploy changes
4. Monitor with `./deploy.sh status`

Happy coding! 🚀📸
