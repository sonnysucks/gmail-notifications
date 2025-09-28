#!/bin/bash

# SnapStudio Installation Script for Linux
# This script installs Podman and sets up SnapStudio

set -e  # Exit on any error

echo "🎯 SnapStudio Installation Script for Linux"
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

# Detect Linux distribution
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$NAME
    VER=$VERSION_ID
else
    print_error "Cannot detect Linux distribution"
    exit 1
fi

print_status "Detected OS: $OS"

# Install Podman based on distribution
print_status "Installing Podman..."
if [[ "$OS" == *"Ubuntu"* ]] || [[ "$OS" == *"Debian"* ]]; then
    sudo apt update
    sudo apt install -y podman
elif [[ "$OS" == *"Fedora"* ]] || [[ "$OS" == *"Red Hat"* ]] || [[ "$OS" == *"CentOS"* ]]; then
    sudo dnf install -y podman
elif [[ "$OS" == *"Arch"* ]]; then
    sudo pacman -S podman
else
    print_error "Unsupported Linux distribution: $OS"
    print_status "Please install Podman manually for your distribution"
    exit 1
fi

print_success "Podman installed"

# Start Podman service
print_status "Starting Podman service..."
sudo systemctl start podman
sudo systemctl enable podman
print_success "Podman service started"

# Check for Git
print_status "Checking Git installation..."
if ! command -v git &> /dev/null; then
    print_status "Installing Git..."
    if [[ "$OS" == *"Ubuntu"* ]] || [[ "$OS" == *"Debian"* ]]; then
        sudo apt install -y git
    elif [[ "$OS" == *"Fedora"* ]] || [[ "$OS" == *"Red Hat"* ]] || [[ "$OS" == *"CentOS"* ]]; then
        sudo dnf install -y git
    elif [[ "$OS" == *"Arch"* ]]; then
        sudo pacman -S git
    fi
    print_success "Git installed"
else
    print_success "Git found"
fi

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