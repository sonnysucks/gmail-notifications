#!/bin/bash

# SnapStudio Cloudflare Deployment Script
# Deploy the real SnapStudio application to Cloudflare

set -e

echo "📸 SnapStudio Cloudflare Deployment"
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

# Check if we're in the right directory
if [ ! -f "cloudflare/wrangler.toml" ]; then
    print_error "Please run this script from the SnapStudio root directory"
    exit 1
fi

# Check if wrangler is installed
if ! command -v wrangler &> /dev/null; then
    print_error "Wrangler CLI is not installed. Please install it first:"
    echo "npm install -g wrangler"
    exit 1
fi

# Check if logged in to Cloudflare
if ! wrangler whoami &> /dev/null; then
    print_error "Not logged in to Cloudflare. Please run:"
    echo "wrangler login"
    exit 1
fi

print_status "Setting up SnapStudio database schema..."

# Apply database schema
wrangler d1 execute snapstudio-db --remote --file=cloudflare/schema.sql

if [ $? -eq 0 ]; then
    print_success "Database schema applied successfully!"
else
    print_error "Failed to apply database schema"
    exit 1
fi

print_status "Deploying SnapStudio to Cloudflare Pages..."

# Deploy to Cloudflare Pages
cd cloudflare
wrangler pages deploy functions --project-name snapstudio

if [ $? -eq 0 ]; then
    print_success "SnapStudio deployed successfully!"
    
    # Get deployment URL
    DEPLOYMENT_URL=$(wrangler pages deployment list --project-name snapstudio --format json | jq -r '.[0].url')
    
    echo ""
    echo "🎉 SnapStudio is now live!"
    echo "========================="
    echo ""
    echo "🌐 Application URL: $DEPLOYMENT_URL"
    echo "📊 Database: snapstudio-db (D1)"
    echo "💰 Cost: $0/month (Cloudflare free tier)"
    echo ""
    echo "🔧 Management commands:"
    echo "  View logs:         wrangler pages deployment tail --project-name snapstudio"
    echo "  Update deployment: wrangler pages deploy functions --project-name snapstudio"
    echo "  Database console:  wrangler d1 execute snapstudio-db --command 'SELECT * FROM clients'"
    echo ""
    echo "📋 Features deployed:"
    echo "  ✅ Dashboard with business metrics"
    echo "  ✅ Client management (CRUD)"
    echo "  ✅ Appointment management (CRUD)"
    echo "  ✅ Calendar view"
    echo "  ✅ Analytics dashboard"
    echo "  ✅ Package management"
    echo "  ✅ Authentication system"
    echo "  ✅ Responsive Bootstrap UI"
    echo ""
    echo "🎯 Next steps:"
    echo "  1. Visit $DEPLOYMENT_URL"
    echo "  2. Login with admin/admin123"
    echo "  3. Add your first client"
    echo "  4. Create an appointment"
    echo "  5. Customize the system for your business"
    echo ""
    print_success "Deployment completed! Happy shooting! 📸✨"
    
else
    print_error "Deployment failed!"
    exit 1
fi
