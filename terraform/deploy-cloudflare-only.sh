#!/bin/bash

# SnapStudio Cloudflare-Only Deployment Script
# Deploy SnapStudio using only Cloudflare services

set -e

echo "☁️ SnapStudio Cloudflare-Only Deployment"
echo "========================================"

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
if [ ! -f "terraform-cloudflare-only.tfvars" ]; then
    print_warning "terraform-cloudflare-only.tfvars not found. Creating from template..."
    cp terraform-cloudflare-only.tfvars.example terraform-cloudflare-only.tfvars
    
    print_warning "IMPORTANT: Please edit terraform-cloudflare-only.tfvars and configure:"
    echo "  - Domain name"
    echo "  - Cloudflare API token"
    echo "  - Cloudflare account ID"
    echo ""
    echo "Press Enter to continue after editing terraform-cloudflare-only.tfvars..."
    read -r
fi

print_status "Initializing Terraform..."
terraform init

print_status "Planning Cloudflare-only deployment..."
terraform plan -var-file="terraform-cloudflare-only.tfvars" -out=plan.out

echo ""
print_warning "This will create:"
echo "  - Cloudflare D1 database (free tier)"
echo "  - Cloudflare R2 bucket for storage (free tier)"
echo "  - Cloudflare Worker (free tier)"
echo "  - DNS records"
echo "  - Security rules"
echo "  - Rate limiting"
echo ""
echo "💰 Total cost: FREE (using Cloudflare free tier)"
echo ""
echo "Press Enter to continue with deployment..."
read -r

print_status "Deploying to Cloudflare..."
terraform apply plan.out

if [ $? -eq 0 ]; then
    print_success "Cloudflare deployment completed successfully!"
    
    # Get outputs
    DOMAIN_URL=$(terraform output -raw domain_url)
    WORKER_URL=$(terraform output -raw worker_url)
    DATABASE_ID=$(terraform output -raw database_id)
    
    echo ""
    echo "🎉 SnapStudio is now deployed on Cloudflare!"
    echo "============================================="
    echo ""
    echo "🌐 Application URL: $DOMAIN_URL"
    echo "⚡ Worker URL: $WORKER_URL"
    echo "🗄️  Database ID: $DATABASE_ID"
    echo ""
    echo "⏳ Waiting for DNS propagation..."
    sleep 10
    
    # Test application
    if curl -f "$DOMAIN_URL/api/health" > /dev/null 2>&1; then
        print_success "Application is healthy and responding!"
    else
        print_warning "Application may still be propagating. Try again in a few minutes."
    fi
    
    echo ""
    echo "🔧 Management commands:"
    echo "  View logs:         wrangler tail snapstudio-worker"
    echo "  Update worker:     wrangler deploy"
    echo "  Database console:  wrangler d1 execute snapstudio-db --command 'SELECT * FROM clients'"
    echo "  Destroy infra:     terraform destroy"
    echo ""
    echo "📊 Cloudflare Dashboard:"
    echo "  https://dash.cloudflare.com"
    echo ""
    echo "💰 Cost breakdown:"
    echo "  - Cloudflare Workers: FREE (100k requests/day)"
    echo "  - Cloudflare D1: FREE (5GB storage)"
    echo "  - Cloudflare R2: FREE (10GB storage)"
    echo "  - DNS & SSL: FREE"
    echo "  - Total: $0/month"
    echo ""
    print_success "Deployment completed! Happy shooting! 📸✨"
    
else
    print_error "Deployment failed!"
    echo "Check the error messages above and try again."
    exit 1
fi
