# ⚡ Quick Setup Reference
## Photography Scheduler - Essential Commands

**For the complete setup guide, see `STARTUP_GUIDE.md`**

---

## 🚀 **5-Minute Setup (Essential Commands)**

### **1. Clone & Setup**
```bash
# Clone repository
git clone https://github.com/yourusername/gmail-notifications.git
cd gmail-notifications

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### **2. Google Cloud Setup**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create project → Enable Gmail API + Calendar API
3. Create OAuth 2.0 credentials → Download `credentials.json`
4. Place `credentials.json` in project root

### **3. Configuration**
```bash
# Create config file
cp config.example.yaml config.yaml

# Edit with your business details
nano config.yaml  # or code config.yaml
```

### **4. Initialize System**
```bash
# Setup database and verify
python main.py setup

# Test basic functionality
python test_crm.py
python test_baby_photography.py
```

---

## 🔧 **Essential Configuration Updates**

### **Business Information**
```yaml
business:
  name: "Your Business Name"
  email: "your-email@gmail.com"
  phone: "+1-XXX-XXX-XXXX"
  website: "https://yourwebsite.com"
```

### **Working Hours (9 AM - 8 PM)**
```yaml
calendar:
  business_hours:
    daily:
      start: "09:00"
      end: "20:00"
      timezone: "America/New_York"
```

### **Calendar Settings**
```yaml
calendar:
  target_calendar_id: "primary"  # or specific calendar ID
  timezone: "America/New_York"    # Your timezone
```

---

## 🧪 **Quick Testing Commands**

### **Test Configuration**
```bash
python -c "
from config.config_manager import ConfigManager
cm = ConfigManager()
print('✅ Config loaded:', cm.get('business.name'))
"
```

### **Test CRM**
```bash
python -c "
from scheduler.crm_manager import CRMManager
from config.config_manager import ConfigManager
cm = ConfigManager()
crm = CRMManager(cm)
print('✅ CRM ready!')
"
```

### **Test Authentication**
```bash
# Test Gmail
python -c "from gmail.gmail_manager import GmailManager; GmailManager(ConfigManager()).authenticate()"

# Test Calendar
python -c "from calendar.calendar_manager import CalendarManager; CalendarManager(ConfigManager()).authenticate()"
```

---

## 📱 **First Usage Commands**

### **System Status**
```bash
python main.py --help
python main.py list --days 30
```

### **Create Test Appointment**
```bash
python main.py schedule "Test Client" "2025-01-15 10:00" "Mini Session" \
  --email "test@example.com" --phone "+1-555-0123"
```

### **CRM Operations**
```bash
python main.py crm search "Test"
python main.py crm client 1
python main.py crm analytics
```

### **Baby Photography**
```bash
python main.py baby add-baby 1 "Baby Test" "2024-12-01"
python main.py baby milestones 1
```

---

## 🚨 **Common Issues & Quick Fixes**

### **Python Version Error**
```bash
# Install Python 3.8+
brew install python@3.9  # macOS
sudo apt install python3.9  # Ubuntu
```

### **Missing Dependencies**
```bash
pip install --upgrade -r requirements.txt
```

### **Configuration Error**
```bash
cp config.example.yaml config.yaml
# Edit config.yaml with your details
```

### **Database Error**
```bash
rm -rf data/
python main.py setup
```

### **Authentication Error**
```bash
# Delete old tokens and re-authenticate
rm -f token.json
python main.py setup
```

---

## 📋 **Setup Checklist**

- [ ] Repository cloned
- [ ] Virtual environment created & activated
- [ ] Dependencies installed
- [ ] Google Cloud project created
- [ ] APIs enabled (Gmail + Calendar)
- [ ] OAuth credentials downloaded
- [ ] `credentials.json` in project root
- [ ] `config.yaml` created & customized
- [ ] System initialized (`python main.py setup`)
- [ ] Tests passing
- [ ] Test appointment created
- [ ] CRM commands working

---

## 🎯 **Next Steps After Setup**

1. **Customize Business Details**: Update pricing, session types, working hours
2. **Test All Features**: Verify scheduling, CRM, baby photography features
3. **Set Up Email Templates**: Customize communication templates
4. **Configure Calendar**: Set up target Google Calendar
5. **Import Existing Clients**: Add current clients to CRM
6. **Set Up Automation**: Configure reminder system

---

**⚡ This quick reference covers the essential setup steps. For detailed explanations, troubleshooting, and advanced configuration, refer to `STARTUP_GUIDE.md`.** 🚀
