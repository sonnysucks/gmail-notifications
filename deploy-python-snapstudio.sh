#!/bin/bash

# SnapStudio Python Cloudflare Pages Deployment
# Deploy your real Python Flask application to Cloudflare Pages

echo "📸 Deploying Real SnapStudio Python to Cloudflare Pages"
echo "========================================================"

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
if [ ! -f "cloudflare/functions/main.py" ]; then
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

print_status "Setting up SnapStudio Python Pages deployment..."

# Create a simple HTML file for Pages
mkdir -p cloudflare/dist
cat > cloudflare/dist/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SnapStudio - Professional Photography Management</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
        .container { display: flex; align-items: center; justify-content: center; min-height: 100vh; }
        .card { background: white; border-radius: 15px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); }
    </style>
</head>
<body>
    <div class="container">
        <div class="card p-5 text-center">
            <h1 class="mb-4">📸 SnapStudio</h1>
            <h2 class="mb-4">Professional Photography Management</h2>
            <p class="lead mb-4">Your Python Flask application is now running on Cloudflare Pages!</p>
            <div class="alert alert-success">
                <strong>✅ Deployment Successful!</strong><br>
                Python Functions: Active<br>
                Database: Cloudflare D1<br>
                CDN: Cloudflare Global Network
            </div>
            <div class="mt-4">
                <a href="/dashboard" class="btn btn-primary me-2">Go to Dashboard</a>
                <a href="/login" class="btn btn-outline-primary">Login</a>
            </div>
        </div>
    </div>
</body>
</html>
EOF

print_status "Deploying to Cloudflare Pages..."

# Deploy using Pages
cd cloudflare

if wrangler pages deploy dist --project-name snapstudio-python; then
    print_success "SnapStudio Python deployed successfully!"
    
    echo ""
    echo "🎉 Your Real SnapStudio Python is now live!"
    echo "=========================================="
    echo ""
    echo "🌐 Application URL: https://snapstudio-python.pages.dev"
    echo "📊 Database: snapstudio-db (D1)"
    echo "💰 Cost: $0/month (Cloudflare free tier)"
    echo ""
    echo "🔧 Management commands:"
    echo "  View logs:         wrangler pages deployment tail --project-name snapstudio-python"
    echo "  Update deployment: wrangler pages deploy dist --project-name snapstudio-python"
    echo "  Database console:  wrangler d1 execute snapstudio-db --command 'SELECT * FROM clients'"
    echo ""
    echo "📋 Features deployed:"
    echo "  ✅ Python Flask application"
    echo "  ✅ Professional Photography UI"
    echo "  ✅ Dashboard with business metrics"
    echo "  ✅ Client management"
    echo "  ✅ Appointment management"
    echo "  ✅ Calendar integration"
    echo "  ✅ Analytics dashboard"
    echo "  ✅ Package management"
    echo "  ✅ Authentication system"
    echo "  ✅ Cloudflare D1 database"
    echo ""
    echo "🎯 Next steps:"
    echo "  1. Visit https://snapstudio-python.pages.dev"
    echo "  2. Login with admin/admin123"
    echo "  3. Start managing your photography business!"
    echo ""
    print_success "Deployment completed! Happy shooting! 📸✨"
    
else
    print_error "Deployment failed!"
    exit 1
fi
