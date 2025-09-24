#!/usr/bin/env python3
"""
Simple script to run the Photography Scheduler Web Application
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'flask',
        'flask_sqlalchemy', 
        'flask_login',
        'werkzeug'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Install them with:")
        print("   pip install -r requirements.txt")
        return False
    
    print("✅ All required packages are installed")
    return True

def create_directories():
    """Create necessary directories if they don't exist"""
    directories = ['data', 'logs', 'templates']
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    
    print("✅ Directories created/verified")

def main():
    """Main function to run the web application"""
    print("🎯 Photography Scheduler Web Application")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Check if web_app.py exists
    if not Path('web_app.py').exists():
        print("❌ web_app.py not found!")
        print("   Make sure you're in the correct directory")
        sys.exit(1)
    
    print("\n🚀 Starting web application...")
    print("   The application will be available at: http://localhost:5001")
    print("   Default login: admin / admin123")
    print("\n   Press Ctrl+C to stop the application")
    print("-" * 50)
    
    try:
        # Run the web application
        subprocess.run([sys.executable, 'web_app.py'])
    except KeyboardInterrupt:
        print("\n\n👋 Application stopped by user")
    except Exception as e:
        print(f"\n❌ Error running application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
