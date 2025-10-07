#!/bin/bash

echo "🐍 Deploying SnapStudio Python Flask App via Cloudflare Tunnel"
echo "=============================================================="

# Check if cloudflared is installed
if ! command -v cloudflared &> /dev/null
then
    echo "📦 Installing Cloudflare Tunnel (cloudflared)..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        brew install cloudflared
    else
        # Linux
        wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
        sudo dpkg -i cloudflared-linux-amd64.deb
    fi
fi

# Check if Flask app is running
echo "🔍 Checking if Flask app is running..."
if ! curl -s http://localhost:5000 > /dev/null; then
    echo "⚠️  Flask app not running. Starting it..."
    echo "🚀 Starting your Python Flask SnapStudio app..."
    
    # Start Flask app in background
    /usr/bin/python3 web_app.py &
    FLASK_PID=$!
    
    # Wait for Flask to start
    echo "⏳ Waiting for Flask app to start..."
    sleep 5
    
    # Check if it's running
    if curl -s http://localhost:5000 > /dev/null; then
        echo "✅ Flask app started successfully (PID: $FLASK_PID)"
    else
        echo "❌ Failed to start Flask app"
        exit 1
    fi
else
    echo "✅ Flask app is already running on localhost:5000"
fi

echo ""
echo "🌐 Setting up Cloudflare Tunnel..."
echo "This will make your local Flask app accessible at https://snapstudio.cc"
echo ""

# Create tunnel configuration
cat > tunnel-config.yml << EOF
tunnel: snapstudio-tunnel
credentials-file: /Users/sonny/.cloudflared/$(uuidgen).json

ingress:
  - hostname: snapstudio.cc
    service: http://localhost:5000
  - hostname: www.snapstudio.cc
    service: http://localhost:5000
  - service: http_status:404
EOF

# Create credentials directory
mkdir -p ~/.cloudflared

# Create tunnel
echo "🔧 Creating Cloudflare tunnel..."
cloudflared tunnel create snapstudio-tunnel

# Configure tunnel
echo "⚙️  Configuring tunnel..."
cloudflared tunnel route dns snapstudio-tunnel snapstudio.cc
cloudflared tunnel route dns snapstudio-tunnel www.snapstudio.cc

echo ""
echo "🚀 Starting Cloudflare tunnel..."
echo "Your Flask app will be accessible at: https://snapstudio.cc"
echo ""
echo "Press Ctrl+C to stop the tunnel"
echo ""

# Start tunnel
cloudflared tunnel run snapstudio-tunnel
