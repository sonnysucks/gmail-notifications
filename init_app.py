#!/usr/bin/env python3
"""
Gmail Notifications System - Application Initialization Script

This script initializes the application by:
1. Creating necessary directories
2. Setting up configuration files
3. Initializing the database
4. Creating default data
5. Setting up logging

Run this script before starting the application for the first time.
"""

import os
import sys
import sqlite3
import yaml
import logging
from pathlib import Path
from datetime import datetime

def create_directories():
    """Create all necessary directories for the application"""
    print("📁 Creating application directories...")
    
    directories = [
        'data',
        'logs', 
        'backups',
        'templates',
        'uploads',
        'exports',
        'temp'
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"   ✓ Created directory: {directory}/")
    
    # Create instance directory for Flask
    Path('instance').mkdir(exist_ok=True)
    print("   ✓ Created directory: instance/")

def create_config_file():
    """Create the main configuration file"""
    print("⚙️  Creating configuration file...")
    
    config = {
        'app': {
            'name': 'Gmail Notifications System',
            'version': '1.0.0',
            'debug': True,
            'secret_key': 'your-secret-key-change-this-in-production',
            'port': 5001,
            'host': '0.0.0.0'
        },
        'database': {
            'type': 'sqlite',
            'path': 'data/web_app.db',
            'backup_path': 'backups/'
        },
        'logging': {
            'level': 'INFO',
            'file': 'logs/app.log',
            'max_size': '10MB',
            'backup_count': 5
        },
        'gmail': {
            'enabled': False,
            'credentials_file': 'credentials.json',
            'token_file': 'token.json',
            'scopes': ['https://www.googleapis.com/auth/gmail.readonly']
        },
        'google_calendar': {
            'enabled': False,
            'client_id': '',
            'client_secret': '',
            'google_account': '',
            'calendar_id': '',
            'custom_calendar_id': '',
            'sync_appointments': True,
            'sync_reminders': True,
            'event_title_format': '{client_name} - {session_type}',
            'event_description': 'Photography session',
            'reminder_minutes': 60
        },
        'session_types': [
            {
                'name': 'Newborn Session',
                'duration': 120,
                'price': 299.00,
                'description': 'Perfect for babies 0-14 days old',
                'props': ['Blankets', 'Baskets', 'Hats', 'Headbands']
            },
            {
                'name': 'Milestone Session',
                'duration': 90,
                'price': 199.00,
                'description': 'Capture important milestones (3, 6, 9, 12 months)',
                'props': ['Toys', 'Props', 'Themes']
            },
            {
                'name': 'Birthday Session',
                'duration': 60,
                'price': 149.00,
                'description': 'Celebrate your little one\'s special day',
                'props': ['Cake', 'Balloons', 'Decorations']
            },
            {
                'name': 'Family Session',
                'duration': 90,
                'price': 249.00,
                'description': 'Beautiful family portraits',
                'props': ['Outdoor', 'Studio', 'Props']
            }
        ],
        'themes': [
            'Classic', 'Vintage', 'Modern', 'Rustic', 'Elegant', 'Playful', 'Seasonal'
        ],
        'props': [
            'Blankets', 'Baskets', 'Hats', 'Headbands', 'Toys', 'Flowers', 'Balloons'
        ],
        'business': {
            'name': 'Your Photography Business',
            'email': 'info@yourbusiness.com',
            'phone': '(555) 123-4567',
            'address': '123 Photography Lane, City, State 12345',
            'website': 'https://yourbusiness.com',
            'hours': 'Monday-Friday: 9AM-6PM, Saturday: 10AM-4PM'
        }
    }
    
    # Write config to file
    with open('config.yaml', 'w') as f:
        yaml.dump(config, f, default_flow_style=False, indent=2)
    
    print("   ✓ Created config.yaml")

def init_database():
    """Initialize the SQLite database with all necessary tables"""
    print("🗄️  Initializing database...")
    
    db_path = 'data/web_app.db'
    
    # Connect to database (creates it if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(80) UNIQUE NOT NULL,
            email VARCHAR(120) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            role VARCHAR(20) DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create clients table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(120),
            phone VARCHAR(20),
            address TEXT,
            children_count INTEGER DEFAULT 0,
            children_names TEXT,
            children_birth_dates TEXT,
            preferences TEXT,
            family_type VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create appointments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            session_type VARCHAR(100) NOT NULL,
            date DATE NOT NULL,
            time TIME NOT NULL,
            duration INTEGER DEFAULT 60,
            status VARCHAR(20) DEFAULT 'pending',
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES clients (id)
        )
    ''')
    
    # Create baby_milestones table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS baby_milestones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            baby_name VARCHAR(100) NOT NULL,
            milestone_type VARCHAR(100) NOT NULL,
            milestone_date DATE NOT NULL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES clients (id)
        )
    ''')
    
    # Create birthday_sessions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS birthday_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            baby_name VARCHAR(100) NOT NULL,
            birthday_date DATE NOT NULL,
            session_date DATE NOT NULL,
            theme VARCHAR(100),
            props TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES clients (id)
        )
    ''')
    
    # Create client_notes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS client_notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            note_type VARCHAR(50) NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES clients (id)
        )
    ''')
    
    # Create marketing_campaigns table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS marketing_campaigns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            campaign_type VARCHAR(50) NOT NULL,
            target_audience TEXT,
            message TEXT,
            status VARCHAR(20) DEFAULT 'draft',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create system_logs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            level VARCHAR(20) NOT NULL,
            message TEXT NOT NULL,
            source VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create backup_logs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS backup_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            backup_type VARCHAR(50) NOT NULL,
            filename VARCHAR(255),
            file_size INTEGER,
            status VARCHAR(20) NOT NULL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insert default admin user
    cursor.execute('''
        INSERT OR IGNORE INTO users (username, email, password_hash, role)
        VALUES (?, ?, ?, ?)
    ''', ('admin', 'admin@example.com', 'pbkdf2:sha256:600000$default_hash$admin123', 'admin'))
    
    # Insert default session types
    default_session_types = [
        ('Newborn Session', 120, 299.00, 'Perfect for babies 0-14 days old'),
        ('Milestone Session', 90, 199.00, 'Capture important milestones (3, 6, 9, 12 months)'),
        ('Birthday Session', 60, 149.00, 'Celebrate your little one\'s special day'),
        ('Family Session', 90, 249.00, 'Beautiful family portraits')
    ]
    
    for session_type in default_session_types:
        cursor.execute('''
            INSERT OR IGNORE INTO system_logs (level, message, source)
            VALUES (?, ?, ?)
        ''', ('INFO', f'Default session type: {session_type[0]}', 'init_script'))
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print("   ✓ Database initialized successfully")
    print("   ✓ Created all necessary tables")
    print("   ✓ Added default admin user (username: admin, password: admin123)")

def setup_logging():
    """Set up logging configuration"""
    print("📝 Setting up logging...")
    
    # Create logs directory if it doesn't exist
    Path('logs').mkdir(exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/init.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Log initialization
    logger = logging.getLogger('init_script')
    logger.info('Application initialization started')
    
    print("   ✓ Logging configured")
    print("   ✓ Log file: logs/init.log")

def create_sample_data():
    """Create sample data for testing"""
    print("📊 Creating sample data...")
    
    db_path = 'data/web_app.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Sample client
    cursor.execute('''
        INSERT OR IGNORE INTO clients (name, email, phone, children_count, family_type)
        VALUES (?, ?, ?, ?, ?)
    ''', ('Sample Family', 'sample@example.com', '(555) 123-4567', 1, 'New Parents'))
    
    # Sample appointment
    cursor.execute('''
        INSERT OR IGNORE INTO appointments (client_id, session_type, date, time, duration, status)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (1, 'Newborn Session', '2025-09-15', '10:00:00', 120, 'confirmed'))
    
    # Sample milestone
    cursor.execute('''
        INSERT OR IGNORE INTO baby_milestones (client_id, baby_name, milestone_type, milestone_date)
        VALUES (?, ?, ?, ?)
    ''', (1, 'Baby Emma', 'First Smile', '2025-08-20'))
    
    conn.commit()
    conn.close()
    
    print("   ✓ Created sample client, appointment, and milestone")

def create_gitignore():
    """Create or update .gitignore file"""
    print("🚫 Updating .gitignore...")
    
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Database
*.db
*.sqlite
*.sqlite3
data/*.db

# Configuration
config.yaml
credentials.json
token.json
*.key

# Logs
logs/*.log
*.log

# Backups
backups/*.json
backups/*.db

# Instance
instance/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Temporary files
temp/
uploads/
exports/
*.tmp
*.temp
"""
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content)
    
    print("   ✓ Updated .gitignore")

def create_readme():
    """Create a setup README"""
    print("📖 Creating setup documentation...")
    
    readme_content = """# Gmail Notifications System - Setup Complete! 🎉

## 🚀 Quick Start

1. **Activate Virtual Environment:**
   ```bash
   source .venv/bin/activate  # On macOS/Linux
   # or
   .venv\\Scripts\\activate   # On Windows
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the Application:**
   ```bash
   python run_web_app.py
   ```

4. **Access the Application:**
   - URL: http://localhost:5001
   - Username: admin
   - Password: admin123

## 📁 Directory Structure

- `data/` - Database files
- `logs/` - Application logs
- `backups/` - System backups
- `templates/` - HTML templates
- `uploads/` - File uploads
- `exports/` - Data exports
- `temp/` - Temporary files

## ⚙️ Configuration

The application is configured via `config.yaml`. Key settings include:
- Database configuration
- Gmail integration settings
- Google Calendar settings
- Session types and pricing
- Business information

## 🔒 Security Notes

- Change the default admin password after first login
- Update the secret key in production
- Secure your configuration files
- Regularly backup your data

## 📞 Support

If you encounter issues:
1. Check the logs in `logs/` directory
2. Verify database exists in `data/` directory
3. Ensure all dependencies are installed
4. Check configuration in `config.yaml`

Happy shooting! 📸✨
"""
    
    with open('SETUP_COMPLETE.md', 'w') as f:
        f.write(readme_content)
    
    print("   ✓ Created SETUP_COMPLETE.md")

def main():
    """Main initialization function"""
    print("🚀 Gmail Notifications System - Initialization Script")
    print("=" * 60)
    
    try:
        # Run all initialization steps
        create_directories()
        create_config_file()
        setup_logging()
        init_database()
        create_sample_data()
        create_gitignore()
        create_readme()
        
        print("\n" + "=" * 60)
        print("✅ Initialization Complete!")
        print("=" * 60)
        print("\n🎯 Next Steps:")
        print("1. Activate your virtual environment")
        print("2. Install dependencies: pip install -r requirements.txt")
        print("3. Start the application: python run_web_app.py")
        print("4. Access at: http://localhost:5001")
        print("5. Login with: admin / admin123")
        print("\n📁 Created directories: data/, logs/, backups/, uploads/, exports/, temp/")
        print("⚙️  Configuration: config.yaml")
        print("🗄️  Database: data/web_app.db")
        print("📖 Documentation: SETUP_COMPLETE.md")
        
    except Exception as e:
        print(f"\n❌ Initialization failed: {str(e)}")
        print("Please check the error and try again.")
        sys.exit(1)

if __name__ == '__main__':
    main()
