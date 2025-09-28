#!/bin/bash

# SnapStudio Podman Build Script
# Builds the SnapStudio Podman image

set -e

echo "🐳 Building SnapStudio Podman Image"
echo "===================================="

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
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

# Check if Podman is installed
if ! command -v podman &> /dev/null; then
    echo "❌ Podman is not installed. Please install Podman first."
    echo "macOS: brew install podman"
    echo "Linux: sudo dnf install podman (Fedora) or sudo apt install podman (Ubuntu)"
    exit 1
fi

# Check if Podman is running
if ! podman info &> /dev/null; then
    echo "❌ Podman is not running. Please start Podman machine first."
    echo "Run: podman machine start"
    exit 1
fi

print_status "Podman is available and running"

# Build the image
print_status "Building SnapStudio Podman image..."
podman build -t snapstudio:latest .

if [ $? -eq 0 ]; then
    print_success "Podman image built successfully!"
    echo ""
    echo "🎉 SnapStudio Podman Image Ready!"
    echo "================================="
    echo ""
    echo "To run the container:"
    echo "  podman run -d -p 5001:5001 --name snapstudio snapstudio:latest"
    echo ""
    echo "Or use podman-compose:"
    echo "  podman-compose up -d"
    echo ""
    echo "Access the application at: http://localhost:5001"
    echo "Default login: admin / admin123"
    echo ""
    print_success "Build completed successfully!"
else
    echo "❌ Podman build failed!"
    exit 1
fi
