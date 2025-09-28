#!/bin/bash

# SnapStudio Installation Script for macOS
# This script installs Podman and sets up SnapStudio

set -e  # Exit on any error

echo "🎯 SnapStudio Installation Script for macOS"
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
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

# Check if Homebrew is installed
print_status "Checking Homebrew installation..."
if ! command -v brew &> /dev/null; then
    print_error "Homebrew is not installed. Please install Homebrew first."
    print_status "Install Homebrew from: https://brew.sh/"
    exit 1
fi
print_success "Homebrew found"

# Check for Podman
print_status "Checking Podman installation..."
if ! command -v podman &> /dev/null; then
    print_status "Installing Podman..."
    brew install podman
    print_success "Podman installed"
else
    print_success "Podman is already installed"
fi

# Initialize Podman machine if needed
print_status "Checking Podman machine..."
if ! podman machine list | grep -q "podman-machine-default"; then
    print_status "Initializing Podman machine..."
    podman machine init
    print_success "Podman machine initialized"
fi

# Start Podman machine
print_status "Starting Podman machine..."
podman machine start
print_success "Podman machine started"

# Check for Git
print_status "Checking Git installation..."
if ! command -v git &> /dev/null; then
    print_error "Git is not installed. Please install Git first."
    print_status "You can install Git via Homebrew: brew install git"
    exit 1
fi
print_success "Git found"

# Clone repository if not already present
if [ ! -d ".git" ]; then
    print_status "Cloning SnapStudio repository..."
    git clone https://github.com/sonnysucks/gmail-notifications.git .
    print_success "Repository cloned"
else
    print_success "Repository already present"
fi

# Make scripts executable
print_status "Making scripts executable..."
chmod +x podman_build.sh podman_run.sh
print_success "Scripts made executable"

# Build and run
print_status "Building SnapStudio container..."
./podman_build.sh

print_status "Starting SnapStudio container..."
./podman_run.sh

echo ""
echo "🎉 SnapStudio Installation Complete!"
echo "======================================"
echo ""
echo "Access the web interface at: http://localhost:5001"
echo "Default login: admin / admin123"
echo ""
echo "Container management:"
echo "  View logs:    podman logs -f snapstudio-app"
echo "  Stop:         podman stop snapstudio-app"
echo "  Start:        podman start snapstudio-app"
echo "  Remove:       podman rm -f snapstudio-app"
echo ""
echo "For support, contact: snapappdevelopment@gmail.com"
echo ""
print_success "Installation completed successfully!"