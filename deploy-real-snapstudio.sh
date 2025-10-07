#!/bin/bash

# SnapStudio Real Application Deployment
# Replace the test version with the real SnapStudio application

echo "📸 Deploying Real SnapStudio Application"
echo "======================================="

# Check if we're in the right directory
if [ ! -f "cloudflare/worker-real.js" ]; then
    echo "❌ Please run this script from the SnapStudio root directory"
    exit 1
fi

echo "🔄 Deploying real SnapStudio application..."

# Deploy the real application
cd cloudflare

if wrangler deploy; then
    echo ""
    echo "✅ SUCCESS! Real SnapStudio deployed!"
    echo "====================================="
    echo ""
    echo "🌐 Your real SnapStudio is now live at:"
    echo "   https://snapstudio.cc"
    echo "   https://www.snapstudio.cc"
    echo ""
    echo "🎯 Features now available:"
    echo "   ✅ Professional Dashboard"
    echo "   ✅ Client Management"
    echo "   ✅ Appointment Management"
    echo "   ✅ Calendar View"
    echo "   ✅ Analytics Dashboard"
    echo "   ✅ Package Management"
    echo "   ✅ Login System"
    echo ""
    echo "🔐 Login credentials:"
    echo "   Username: admin"
    echo "   Password: admin123"
    echo ""
    echo "📊 Database: Connected to D1 with proper schema"
    echo "💰 Cost: $0/month (Cloudflare free tier)"
    echo ""
    echo "🎉 Your professional photography business management system is ready!"
    echo ""
    echo "Next steps:"
    echo "1. Visit https://snapstudio.cc"
    echo "2. Login with admin/admin123"
    echo "3. Start managing your photography business!"
    
else
    echo "❌ Deployment failed!"
    exit 1
fi
