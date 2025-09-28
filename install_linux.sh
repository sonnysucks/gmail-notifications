#!/bin/bash

# SnapStudio Installation Script for Linux
# This script installs SnapStudio and all dependencies on Linux

set -e  # Exit on any error

echo "🎯 SnapStudio Installation Script for Linux"
echo "============================================="

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
    OS=$(uname -s)
    VER=$(uname -r)
fi

print_status "Detected OS: $OS $VER"

# Check if Python 3 is installed
print_status "Checking Python 3 installation..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.8+ first."
    print_status "Install Python 3 using your package manager:"
    print_status "Ubuntu/Debian: sudo apt update && sudo apt install python3 python3-pip python3-venv"
    print_status "CentOS/RHEL: sudo yum install python3 python3-pip"
    print_status "Fedora: sudo dnf install python3 python3-pip"
    print_status "Arch: sudo pacman -S python python-pip"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
print_success "Python $PYTHON_VERSION found"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 is not installed. Please install pip3 first."
    print_status "Install pip3 using your package manager:"
    print_status "Ubuntu/Debian: sudo apt install python3-pip"
    print_status "CentOS/RHEL: sudo yum install python3-pip"
    print_status "Fedora: sudo dnf install python3-pip"
    print_status "Arch: sudo pacman -S python-pip"
    exit 1
fi

# Create virtual environment
print_status "Creating virtual environment..."
if [ -d "venv" ]; then
    print_warning "Virtual environment already exists. Removing old one..."
    rm -rf venv
fi

python3 -m venv venv
print_success "Virtual environment created"

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate
print_success "Virtual environment activated"

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip
print_success "pip upgraded"

# Install dependencies
print_status "Installing Python dependencies..."
pip install -r requirements.txt
print_success "Dependencies installed"

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p data
mkdir -p logs
mkdir -p backups
mkdir -p exports
mkdir -p uploads
mkdir -p temp
print_success "Directories created"

# Set up configuration file
print_status "Setting up configuration..."
if [ ! -f "config.yaml" ]; then
    if [ -f "config.example.yaml" ]; then
        cp config.example.yaml config.yaml
        print_success "Configuration file created from example"
    else
        print_warning "No config.example.yaml found. You'll need to create config.yaml manually."
    fi
else
    print_success "Configuration file already exists"
fi

# Set permissions
print_status "Setting file permissions..."
chmod +x run_web_app.py
chmod +x main.py
chmod +x install_linux.sh
print_success "Permissions set"

# Test installation
print_status "Testing installation..."
python3 -c "import flask, sqlalchemy, yaml; print('All imports successful')"
print_success "Installation test passed"

echo ""
echo "🎉 SnapStudio Installation Complete!"
echo "======================================"
echo ""
echo "To start the web application:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the web app: python3 web_app.py"
echo "3. Open your browser to: http://localhost:5001"
echo "4. Login with: admin / admin123"
echo ""
echo "To start the CLI application:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run: python3 main.py --help"
echo ""
echo "For support, contact: snapappdevelopment@gmail.com"
echo ""
print_success "Installation completed successfully!"
