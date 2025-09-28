#!/usr/bin/env python3
"""Verify SnapStudio setup and dependencies."""

import sys
import subprocess
import importlib
import os

def check_python_version():
    """Check Python version."""
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Need Python 3.8+")
        return False

def check_dependencies():
    """Check required dependencies."""
    required = [
        'flask', 'sqlalchemy', 'yaml', 'google.auth', 
        'google.oauth2', 'googleapiclient', 'werkzeug'
    ]
    
    missing = []
    for dep in required:
        try:
            importlib.import_module(dep)
            print(f"✅ {dep} - OK")
        except ImportError:
            print(f"❌ {dep} - Missing")
            missing.append(dep)
    
    return len(missing) == 0

def check_directories():
    """Check required directories."""
    required_dirs = ['data', 'logs', 'backups', 'exports', 'uploads', 'temp']
    
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✅ {dir_name}/ - OK")
        else:
            print(f"❌ {dir_name}/ - Missing")
            return False
    return True

def check_config_files():
    """Check configuration files."""
    config_files = ['config.yaml', 'requirements.txt']
    
    for file_name in config_files:
        if os.path.exists(file_name):
            print(f"✅ {file_name} - OK")
        else:
            if file_name == 'config.yaml' and os.path.exists('config.example.yaml'):
                print(f"⚠️  {file_name} - Missing (but config.example.yaml exists)")
            else:
                print(f"❌ {file_name} - Missing")
                return False
    return True

def check_database():
    """Check database files."""
    db_files = ['data/web_app.db', 'data/crm.db']
    
    for db_file in db_files:
        if os.path.exists(db_file):
            print(f"✅ {db_file} - OK")
        else:
            print(f"⚠️  {db_file} - Missing (will be created on first run)")
    
    return True

def check_scripts():
    """Check installation scripts."""
    scripts = ['install_macos.sh', 'install_linux.sh', 'install_windows.bat']
    
    for script in scripts:
        if os.path.exists(script):
            print(f"✅ {script} - OK")
        else:
            print(f"❌ {script} - Missing")
            return False
    return True

def main():
    """Run all checks."""
    print("🔍 Verifying SnapStudio Setup")
    print("=" * 40)
    
    checks = [
        check_python_version(),
        check_dependencies(),
        check_directories(),
        check_config_files(),
        check_database(),
        check_scripts()
    ]
    
    print("\n" + "=" * 40)
    
    if all(checks):
        print("🎉 All checks passed! SnapStudio is ready to use.")
        print("\nNext steps:")
        print("1. Run: python web_app.py")
        print("2. Open: http://localhost:5001")
        print("3. Login: admin / admin123")
        return 0
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print("\nTroubleshooting:")
        print("1. Run the appropriate installation script")
        print("2. Check the README.md for detailed instructions")
        print("3. Contact support: snapappdevelopment@gmail.com")
        return 1

if __name__ == "__main__":
    sys.exit(main())
