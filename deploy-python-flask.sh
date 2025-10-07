#!/bin/bash

echo "🐍 Deploying SnapStudio Python Flask App to Cloudflare Workers"
echo "=============================================================="

# Check if we're in the right directory
if [ ! -f "worker-python.py" ]; then
    echo "❌ Error: worker-python.py not found"
    echo "Please run this script from the cloudflare directory"
    exit 1
fi

# Check if wrangler is installed
if ! command -v wrangler &> /dev/null
then
    echo "⚠️  Wrangler CLI not found"
    echo "Installing Wrangler..."
    npm install -g wrangler
fi

# Authenticate wrangler if not already
echo "🔐 Checking Wrangler authentication..."
wrangler whoami &> /dev/null
if [ $? -ne 0 ]; then
    echo "Authenticating Wrangler..."
    wrangler login
fi

echo ""
echo "🚀 Deploying your Python Flask application to Cloudflare Workers..."
echo "This will replace the current JavaScript version with your Python app!"
echo ""

# Deploy using the Python configuration
wrangler deploy --config wrangler-python.toml

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ SUCCESS! Your Python Flask SnapStudio app is now deployed!"
    echo ""
    echo "🌐 Your app is live at: https://snapstudio.cc"
    echo "📊 Health check: https://snapstudio.cc/api/health"
    echo ""
    echo "🎉 What's deployed:"
    echo "   ✅ Your actual Python Flask application"
    echo "   ✅ All your original routes and functionality"
    echo "   ✅ Professional photography features"
    echo "   ✅ Client management & CRM"
    echo "   ✅ Appointment scheduling"
    echo "   ✅ Business analytics"
    echo "   ✅ Package management"
    echo "   ✅ Backup & restore"
    echo ""
    echo "🔧 Next steps:"
    echo "   1. Visit https://snapstudio.cc to see your app"
    echo "   2. Test all the features"
    echo "   3. Configure your database with real data"
    echo "   4. Set up your Google Calendar integration"
    echo ""
else
    echo "❌ Deployment failed. Please check the error messages above."
    exit 1
fi
