#!/bin/bash

echo "🚀 SnapStudio Cloudflare Deployment Workflow"
echo "============================================="

# Check if we're in the right directory
if [ ! -f "web_app.py" ]; then
    echo "❌ Please run this script from the SnapStudio root directory"
    exit 1
fi

# Function to show usage
show_usage() {
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  dev          - Start local development server"
    echo "  build        - Build container image"
    echo "  test         - Test container locally"
    echo "  deploy       - Deploy to Cloudflare (requires tunnel setup)"
    echo "  update       - Update existing deployment"
    echo "  logs         - View container logs"
    echo "  stop         - Stop local container"
    echo "  status       - Check deployment status"
    echo ""
    echo "Examples:"
    echo "  $0 dev       # Start local development"
    echo "  $0 build     # Build container for deployment"
    echo "  $0 deploy    # Deploy to Cloudflare"
    echo ""
}

# Function to start local development
start_dev() {
    echo "🔧 Starting local development server..."
    echo "   Make sure to stop any running containers first:"
    echo "   podman stop snapstudio-app 2>/dev/null || true"
    echo ""
    echo "Starting Flask development server on port 5001..."
    python3 web_app.py
}

# Function to build container
build_container() {
    echo "🔨 Building SnapStudio container..."
    
    # Check if podman is available
    if command -v podman &> /dev/null; then
        CONTAINER_CMD="podman"
    elif command -v docker &> /dev/null; then
        CONTAINER_CMD="docker"
    else
        echo "❌ Neither Podman nor Docker found"
        exit 1
    fi
    
    echo "Using: $CONTAINER_CMD"
    
    # Build the image
    $CONTAINER_CMD build -t snapstudio:latest .
    
    if [ $? -eq 0 ]; then
        echo "✅ Container built successfully!"
        echo "   Image: snapstudio:latest"
    else
        echo "❌ Container build failed"
        exit 1
    fi
}

# Function to test container locally
test_container() {
    echo "🧪 Testing container locally..."
    
    # Stop existing container
    podman stop snapstudio-app 2>/dev/null || true
    podman rm snapstudio-app 2>/dev/null || true
    
    # Start container
    podman run -d \
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
    
    # Wait for startup
    echo "⏳ Waiting for container to start..."
    sleep 10
    
    # Test health endpoint
    if curl -s http://localhost:5001/health > /dev/null; then
        echo "✅ Container is running and healthy!"
        echo "🌐 Local URL: http://localhost:5001"
        echo "📊 Health check: http://localhost:5001/health"
    else
        echo "❌ Container failed to start"
        podman logs snapstudio-app
        exit 1
    fi
}

# Function to deploy to Cloudflare
deploy_to_cloudflare() {
    echo "🌐 Deploying to Cloudflare..."
    
    # Check if tunnel token is set
    if [ ! -f ".env" ] || ! grep -q "CLOUDFLARE_TUNNEL_TOKEN" .env; then
        echo "❌ Cloudflare tunnel token not found in .env"
        echo ""
        echo "Please set up Cloudflare tunnel first:"
        echo "1. Go to Cloudflare Dashboard → Zero Trust → Access → Tunnels"
        echo "2. Create a new tunnel named 'snapstudio-tunnel'"
        echo "3. Configure public hostname: snapstudio.cc"
        echo "4. Set service: http://localhost:5001"
        echo "5. Copy the tunnel token"
        echo "6. Add to .env: CLOUDFLARE_TUNNEL_TOKEN=your-token-here"
        exit 1
    fi
    
    # Ensure container is running
    if ! podman ps | grep -q snapstudio-app; then
        echo "🔄 Starting container..."
        test_container
    fi
    
    # Start Cloudflare tunnel
    echo "🌐 Starting Cloudflare tunnel..."
    echo "   Make sure cloudflared is installed: brew install cloudflared"
    echo ""
    
    # Extract token from .env
    TUNNEL_TOKEN=$(grep "CLOUDFLARE_TUNNEL_TOKEN" .env | cut -d'=' -f2)
    
    echo "Starting tunnel with token..."
    cloudflared tunnel run --token "$TUNNEL_TOKEN" &
    TUNNEL_PID=$!
    
    echo "✅ Deployment started!"
    echo "   Container: snapstudio-app (localhost:5001)"
    echo "   Tunnel PID: $TUNNEL_PID"
    echo "   Public URL: https://snapstudio.cc"
    echo ""
    echo "To stop tunnel: kill $TUNNEL_PID"
    echo "To stop container: podman stop snapstudio-app"
}

# Function to update deployment
update_deployment() {
    echo "🔄 Updating deployment..."
    
    # Build new container
    build_container
    
    # Stop existing container
    podman stop snapstudio-app 2>/dev/null || true
    podman rm snapstudio-app 2>/dev/null || true
    
    # Start new container
    test_container
    
    echo "✅ Deployment updated!"
    echo "   New container is running on localhost:5001"
    echo "   Cloudflare tunnel will automatically use the new container"
}

# Function to view logs
view_logs() {
    echo "📋 Container logs:"
    podman logs -f snapstudio-app
}

# Function to stop container
stop_container() {
    echo "🛑 Stopping SnapStudio container..."
    podman stop snapstudio-app 2>/dev/null || true
    podman rm snapstudio-app 2>/dev/null || true
    echo "✅ Container stopped"
}

# Function to check status
check_status() {
    echo "📊 Deployment Status"
    echo "==================="
    
    # Check container status
    if podman ps | grep -q snapstudio-app; then
        echo "✅ Container: Running (snapstudio-app)"
        echo "🌐 Local URL: http://localhost:5001"
        
        # Test health
        if curl -s http://localhost:5001/health > /dev/null; then
            echo "💚 Health: Healthy"
        else
            echo "💔 Health: Unhealthy"
        fi
    else
        echo "❌ Container: Not running"
    fi
    
    # Check tunnel status
    if pgrep -f "cloudflared tunnel" > /dev/null; then
        echo "🌐 Tunnel: Running"
        echo "🔗 Public URL: https://snapstudio.cc"
    else
        echo "❌ Tunnel: Not running"
    fi
}

# Main script logic
case "${1:-}" in
    "dev")
        start_dev
        ;;
    "build")
        build_container
        ;;
    "test")
        test_container
        ;;
    "deploy")
        deploy_to_cloudflare
        ;;
    "update")
        update_deployment
        ;;
    "logs")
        view_logs
        ;;
    "stop")
        stop_container
        ;;
    "status")
        check_status
        ;;
    *)
        show_usage
        ;;
esac
