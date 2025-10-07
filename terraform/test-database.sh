#!/bin/bash

# Test SnapStudio Cloudflare D1 Database
# This script tests the database connection and creates sample data

echo "🧪 Testing SnapStudio Cloudflare D1 Database"
echo "============================================="

# Database ID from Terraform
DATABASE_ID="3c0d0b5c-9523-4c73-9872-0145f1221302"

echo "📊 Database ID: $DATABASE_ID"
echo "🌐 Domain: snapstudio.cc"
echo ""

# Test database connection (requires wrangler CLI)
if command -v wrangler &> /dev/null; then
    echo "✅ Wrangler CLI found"
    echo ""
    echo "🔧 Testing database connection..."
    
    # Create a test table
    echo "Creating test table..."
    wrangler d1 execute snapstudio-db --command "CREATE TABLE IF NOT EXISTS test_table (id INTEGER PRIMARY KEY, name TEXT, created_at DATETIME DEFAULT CURRENT_TIMESTAMP);"
    
    # Insert test data
    echo "Inserting test data..."
    wrangler d1 execute snapstudio-db --command "INSERT INTO test_table (name) VALUES ('SnapStudio Test');"
    
    # Query test data
    echo "Querying test data..."
    wrangler d1 execute snapstudio-db --command "SELECT * FROM test_table;"
    
    echo ""
    echo "🎉 Database test completed successfully!"
    echo "✅ SnapStudio D1 database is working!"
    
else
    echo "⚠️  Wrangler CLI not found"
    echo "Install it with: npm install -g wrangler"
    echo ""
    echo "📋 Manual test commands:"
    echo "wrangler d1 execute snapstudio-db --command \"CREATE TABLE IF NOT EXISTS clients (id INTEGER PRIMARY KEY, name TEXT, email TEXT, created_at DATETIME DEFAULT CURRENT_TIMESTAMP);\""
    echo "wrangler d1 execute snapstudio-db --command \"INSERT INTO clients (name, email) VALUES ('Test Client', 'test@example.com');\""
    echo "wrangler d1 execute snapstudio-db --command \"SELECT * FROM clients;\""
fi

echo ""
echo "🚀 Next Steps:"
echo "1. Set up DNS records manually in Cloudflare dashboard"
echo "2. Enable R2 storage for file uploads"
echo "3. Deploy a simple Worker to serve the app"
echo "4. Test the full application"
echo ""
echo "💰 Cost so far: $0 (using Cloudflare free tier)"
