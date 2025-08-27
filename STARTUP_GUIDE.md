# 🚀 Complete Startup Guide
## Photography Scheduler - From Fresh Clone to Running System

**Project**: Gmail Photography Appointment Scheduler with CRM  
**Specialization**: Baby Photography (Maternity, Newborn, Milestone, Smash Cake, Birthday)  
**Repository**: `gmail-notifications`  
**Last Updated**: August 2025

---

## 📋 **Table of Contents**

1. [Prerequisites & System Requirements](#prerequisites--system-requirements)
2. [Repository Setup](#repository-setup)
3. [Python Environment Setup](#python-environment-setup)
4. [Google Cloud Platform Setup](#google-cloud-platform-setup)
5. [Configuration Setup](#configuration-setup)
6. [Database Initialization](#database-initialization)
7. [Testing & Verification](#testing--verification)
8. [First Run & Usage](#first-run--usage)
9. [Troubleshooting](#troubleshooting)
10. [Next Steps](#next-steps)

---

## 🔧 **Prerequisites & System Requirements**

### **System Requirements**
- **Operating System**: macOS 10.15+, Windows 10+, or Linux (Ubuntu 18.04+)
- **Python**: Python 3.8 or higher
- **Memory**: Minimum 4GB RAM (8GB recommended)
- **Storage**: 2GB free space
- **Internet**: Stable internet connection for API access

### **Required Accounts**
- **Google Account**: For Gmail and Google Calendar access
- **Google Cloud Platform**: Free tier account for API access

### **Required Software**
- **Git**: For repository management
- **Python 3.8+**: Core runtime environment
- **pip**: Python package manager
- **Text Editor**: VS Code, Sublime Text, or similar

---

## 📥 **Repository Setup**

### **Step 1: Clone the Repository**
```bash
# Navigate to your desired development directory
cd ~/projects  # or wherever you keep your projects

# Clone the repository
git clone https://github.com/yourusername/gmail-notifications.git

# Navigate into the project directory
cd gmail-notifications

# Verify the clone was successful
ls -la
```

**Expected Output:**
```
total 40
drwxr-xr-x  15 user  staff   480 Aug 15 10:00 .
drwxr-xr-x   3 user  staff    96 Aug 15 10:00 ..
drwxr-xr-x  15 user  staff   480 Aug 15 10:00 .git
drwxr-xr-x   4 user  staff   128 Aug 15 10:00 calendar
drwxr-xr-x   4 user  staff   128 Aug 15 10:00 config
drwxr-xr-x   4 user  staff   128 Aug 15 10:00 data
drwxr-xr-x   4 user  staff   128 Aug 15 10:00 gmail
drwxr-xr-x   4 user  staff   128 Aug 15 10:00 scheduler
drwxr-xr-x   4 user  staff   128 Aug 15 10:00 templates
drwxr-xr-x   4 user  staff   128 Aug 15 10:00 utils
-rw-r--r--   1 user  staff  1234 Aug 15 10:00 README.md
-rw-r--r--   1 user  staff  5678 Aug 15 10:00 main.py
-rw-r--r--   1 user  staff   890 Aug 15 10:00 requirements.txt
-rw-r--r--   1 user  staff  2345 Aug 15 10:00 config.example.yaml
# ... other files
```

### **Step 2: Verify Project Structure**
```bash
# Check that all key directories exist
ls -la | grep "^d"

# Verify key files are present
ls -la *.py *.yaml *.txt *.md
```

---

## 🐍 **Python Environment Setup**

### **Step 1: Check Python Version**
```bash
# Verify Python 3.8+ is installed
python3 --version

# If you have multiple Python versions, ensure you're using 3.8+
python3.8 --version  # or python3.9, python3.10, etc.
```

**Expected Output:**
```
Python 3.8.10  # or higher version
```

### **Step 2: Create Virtual Environment**
```bash
# Create a virtual environment (recommended)
python3 -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate

# Verify activation (you should see (venv) in your prompt)
which python
```

**Expected Output:**
```
/Users/username/projects/gmail-notifications/venv/bin/python
```

### **Step 3: Install Dependencies**
```bash
# Ensure pip is up to date
pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt

# Verify installation
pip list
```

**Expected Output:**
```
Package                    Version
------------------------- -------
google-auth               2.23.4
google-auth-oauthlib      1.1.0
google-auth-httplib2      0.1.1
google-api-python-client  2.108.0
PyYAML                    6.0.1
python-dateutil           2.8.2
pytz                      2023.3
click                     8.1.7
schedule                  1.2.0
requests                  2.31.0
python-dotenv             1.0.0
jinja2                    3.1.2
# ... other packages
```

---

## ☁️ **Google Cloud Platform Setup**

### **Step 1: Create Google Cloud Project**
1. **Go to**: [Google Cloud Console](https://console.cloud.google.com/)
2. **Sign in** with your Google account
3. **Create a new project** or select existing project
4. **Note your Project ID** (you'll need this later)

### **Step 2: Enable Required APIs**
1. **Navigate to**: APIs & Services > Library
2. **Search and enable** these APIs:
   - **Gmail API**
   - **Google Calendar API**
   - **Google+ API** (for OAuth)

### **Step 3: Create OAuth 2.0 Credentials**
1. **Navigate to**: APIs & Services > Credentials
2. **Click**: "Create Credentials" > "OAuth 2.0 Client IDs"
3. **Application type**: Choose "Desktop application"
4. **Name**: "Photography Scheduler"
5. **Click**: "Create"
6. **Download the JSON file** (rename to `credentials.json`)

### **Step 4: Configure OAuth Consent Screen**
1. **Navigate to**: APIs & Services > OAuth consent screen
2. **User Type**: Choose "External" (unless you have Google Workspace)
3. **App name**: "Photography Scheduler"
4. **User support email**: Your email address
5. **Developer contact information**: Your email address
6. **Scopes**: Add these scopes:
   - `https://www.googleapis.com/auth/gmail.modify`
   - `https://www.googleapis.com/auth/calendar`
   - `https://www.googleapis.com/auth/userinfo.email`

### **Step 5: Place Credentials File**
```bash
# Copy credentials.json to the project root
cp ~/Downloads/credentials.json .

# Verify the file is in place
ls -la credentials.json
```

**Expected Output:**
```
-rw-r--r--  1 user  staff  1234 Aug 15 10:00 credentials.json
```

---

## ⚙️ **Configuration Setup**

### **Step 1: Create Configuration File**
```bash
# Copy the example configuration
cp config.example.yaml config.yaml

# Verify the file was created
ls -la config.yaml
```

### **Step 2: Edit Configuration File**
```bash
# Open the configuration file in your preferred editor
# VS Code:
code config.yaml

# Or use a text editor:
nano config.yaml
# or
vim config.yaml
```

### **Step 3: Update Business Information**
```yaml
# Update these sections in config.yaml:

business:
  name: "Your Photography Business Name"
  email: "your-email@gmail.com"
  phone: "+1-XXX-XXX-XXXX"
  website: "https://yourwebsite.com"
  address: "Your City, State ZIP"
  tax_id: "XX-XXXXXXX"  # Optional
  business_type: "LLC"   # or Sole Proprietorship, Corporation, etc.
```

### **Step 4: Update Calendar Settings**
```yaml
calendar:
  target_calendar_id: "primary"  # or specific calendar ID
  timezone: "America/New_York"    # Your timezone
  
  business_hours:
    daily:
      start: "09:00"
      end: "20:00"
      timezone: "America/New_York"
```

### **Step 5: Update Email Settings**
```yaml
email:
  from_name: "Your Photography Business"
  reply_to: "your-email@gmail.com"
```

### **Step 6: Update Gmail Settings**
```yaml
gmail:
  label_name: "Photography Appointments"  # Customize as needed
  search_query: "subject:(appointment OR session OR photoshoot) OR body:(appointment OR session OR photoshoot)"
```

### **Step 7: Verify Configuration**
```bash
# Test configuration loading
python -c "
from config.config_manager import ConfigManager
try:
    cm = ConfigManager()
    print('✅ Configuration loaded successfully!')
    print(f'Business: {cm.get(\"business.name\")}')
    print(f'Calendar: {cm.get(\"calendar.target_calendar_id\")}')
    print(f'Timezone: {cm.get(\"calendar.timezone\")}')
except Exception as e:
    print(f'❌ Configuration error: {e}')
"
```

**Expected Output:**
```
✅ Configuration loaded successfully!
Business: Your Photography Business Name
Calendar: primary
Timezone: America/New_York
```

---

## 🗄️ **Database Initialization**

### **Step 1: Create Data Directory**
```bash
# Ensure the data directory exists
mkdir -p data

# Verify directory structure
ls -la data/
```

### **Step 2: Initialize CRM Database**
```bash
# Run the setup command to initialize the database
python main.py setup

# Verify database was created
ls -la data/
```

**Expected Output:**
```
✅ CRM database initialized successfully!
✅ Configuration validated successfully!
✅ Gmail labels configured successfully!
✅ Calendar access verified successfully!
✅ System is ready to use!

data/
├── crm.db          # SQLite database
└── reminders.json  # Reminders storage
```

### **Step 3: Verify Database Tables**
```bash
# Test CRM functionality
python -c "
from scheduler.crm_manager import CRMManager
from config.config_manager import ConfigManager

try:
    cm = ConfigManager()
    crm = CRMManager(cm)
    print('✅ CRM database initialized successfully!')
    print('✅ All tables created and ready!')
except Exception as e:
    print(f'❌ CRM error: {e}')
"
```

**Expected Output:**
```
✅ CRM database initialized successfully!
✅ All tables created and ready!
```

---

## 🧪 **Testing & Verification**

### **Step 1: Run Basic Tests**
```bash
# Test the scheduler models
python test_scheduler.py

# Test CRM functionality
python test_crm.py

# Test baby photography features
python test_baby_photography.py
```

**Expected Output:**
```
✅ All tests passed successfully!
```

### **Step 2: Test Configuration Loading**
```bash
# Test configuration manager
python -c "
from config.config_manager import ConfigManager
cm = ConfigManager()
print('✅ Config Manager: OK')
print('✅ Business Info:', cm.get('business.name'))
print('✅ Calendar ID:', cm.get('calendar.target_calendar_id'))
print('✅ Timezone:', cm.get('calendar.timezone'))
print('✅ Working Hours:', cm.get('calendar.business_hours.daily.start'), '-', cm.get('calendar.business_hours.daily.end'))
"
```

### **Step 3: Test Gmail Authentication**
```bash
# Test Gmail connection (this will open browser for OAuth)
python -c "
from gmail.gmail_manager import GmailManager
from config.config_manager import ConfigManager

try:
    cm = ConfigManager()
    gmail = GmailManager(cm)
    gmail.authenticate()
    print('✅ Gmail authentication successful!')
except Exception as e:
    print(f'❌ Gmail error: {e}')
"
```

### **Step 4: Test Calendar Authentication**
```bash
# Test Calendar connection
python -c "
from calendar.calendar_manager import CalendarManager
from config.config_manager import ConfigManager

try:
    cm = ConfigManager()
    cal = CalendarManager(cm)
    cal.authenticate()
    print('✅ Calendar authentication successful!')
except Exception as e:
    print(f'❌ Calendar error: {e}')
"
```

---

## 🚀 **First Run & Usage**

### **Step 1: Verify System Status**
```bash
# Check system status
python main.py --help

# List current appointments (should be empty initially)
python main.py list --days 30
```

### **Step 2: Test Appointment Creation**
```bash
# Create a test appointment
python main.py schedule "Test Client" "2025-01-15 10:00" "Mini Session" \
  --email "test@example.com" \
  --phone "+1-555-0123" \
  --fee 125.00

# Verify the appointment was created
python main.py list --days 30
```

### **Step 3: Test CRM Commands**
```bash
# Search for clients
python main.py crm search "Test"

# Get client details
python main.py crm client 1

# Add a note to the client
python main.py crm add-note 1 "Test client for system verification"
```

### **Step 4: Test Baby Photography Features**
```bash
# Add a baby to a client
python main.py baby add-baby 1 "Baby Test" "2024-12-01"

# Check milestones
python main.py baby milestones 1

# Update family information
python main.py baby update-family 1 --due-date "2025-06-01"
```

---

## 🔧 **Troubleshooting**

### **Common Issues & Solutions**

#### **1. Python Version Issues**
```bash
# Problem: Python version too old
python3 --version  # Shows < 3.8

# Solution: Install Python 3.8+
# On macOS with Homebrew:
brew install python@3.9

# On Ubuntu:
sudo apt update
sudo apt install python3.9 python3.9-venv python3.9-pip
```

#### **2. Missing Dependencies**
```bash
# Problem: Import errors
ModuleNotFoundError: No module named 'google.auth'

# Solution: Reinstall dependencies
pip install --upgrade -r requirements.txt

# Or install specific package
pip install google-auth google-auth-oauthlib google-api-python-client
```

#### **3. Configuration Errors**
```bash
# Problem: Configuration not found
FileNotFoundError: config.yaml

# Solution: Create configuration file
cp config.example.yaml config.yaml
# Then edit config.yaml with your settings
```

#### **4. Authentication Issues**
```bash
# Problem: OAuth authentication fails
# Solution: 
# 1. Verify credentials.json is in project root
# 2. Check OAuth consent screen is configured
# 3. Ensure APIs are enabled in Google Cloud Console
# 4. Delete token.json if it exists and re-authenticate
```

#### **5. Database Issues**
```bash
# Problem: Database errors
# Solution: Reinitialize database
rm -rf data/
python main.py setup
```

#### **6. Permission Issues**
```bash
# Problem: Cannot write to data directory
# Solution: Check directory permissions
ls -la data/
chmod 755 data/
```

### **Debug Mode**
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG

# Run with verbose output
python main.py --verbose setup
```

---

## 📚 **Next Steps**

### **Immediate Actions (First Week)**
1. **Customize Configuration**: Update business details, pricing, and session types
2. **Test All Features**: Verify scheduling, CRM, and baby photography features
3. **Set Up Email Templates**: Customize email templates for your business
4. **Configure Calendar**: Set up your target Google Calendar

### **Short Term (First Month)**
1. **Import Existing Clients**: Add current clients to the CRM system
2. **Set Up Reminders**: Configure automated reminder system
3. **Test Gmail Integration**: Verify email scanning and processing
4. **Customize Session Types**: Adjust pricing and session details

### **Medium Term (2-3 Months)**
1. **Automation Setup**: Configure cron jobs or systemd services
2. **Backup Strategy**: Implement database and configuration backups
3. **Performance Optimization**: Monitor and optimize system performance
4. **User Training**: Train team members on system usage

### **Long Term (3+ Months)**
1. **Web Interface**: Consider developing a web-based interface
2. **Mobile App**: Explore mobile application development
3. **Advanced Analytics**: Implement detailed business intelligence
4. **Integration**: Connect with other business systems

---

## 📞 **Support & Resources**

### **Documentation Files**
- **`README.md`**: Project overview and basic information
- **`PROJECT_SUMMARY.md`**: Current project state and architecture
- **`DEVELOPMENT_LOG.md`**: Development history and decisions
- **`CALENDAR_SETUP.md`**: Detailed calendar configuration guide
- **`SETUP_GUIDE.md`**: This comprehensive setup guide

### **Configuration Files**
- **`config.example.yaml`**: Template configuration file
- **`config.yaml`**: Your actual configuration (create from example)

### **Test Files**
- **`test_scheduler.py`**: Basic functionality tests
- **`test_crm.py`**: CRM system tests
- **`test_baby_photography.py`**: Baby photography feature tests

### **Key Directories**
- **`config/`**: Configuration management
- **`scheduler/`**: CRM and appointment scheduling
- **`gmail/`**: Gmail API integration
- **`calendar/`**: Google Calendar integration
- **`utils/`**: Utility functions and templates
- **`data/`**: Database and data storage

---

## 🎯 **Success Checklist**

### **Setup Complete When:**
- [ ] Repository cloned successfully
- [ ] Python virtual environment created and activated
- [ ] All dependencies installed without errors
- [ ] Google Cloud Platform project created
- [ ] Required APIs enabled
- [ ] OAuth credentials created and downloaded
- [ ] `credentials.json` placed in project root
- [ ] `config.yaml` created and customized
- [ ] Configuration loads without errors
- [ ] CRM database initializes successfully
- [ ] All tests pass
- [ ] Gmail authentication works
- [ ] Calendar authentication works
- [ ] Test appointment can be created
- [ ] CRM commands function properly
- [ ] Baby photography features work

### **System Ready When:**
- [ ] All checklist items above are completed
- [ ] Business information is customized
- [ ] Working hours are configured (9 AM to 8 PM)
- [ ] Session types and pricing are set
- [ ] Email templates are customized
- [ ] Calendar integration is working
- [ ] Gmail scanning is configured
- [ ] Reminder system is set up

---

## 🚀 **Quick Start Commands**

### **After Setup, Use These Commands:**
```bash
# Check system status
python main.py --help

# Initialize system (first time only)
python main.py setup

# Schedule an appointment
python main.py schedule "Client Name" "2025-01-15 10:00" "Session Type"

# List appointments
python main.py list --days 30

# Run reminder service
python main.py reminders

# CRM operations
python main.py crm search "query"
python main.py crm client 1
python main.py crm analytics

# Baby photography features
python main.py baby add-baby 1 "Baby Name" "2024-12-01"
python main.py baby milestones 1
```

---

**🎉 Congratulations! You've successfully set up the Photography Scheduler system!**

**This comprehensive startup guide ensures you have everything needed to get the system running from a fresh repository clone. The system is now ready to manage your baby photography business with CRM capabilities, automated scheduling, and specialized workflows for capturing life's precious moments.** 🎯📸👶✨

**For ongoing support and development, refer to the other documentation files in this project. Happy scheduling!** 🚀
