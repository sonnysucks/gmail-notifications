# 📚 Documentation Index
## Gmail Photography Appointment Scheduler - Complete Documentation Guide

**Project**: Baby Photography CRM & Scheduling System  
**Version**: 2.0 (Web Application)  
**Last Updated**: September 2024  

---

## 🎯 **Quick Navigation**

### **For Users**
- [🚀 Quick Start Guide](#quick-start-guide) - Get running in 5 minutes
- [🌐 Web Application Guide](#web-application-guide) - Complete web interface documentation
- [⚙️ Configuration Guide](#configuration-guide) - System setup and customization
- [🔧 Troubleshooting](#troubleshooting) - Common issues and solutions

### **For Developers**
- [🏗️ Architecture Overview](#architecture-overview) - System design and components
- [📡 API Documentation](#api-documentation) - REST API endpoints and usage
- [💾 Database Schema](#database-schema) - Data models and relationships
- [🧪 Testing Guide](#testing-guide) - Test suites and development workflow

### **For LLM/AI Assistants**
- [🤖 LLM Context Guide](#llm-context-guide) - Optimized information for AI understanding
- [📋 System State Summary](#system-state-summary) - Current implementation status
- [🔍 Code Structure Map](#code-structure-map) - File organization and responsibilities

---

## 🚀 **Quick Start Guide**

### **Web Application (Recommended)**
```bash
# 1. Clone and setup
git clone <repository-url>
cd gmail-notifications
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Run web application
python run_web_app.py

# 3. Access application
# Open browser to: http://localhost:5001
# Login: admin / admin123
```

### **CLI Application (Legacy)**
```bash
# Setup configuration
cp config.example.yaml config.yaml
# Edit config.yaml with your details

# Initialize system
python main.py --setup

# Test functionality
python test_crm.py
```

---

## 🌐 **Web Application Guide**

### **Core Features**
- **Dashboard**: Business overview with metrics and quick actions
- **Appointment Management**: Create, edit, view appointments with baby photography focus
- **Client Management**: Complete CRM with family and baby tracking
- **Calendar View**: Interactive calendar with appointment visualization
- **Analytics**: Revenue tracking, session statistics, client metrics
- **Backup & Restore**: Complete system backup and data management
- **Configuration**: Comprehensive business setup and customization

### **Key Pages**
- `/` - Dashboard with business overview
- `/appointments` - Appointment list and management
- `/calendar` - Interactive calendar view
- `/clients` - Client management and CRM
- `/analytics` - Business analytics and reporting
- `/setup` - System configuration
- `/backup-restore` - Data backup and restore

### **Authentication**
- Default credentials: `admin` / `admin123`
- Session-based authentication
- Secure cookie handling

---

## ⚙️ **Configuration Guide**

### **Web Application Configuration**
The web application uses the same configuration system as the CLI version:

```yaml
# config.yaml
business:
  name: "Your Photography Business"
  email: "your@email.com"
  phone: "+1-XXX-XXX-XXXX"

calendar:
  target_calendar_id: "primary"
  timezone: "America/New_York"
  business_hours:
    daily:
      start: "09:00"
      end: "20:00"

appointments:
  session_types:
    - name: "Newborn Session"
      duration: 180
      base_price: 350
    - name: "Milestone Session"
      duration: 60
      base_price: 225
```

---

## 🏗️ **Architecture Overview**

### **Current Architecture (Web Application)**

```
gmail-notifications/
├── web_app.py                 # Flask web application (main entry point)
├── run_web_app.py            # Web app launcher
├── main.py                   # CLI application (legacy)
├── scheduler/                # Core business logic
│   ├── models.py            # Data models (Client, Appointment, etc.)
│   ├── crm_manager.py       # CRM operations
│   └── appointment_scheduler.py  # Scheduling logic
├── templates/                # Jinja2 HTML templates
│   ├── dashboard.html       # Main dashboard
│   ├── appointments.html    # Appointment management
│   ├── calendar.html        # Calendar view
│   ├── clients.html         # Client management
│   ├── analytics.html       # Business analytics
│   └── backup_restore.html  # Backup management
├── static/                   # CSS, JS, images
├── config/                   # Configuration management
├── data/                     # SQLite database
└── backups/                  # System backups
```

### **Technology Stack**
- **Backend**: Flask (Python web framework)
- **Database**: SQLite with custom ORM
- **Frontend**: Bootstrap 5 + Custom CSS/JavaScript
- **Authentication**: Flask-Login
- **Templates**: Jinja2
- **Configuration**: YAML-based

---

## 📡 **API Documentation**

### **Authentication Required Endpoints**

#### **Appointments**
- `GET /appointments` - List all appointments
- `POST /appointments` - Create new appointment
- `GET /appointments/<id>` - Get appointment details
- `PUT /appointments/<id>` - Update appointment
- `DELETE /appointments/<id>` - Delete appointment

#### **Clients**
- `GET /clients` - List all clients
- `POST /clients` - Create new client
- `GET /clients/<id>` - Get client details
- `PUT /clients/<id>` - Update client
- `DELETE /clients/<id>` - Delete client

#### **Analytics**
- `GET /api/analytics/revenue` - Revenue data
- `GET /api/analytics/sessions` - Session statistics
- `GET /api/analytics/clients` - Client metrics

#### **Backup & Restore**
- `POST /api/backup` - Create system backup
- `GET /api/backup/list` - List available backups
- `DELETE /api/backup/delete/<filename>` - Delete backup
- `POST /api/backup/restore` - Restore from backup

### **Authentication**
All API endpoints require authentication via session cookies.

---

## 💾 **Database Schema**

### **Core Tables**
```sql
-- Clients table
CREATE TABLE clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    phone TEXT,
    address TEXT,
    children_count INTEGER DEFAULT 0,
    children_names TEXT,  -- JSON array
    children_birth_dates TEXT,  -- JSON array
    preferences TEXT,  -- JSON object
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Appointments table
CREATE TABLE appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER,
    client_name TEXT,
    client_email TEXT,
    session_type TEXT,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    duration INTEGER,
    status TEXT DEFAULT 'scheduled',
    notes TEXT,
    baby_name TEXT,
    baby_age_days INTEGER,
    session_fee REAL DEFAULT 0,
    total_amount REAL DEFAULT 0,
    payment_status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients (id)
);
```

---

## 🧪 **Testing Guide**

### **Test Scripts**
```bash
# Test core functionality
python test_scheduler.py

# Test CRM system
python test_crm.py

# Test baby photography features
python test_baby_photography.py

# Test client creation
python test_client_creation.py
```

### **Web Application Testing**
```bash
# Start web application
python run_web_app.py

# Test endpoints with curl
curl -X GET http://localhost:5001/appointments
curl -X POST http://localhost:5001/api/backup
```

---

## 🔧 **Troubleshooting**

### **Common Issues**

#### **Web Application Won't Start**
```bash
# Check port availability
lsof -i :5001

# Check Python version
python --version  # Should be 3.8+

# Check dependencies
pip install -r requirements.txt
```

#### **Database Errors**
```bash
# Reset database
rm -rf data/
python run_web_app.py  # Will recreate database
```

#### **Authentication Issues**
```bash
# Clear session data
rm -rf instance/
python run_web_app.py
```

#### **Backup/Restore Issues**
- Check file permissions in `backups/` directory
- Ensure sufficient disk space
- Verify JSON file integrity

---

## 🤖 **LLM Context Guide**

### **For AI Assistants - Key Information**

#### **Project Purpose**
Baby photography business management system with CRM, appointment scheduling, and web interface.

#### **Current State (September 2024)**
- **Primary Interface**: Flask web application (`web_app.py`)
- **Legacy Interface**: CLI application (`main.py`) - still functional
- **Database**: SQLite (`data/crm.db`)
- **Authentication**: Session-based (admin/admin123)

#### **Key Components**
1. **Web Application** (`web_app.py`) - Main Flask app with routes
2. **Scheduler Module** (`scheduler/`) - Business logic and data models
3. **Templates** (`templates/`) - Jinja2 HTML templates
4. **Configuration** (`config.yaml`) - YAML-based settings

#### **Recent Features (September 2024)**
- ✅ Interactive calendar view with appointment visualization
- ✅ Complete backup/restore system
- ✅ Business analytics dashboard
- ✅ Clickable appointment management
- ✅ Responsive web design

#### **File Responsibilities**
- `web_app.py` - Flask routes and web logic
- `scheduler/models.py` - Data models (Client, Appointment)
- `scheduler/crm_manager.py` - CRM operations
- `scheduler/appointment_scheduler.py` - Scheduling logic
- `templates/*.html` - Web interface templates
- `config/config_manager.py` - Configuration handling

#### **Common Development Patterns**
- Database operations go through `crm_manager.py` or `appointment_scheduler.py`
- Web routes in `web_app.py` follow RESTful patterns
- Templates use Jinja2 with Bootstrap 5
- Configuration accessed via `config_manager.py`

---

## 📋 **System State Summary**

### **Implementation Status**
- ✅ **Web Application**: Complete and functional
- ✅ **CRM System**: Full client and appointment management
- ✅ **Calendar Integration**: Interactive calendar view
- ✅ **Analytics**: Revenue and session tracking
- ✅ **Backup System**: Complete backup/restore functionality
- ✅ **Authentication**: Session-based security
- 🔄 **Email Integration**: Basic implementation (needs enhancement)
- 🔄 **Gmail Integration**: Basic implementation (needs enhancement)

### **Current Capabilities**
- Create, edit, delete appointments and clients
- Interactive calendar with appointment visualization
- Business analytics and reporting
- Complete system backup and restore
- Responsive web interface
- Session-based authentication

### **Known Limitations**
- Email templates need customization
- Gmail integration needs enhancement
- No payment processing integration
- Single-user system (no multi-user support)

---

## 🔍 **Code Structure Map**

### **Entry Points**
- `run_web_app.py` - Web application launcher
- `main.py` - CLI application (legacy)

### **Core Modules**
- `scheduler/models.py` - Data models
- `scheduler/crm_manager.py` - CRM operations
- `scheduler/appointment_scheduler.py` - Scheduling logic
- `config/config_manager.py` - Configuration management

### **Web Components**
- `web_app.py` - Flask application and routes
- `templates/` - HTML templates
- `static/` - CSS, JavaScript, assets

### **Data Storage**
- `data/crm.db` - SQLite database
- `backups/` - System backup files
- `config.yaml` - Configuration file

---

**This documentation index provides comprehensive guidance for users, developers, and AI assistants working with the Gmail Photography Appointment Scheduler system.** 🎯📸👶
