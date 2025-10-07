#!/bin/bash

# SnapStudio Terraform Deployment Script
# Fully automated deployment with Infrastructure as Code

set -e

echo "🏗️ SnapStudio Terraform Deployment"
echo "=================================="

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

# Check if Terraform is installed
if ! command -v terraform &> /dev/null; then
    print_error "Terraform is not installed. Please install Terraform first."
    echo "Install from: https://developer.hashicorp.com/terraform/downloads"
    exit 1
fi

# Check if terraform.tfvars exists
if [ ! -f "terraform.tfvars" ]; then
    print_warning "terraform.tfvars not found. Creating from template..."
    cp terraform.tfvars.example terraform.tfvars
    
    print_warning "IMPORTANT: Please edit terraform.tfvars and configure:"
    echo "  - Domain name"
    echo "  - Digital Ocean API token"
    echo "  - Cloudflare API token and account ID"
    echo "  - SSH key fingerprint"
    echo ""
    echo "Press Enter to continue after editing terraform.tfvars..."
    read -r
fi

print_status "Initializing Terraform..."
terraform init

print_status "Planning deployment..."
terraform plan

echo ""
print_warning "This will create:"
echo "  - Digital Ocean droplet (\$6/month)"
echo "  - Cloudflare tunnel"
echo "  - DNS records"
echo "  - Security rules"
echo "  - Rate limiting"
echo ""
echo "Press Enter to continue with deployment..."
read -r

print_status "Deploying infrastructure..."
terraform apply -auto-approve

if [ $? -eq 0 ]; then
    print_success "Infrastructure deployed successfully!"
    
    # Get outputs
    DROPLET_IP=$(terraform output -raw droplet_ip)
    DOMAIN_URL=$(terraform output -raw domain_url)
    
    echo ""
    echo "🎉 SnapStudio is now deployed!"
    echo "=============================="
    echo ""
    echo "🌐 Application URL: $DOMAIN_URL"
    echo "🖥️  Server IP: $DROPLET_IP"
    echo ""
    echo "⏳ Waiting for application to be ready..."
    sleep 30
    
    # Test application
    if curl -f "$DOMAIN_URL/health" > /dev/null 2>&1; then
        print_success "Application is healthy and responding!"
    else
        print_warning "Application may still be starting. Check logs:"
        echo "ssh root@$DROPLET_IP 'docker-compose -f /home/snapstudio/gmail-notifications/docker-compose.cloudflare.yml logs -f'"
    fi
    
    echo ""
    echo "🔧 Management commands:"
    echo "  SSH to server:     ssh root@$DROPLET_IP"
    echo "  View logs:         ssh root@$DROPLET_IP 'docker-compose -f /home/snapstudio/gmail-notifications/docker-compose.cloudflare.yml logs -f'"
    echo "  Update app:        ssh root@$DROPLET_IP 'cd /home/snapstudio/gmail-notifications && git pull && docker-compose -f docker-compose.cloudflare.yml up -d'"
    echo "  Destroy infra:     terraform destroy"
    echo ""
    echo "📊 Cloudflare Dashboard:"
    echo "  https://dash.cloudflare.com"
    echo ""
    print_success "Deployment completed! Happy shooting! 📸✨"
    
else
    print_error "Deployment failed!"
    echo "Check the error messages above and try again."
    exit 1
fi

