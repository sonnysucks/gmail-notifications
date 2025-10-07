# SnapStudio Cloudflare Container Deployment Guide

## 🐳 Containerized Deployment to Cloudflare

This guide shows how to deploy your SnapStudio Python Flask application as a container and connect it to Cloudflare using Cloudflare Tunnel.

## 📋 Prerequisites

- Podman or Docker installed
- Cloudflare account
- Domain managed by Cloudflare

## 🚀 Quick Deployment

### 1. Deploy Container

```bash
./deploy-container.sh
```

This will:
- Build your SnapStudio container
- Start the application on port 5000
- Set up necessary directories
- Create environment file

### 2. Set Up Cloudflare Tunnel

#### Option A: Using Cloudflare Dashboard (Recommended)

1. **Go to Cloudflare Dashboard**
   - Navigate to your domain
   - Go to "Zero Trust" → "Access" → "Tunnels"

2. **Create a Tunnel**
   - Click "Create a tunnel"
   - Name it "snapstudio-tunnel"
   - Copy the tunnel token

3. **Configure Tunnel**
   - Add a public hostname: `snapstudio.cc`
   - Set service: `http://localhost:5000`
   - Save configuration

4. **Update Environment**
   ```bash
   # Edit .env file
   CLOUDFLARE_TUNNEL_TOKEN=your-tunnel-token-here
   ```

5. **Start Tunnel**
   ```bash
   cloudflared tunnel run --token YOUR_TUNNEL_TOKEN
   ```

#### Option B: Using Docker Compose

```bash
# Update .env with your tunnel token
echo "CLOUDFLARE_TUNNEL_TOKEN=your-token" >> .env

# Start both app and tunnel
docker-compose up -d
```

## 🔧 Manual Setup

### Build Container
```bash
podman build -t snapstudio:latest .
# or
docker build -t snapstudio:latest .
```

### Run Container
```bash
podman run -d \
  --name snapstudio-app \
  -p 5000:5000 \
  -v $(pwd)/data:/app/data \
  -e FLASK_ENV=production \
  snapstudio:latest
```

### Test Locally
```bash
curl http://localhost:5000/health
```

## 🌐 Cloudflare Configuration

### DNS Settings
- Ensure your domain points to Cloudflare
- Tunnel will handle routing automatically

### Security Features
- **DDoS Protection**: Automatic
- **SSL/TLS**: Automatic HTTPS
- **WAF**: Available in Cloudflare dashboard
- **Rate Limiting**: Configure in Cloudflare dashboard

## 📊 Monitoring

### Health Checks
- Container health check: `/health` endpoint
- Cloudflare tunnel status: Dashboard monitoring
- Application logs: `podman logs snapstudio-app`

### Logs
```bash
# Application logs
podman logs -f snapstudio-app

# Tunnel logs
cloudflared tunnel run --token YOUR_TOKEN --loglevel debug
```

## 🔄 Updates

### Update Application
```bash
# Stop container
podman stop snapstudio-app

# Rebuild with new code
podman build -t snapstudio:latest .

# Start new container
podman start snapstudio-app
```

### Update Tunnel
- Tunnel updates automatically
- No restart needed for application updates

## 🛠️ Troubleshooting

### Container Issues
```bash
# Check container status
podman ps

# Check logs
podman logs snapstudio-app

# Restart container
podman restart snapstudio-app
```

### Tunnel Issues
```bash
# Test tunnel connection
cloudflared tunnel run --token YOUR_TOKEN --loglevel debug

# Check tunnel status in Cloudflare dashboard
```

### Database Issues
```bash
# Check database file
ls -la data/web_app.db

# Reset database (WARNING: loses data)
rm data/web_app.db
podman restart snapstudio-app
```

## 🎯 Benefits

✅ **Global CDN**: Fast access worldwide  
✅ **Automatic SSL**: HTTPS everywhere  
✅ **DDoS Protection**: Built-in security  
✅ **Container Benefits**: Consistent deployment  
✅ **Easy Updates**: Simple container rebuild  
✅ **Monitoring**: Cloudflare analytics  

## 📝 Environment Variables

```bash
# .env file
SECRET_KEY=your-secret-key
CLOUDFLARE_TUNNEL_TOKEN=your-tunnel-token
FLASK_ENV=production
DATABASE_URL=sqlite:////app/data/web_app.db
```

## 🚀 Production Checklist

- [ ] Update SECRET_KEY in .env
- [ ] Set up Cloudflare tunnel
- [ ] Configure custom domain
- [ ] Enable Cloudflare security features
- [ ] Set up monitoring
- [ ] Test all application features
- [ ] Configure backups

Your SnapStudio application is now running as a container and accessible worldwide through Cloudflare! 🌍📸
