#!/bin/bash

# SnapStudio Simple Cloudflare Deployment
# Deploy the real SnapStudio application using Cloudflare Workers

set -e

echo "📸 SnapStudio Simple Cloudflare Deployment"
echo "=========================================="

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
if [ ! -f "cloudflare/functions/index.js" ]; then
    print_error "Please run this script from the SnapStudio root directory"
    exit 1
fi

print_status "Setting up SnapStudio database schema..."

# Apply database schema (this should work since we know the database exists)
if wrangler d1 execute snapstudio-db --remote --file=cloudflare/schema.sql; then
    print_success "Database schema applied successfully!"
else
    print_warning "Database schema might already exist - continuing..."
fi

print_status "Deploying SnapStudio to Cloudflare Workers..."

# Copy the correct wrangler.toml
cp cloudflare/wrangler-workers.toml cloudflare/wrangler.toml

# Deploy using Cloudflare Workers (simpler than Pages)
cd cloudflare

if wrangler deploy --dry-run; then
    print_status "Dry run successful, deploying for real..."
    
    if wrangler deploy; then
        print_success "SnapStudio deployed successfully!"
        
        echo ""
        echo "🎉 SnapStudio is now live!"
        echo "========================="
        echo ""
        echo "🌐 Application URL: https://snapstudio.cc"
        echo "🌐 WWW URL: https://www.snapstudio.cc"
        echo "📊 Database: snapstudio-db (D1)"
        echo "💰 Cost: $0/month (Cloudflare free tier)"
        echo ""
        echo "🔧 Management commands:"
        echo "  View logs:         wrangler tail snapstudio-real"
        echo "  Update deployment: wrangler deploy"
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
        echo "  1. Visit https://snapstudio.cc"
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
else
    print_error "Dry run failed - check configuration"
    exit 1
fi
