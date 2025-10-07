#!/bin/bash

# Quick SnapStudio Real App Deployment
# Replace the test version with real SnapStudio

echo "📸 Deploying Real SnapStudio (Quick Fix)"
echo "========================================"

# Go to cloudflare directory
cd cloudflare

# Deploy the real worker
echo "🔄 Deploying real SnapStudio worker..."
wrangler deploy

echo ""
echo "✅ Done! Your real SnapStudio should now be live at:"
echo "   https://snapstudio.cc"
echo ""
echo "🔐 Login: admin / admin123"
echo "📊 Features: Dashboard, Clients, Appointments, Calendar, Analytics"
