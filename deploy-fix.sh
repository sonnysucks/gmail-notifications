#!/bin/bash

# Quick Fix Deployment - No Terminal Hanging
echo "📸 Deploying Fixed SnapStudio Worker"
echo "==================================="

cd cloudflare
wrangler deploy

echo ""
echo "✅ Fixed! Your SnapStudio should now work without database errors."
echo "🌐 Visit: https://snapstudio.cc"
echo "🔐 Login: admin / admin123"
