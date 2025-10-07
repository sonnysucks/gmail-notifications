#!/bin/bash

echo "🐳 Deploying SnapStudio to Cloudflare with Podman/Docker"
echo "========================================================"

# Check if podman is installed
if command -v podman &> /dev/null; then
    CONTAINER_CMD="podman"
    echo "✅ Using Podman"
elif command -v docker &> /dev/null; then
    CONTAINER_CMD="docker"
    echo "✅ Using Docker"
else
    echo "❌ Neither Podman nor Docker found. Please install one of them."
    exit 1
fi

# Check if cloudflared is installed
if ! command -v cloudflared &> /dev/null; then
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

# Create environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cat > .env << EOF
# SnapStudio Environment Variables
SECRET_KEY=$(openssl rand -hex 32)
CLOUDFLARE_TUNNEL_TOKEN=your-tunnel-token-here
EOF
    echo "⚠️  Please update .env with your Cloudflare tunnel token"
fi

# Build the container
echo "🔨 Building SnapStudio container..."
$CONTAINER_CMD build -t snapstudio:latest .

if [ $? -ne 0 ]; then
    echo "❌ Container build failed"
    exit 1
fi

# Stop existing containers
echo "🛑 Stopping existing containers..."
$CONTAINER_CMD stop snapstudio-app snapstudio-tunnel 2>/dev/null || true
$CONTAINER_CMD rm snapstudio-app snapstudio-tunnel 2>/dev/null || true

# Create necessary directories
mkdir -p data logs uploads exports backups

# Start the application container
echo "🚀 Starting SnapStudio application..."
$CONTAINER_CMD run -d \
    --name snapstudio-app \
    --restart unless-stopped \
    -p 5001:5001 \
    -v $(pwd)/data:/app/data \
    -v $(pwd)/logs:/app/logs \
    -v $(pwd)/uploads:/app/uploads \
    -v $(pwd)/exports:/app/exports \
    -v $(pwd)/backups:/app/backups \
    -e FLASK_ENV=production \
    -e DATABASE_URL=sqlite:////app/data/web_app.db \
    --env-file .env \
    snapstudio:latest

if [ $? -ne 0 ]; then
    echo "❌ Failed to start SnapStudio container"
    exit 1
fi

# Wait for app to start
echo "⏳ Waiting for application to start..."
sleep 10

# Check if app is running
if curl -s http://localhost:5001/health > /dev/null; then
    echo "✅ SnapStudio application is running!"
    echo "🌐 Local URL: http://localhost:5001"
else
    echo "❌ Application failed to start"
    $CONTAINER_CMD logs snapstudio-app
    exit 1
fi

# Start Cloudflare tunnel
echo "🌐 Starting Cloudflare tunnel..."
echo "⚠️  Make sure to:"
echo "   1. Create a Cloudflare tunnel token"
echo "   2. Update CLOUDFLARE_TUNNEL_TOKEN in .env"
echo "   3. Run: cloudflared tunnel run --token YOUR_TOKEN"
echo ""
echo "📋 Manual tunnel setup:"
echo "   1. Go to Cloudflare dashboard"
echo "   2. Create a tunnel"
echo "   3. Configure it to point to localhost:5001"
echo "   4. Get the tunnel token and update .env"
echo ""
echo "🎉 SnapStudio is ready for Cloudflare deployment!"
echo "   Container: snapstudio-app"
echo "   Local URL: http://localhost:5001"
echo "   Next: Set up Cloudflare tunnel"
