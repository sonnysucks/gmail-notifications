#!/bin/bash

# SnapStudio Podman Run Script
# Runs the SnapStudio Podman container

set -e

echo "🚀 Running SnapStudio Podman Container"
echo "======================================"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Podman is installed and running
if ! command -v podman &> /dev/null; then
    print_error "Podman is not installed. Please install Podman first."
    echo "macOS: brew install podman"
    echo "Linux: sudo dnf install podman (Fedora) or sudo apt install podman (Ubuntu)"
    exit 1
fi

if ! podman info &> /dev/null; then
    print_error "Podman is not running. Please start Podman machine first."
    echo "Run: podman machine start"
    exit 1
fi

# Check if image exists
if ! podman image inspect snapstudio:latest &> /dev/null; then
    print_warning "SnapStudio Podman image not found. Building it first..."
    ./podman_build.sh
fi

# Stop and remove existing container if it exists
if podman ps -a --format 'table {{.Names}}' | grep -q "snapstudio-app"; then
    print_status "Stopping existing container..."
    podman stop snapstudio-app &> /dev/null || true
    podman rm snapstudio-app &> /dev/null || true
fi

# Create volumes if they don't exist
print_status "Creating volumes..."
podman volume create snapstudio_data 2>/dev/null || true
podman volume create snapstudio_logs 2>/dev/null || true
podman volume create snapstudio_backups 2>/dev/null || true
podman volume create snapstudio_exports 2>/dev/null || true
podman volume create snapstudio_uploads 2>/dev/null || true

# Run the container
print_status "Starting SnapStudio container..."
podman run -d \
    --name snapstudio-app \
    -p 5001:5001 \
    -v snapstudio_data:/app/data \
    -v snapstudio_logs:/app/logs \
    -v snapstudio_backups:/app/backups \
    -v snapstudio_exports:/app/exports \
    -v snapstudio_uploads:/app/uploads \
    --restart unless-stopped \
    snapstudio:latest

if [ $? -eq 0 ]; then
    print_success "SnapStudio container started successfully!"
    echo ""
    echo "🎉 SnapStudio is now running!"
    echo "============================="
    echo ""
    echo "Access the application at: http://localhost:5001"
    echo "Default login: admin / admin123"
    echo ""
    echo "Container management:"
    echo "  View logs:    podman logs -f snapstudio-app"
    echo "  Stop:         podman stop snapstudio-app"
    echo "  Start:        podman start snapstudio-app"
    echo "  Remove:       podman rm -f snapstudio-app"
    echo ""
    print_success "Container is running in the background!"
else
    print_error "Failed to start SnapStudio container!"
    exit 1
fi
