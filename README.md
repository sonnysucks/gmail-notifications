# SnapStudio
## Professional Photography Business Management System
### Complete CRM & Appointment Scheduler for Professional Photographers & Retouchers

A comprehensive **web-based** appointment scheduling and Customer Relationship Management (CRM) system **designed for professional photography businesses**. Features a modern Flask web application with interactive calendar, business analytics, and complete backup/restore functionality.

## 🌐 **Web Application (Primary Interface)**

**Quick Start**: `python run_web_app.py` → Open `http://localhost:5001` → Login: `admin` / `admin123`

### **Key Web Features**
- **📊 Dashboard**: Business overview with metrics and quick actions
- **📅 Interactive Calendar**: Visual appointment management with clickable days
- **👥 Client Management**: Complete CRM with client and project tracking
- **📈 Analytics**: Revenue tracking, session statistics, client metrics
- **💾 Backup & Restore**: Complete system backup and data management
- **⚙️ Configuration**: Comprehensive business setup and customization

## 📸 **Professional Photography Services**

This system is **designed for professional photographers** specializing in:
- **Portrait Photography** - Professional headshots and personal branding
- **Family Photography** - Milestone sessions and family portraits
- **Event Photography** - Weddings, corporate events, and celebrations
- **Commercial Photography** - Product shots and business photography
- **Retouching Services** - Professional photo editing and enhancement
- **Session Packages** - Customized photography packages for all occasions

## 🚀 **Professional Photography Business Features**

### **Client & Project Management**
- **Client Tracking**: Comprehensive client database with project history
- **Milestone Sessions**: Automated tracking for family milestones and events
- **Session Planning**: Professional session recommendations and scheduling
- **Package Management**: Customizable photography packages and pricing

### **Professional Client Management**
- **Client Type Tracking**: Individual, family, corporate, event clients
- **Project Management**: Track multiple projects and sessions per client
- **Client Database**: Comprehensive client information and preferences
- **Photography Experience**: Client experience level and preferences
- **Referral Sources**: Social media, word of mouth, business partnerships

### **Professional Session Types**
- **Portrait Sessions**: Professional headshots and personal branding
- **Family Sessions**: Milestone and family portrait sessions
- **Event Sessions**: Wedding, corporate, and celebration photography
- **Commercial Sessions**: Product photography and business branding
- **Retouching Services**: Professional photo editing and enhancement
- **Package Deals**: Customized photography packages with professional pricing

### **Advanced Photography Business Tools**
- **Style Management**: Professional photography styles and themes
- **Color Coordination**: Brand color palettes and session themes
- **Equipment Tracking**: Camera gear, lighting, and studio equipment
- **Retouching Workflow**: Professional editing and enhancement services
- **Client Collaboration**: Include family members and stakeholders in sessions

## ✨ **Core Features**

- **Automatic Appointment Scheduling**: Create appointments directly from Gmail
- **Smart Reminder System**: Automated notifications at 2 weeks, 1 week, 3 days, 2 days, and 1 day before appointments
- **Google Calendar Integration**: Works with any Google Calendar as the target
- **Professional Email Templates**: Photography business-specific email templates for all communications
- **Time Zone Handling**: Automatic time zone detection and conversion
- **Gmail Integration**: Scan emails for appointment requests and manage communication

## 🏗️ **Architecture**

### **Web Application Stack**
- **Backend**: Flask (Python web framework) with RESTful API
- **Database**: SQLite with custom ORM and proper indexing
- **Frontend**: Bootstrap 5 + Custom CSS/JavaScript
- **Authentication**: Session-based security
- **Templates**: Jinja2 templating engine

### **Core Components**
- **Web Application** (`web_app.py`): Flask routes and web logic
- **Scheduler Module** (`scheduler/`): Business logic and data models
- **Configuration** (`config/`): YAML-based configuration management
- **Templates** (`templates/`): HTML templates for web interface
- **Static Assets** (`static/`): CSS, JavaScript, and images

### **Legacy CLI Support**
- **CLI Application** (`main.py`): Command-line interface (still functional)
- **Modular Design**: Clean separation of concerns (Gmail, Calendar, Scheduler, CRM, Templates)
- **Scalable**: Can be upgraded to PostgreSQL or MySQL for production use
- **Professional Photography Focused**: Built specifically for professional photography business workflows

## 📊 **CRM Capabilities for Professional Photography**

### **Client Management**
- Comprehensive client profiles with project information
- Client tracking with preferences and milestone planning
- Project size and scope management
- Previous photographer and experience level tracking
- Referral source analysis for marketing optimization

### **Appointment Tracking**
- Full appointment lifecycle management
- Financial tracking with session-specific pricing
- Payment status monitoring
- Equipment and prop requirements
- Priority levels and special instructions
- Follow-up task automation

### **Business Intelligence**
- Revenue analytics by session type and client
- Client acquisition and retention metrics
- Package performance analysis
- Referral source effectiveness
- Customer lifetime value calculations
- Monthly and quarterly reporting

### **Communication Management**
- Organized note system with timestamps
- Internal vs. external note visibility
- Follow-up task automation
- Email template management
- Marketing campaign tracking

## 🛠️ **Prerequisites**

- Python 3.8+
- Google Cloud Platform account
- Gmail API enabled
- Google Calendar API enabled
- OAuth 2.0 credentials

## 📦 **Installation**

### **Web Application (Recommended)**

1. **Clone and setup**:
```bash
git clone <your-repo-url>
cd SnapStudio
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Run the web application**:
```bash
python run_web_app.py
```

3. **Access the application**:
   - Open browser to: `http://localhost:5001`
   - Login: `admin` / `admin123`

### **CLI Application (Legacy)**

1. **Configure the application**:
```bash
cp config.example.yaml config.yaml
# Edit config.yaml with your baby photography business settings
```

2. **Set up Google Cloud credentials** (optional):
   - Create a project in Google Cloud Console
   - Enable Gmail API and Google Calendar API
   - Create OAuth 2.0 credentials
   - Download the credentials JSON file and save as `credentials.json`

## ⚙️ **Configuration for Professional Photography**

Edit `config.yaml` to configure:
- **Business Information**: Studio details, contact info, tax information
- **Session Types & Pricing**: Predefined photography services with professional pricing
- **Photography Settings**: Milestone tracking, client preferences, retouching options
- **CRM Settings**: Client tags, referral sources, client types, experience levels
- **Calendar Settings**: Target calendar, business hours, timezone
- **Email Templates**: Customizable templates for all photography business communications
- **Analytics**: KPI tracking and reporting preferences

## 🎯 **Usage for Professional Photography**

### **Web Application Usage (Recommended)**

1. **Access the web interface**: `http://localhost:5001`
2. **Login**: `admin` / `admin123`
3. **Navigate through the interface**:
   - **Dashboard**: Overview of business metrics
   - **Appointments**: Create, edit, view appointments
   - **Calendar**: Interactive calendar with appointment visualization
   - **Clients**: Manage client information and project details
   - **Analytics**: View business performance and revenue
   - **Setup**: Configure business settings and preferences
   - **Backup & Restore**: Manage system backups

### **CLI Application Usage (Legacy)**

#### **Basic Setup**
```bash
python main.py --setup
```

#### **Professional Photography Appointment Management**
```bash
# Schedule portrait session
python main.py --schedule "Sarah Johnson" "2024-01-15 10:00" "Portrait Session" \
  --client-name "Sarah Johnson" --session-type "portrait" \
  --email "sarah@email.com" --fee 350.00

# Schedule family milestone session
python main.py --schedule "Lisa Smith" "2024-02-01 14:00" "Family Milestone" \
  --client-name "Lisa Smith" --session-type "family" \
  --email "lisa@email.com" --fee 225.00

# Schedule commercial session
python main.py --schedule "Jennifer Davis" "2024-03-15 11:00" "Commercial Session" \
  --client-name "Jennifer Davis" --session-type "commercial" \
  --email "jennifer@email.com" --fee 275.00
```

### **Professional Photography CRM Operations**
```bash
# Add client information
python main.py crm add-client "client_id" "Sarah Johnson" "2024-01-08" \
  --notes "Professional headshot client, prefers natural lighting"

# Check upcoming sessions
python main.py crm upcoming-sessions "client_id"

# Update client information
python main.py crm update-client "client_id" --session-type "portrait" \
  --photography-experience "professional"

# Search for portrait clients
python main.py crm search "portrait"

# View client details with project information
python main.py crm client "client_id"

# Add client note about preferences
python main.py crm add-note "client_id" "Client prefers natural lighting" \
  --title "Lighting Preferences" --type "follow_up"
```

### **Reminder Service**
```bash
# Run reminder service manually
python main.py --reminders

# Sync from Gmail
python main.py --sync
```

## 🧪 **Testing Professional Photography Features**

### **Test Basic Functionality**
```bash
python test_scheduler.py
```

### **Test CRM System**
```bash
python test_crm.py
```

### **Test Photography Business Features**
```bash
python test_photography_business.py
```

## 📁 **Project Structure**

```
SnapStudio/
├── web_app.py              # Flask web application (main entry point)
├── run_web_app.py         # Web application launcher
├── main.py                # CLI application (legacy)
├── scheduler/             # Core business logic
│   ├── models.py         # Data models (Client, Appointment, Milestone, Session)
│   ├── crm_manager.py    # CRM database operations
│   └── appointment_scheduler.py  # Scheduling logic with professional photography
├── templates/             # Jinja2 HTML templates for web interface
│   ├── dashboard.html    # Main dashboard
│   ├── appointments.html # Appointment management
│   ├── calendar.html     # Interactive calendar view
│   ├── clients.html      # Client management
│   ├── analytics.html    # Business analytics
│   └── backup_restore.html # Backup management
├── static/                # CSS, JavaScript, and static assets
├── config/                # Configuration management
├── gmail/                 # Gmail API integration
├── calendar_integration/  # Google Calendar operations
├── utils/                 # Utility functions
├── data/                  # SQLite database and data storage
├── backups/               # System backup files
├── logs/                  # Application logs
├── config.example.yaml    # Example configuration for professional photography
├── requirements.txt       # Python dependencies
├── test_scheduler.py      # Basic functionality tests
├── test_crm.py           # CRM system tests
├── test_photography_business.py # Professional photography business tests
└── README.md             # This file
```

## 🔧 **Advanced Professional Photography Features**

### **Database Management**
- SQLite database with proper indexing for photography business data
- Automatic backup and recovery
- Data export capabilities
- Migration tools for future upgrades

### **API Integration Ready**
- RESTful API structure for photography business workflows
- JSON data exchange
- Webhook support for external integrations
- Third-party service connectors

### **Reporting & Analytics for Professional Photography**
- Automated report generation by session type
- Multiple export formats (CSV, PDF, JSON)
- Scheduled reporting
- Custom KPI tracking for photography business

### **Marketing Tools for Professional Photography**
- Email campaign management for session reminders
- Referral program tracking
- Social media integration
- Client segmentation for targeted marketing

## 🔒 **Security Features**

- OAuth 2.0 authentication
- Secure credential storage
- API key protection
- Environment variable support
- Role-based access control ready

## 🚀 **Production Deployment for Professional Photography**

For production use:
1. **Database**: Upgrade to PostgreSQL or MySQL
2. **Web Interface**: Add Flask/Django web interface
3. **Authentication**: Implement user management system
4. **Monitoring**: Add logging and monitoring tools
5. **Backup**: Set up automated backup procedures
6. **SSL**: Enable HTTPS for web interface

## 📈 **Business Benefits for Professional Photography**

- **Increased Efficiency**: Automate client tracking and session scheduling
- **Better Client Relationships**: Track client preferences and project history
- **Revenue Optimization**: Analyze session performance and package sales
- **Marketing Insights**: Track referral sources and campaign effectiveness
- **Professional Image**: Automated, consistent communication
- **Data-Driven Decisions**: Comprehensive analytics and reporting
- **Package Sales**: Increase revenue with bundled services
- **Client Retention**: Keep clients coming back for multiple sessions

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 **License**

MIT License - see LICENSE file for details

## 🆘 **Support**

For support and questions:
1. Check the logs for error messages
2. Verify your configuration
3. Test with the provided test scripts
4. Open an issue in the repository

## 🔮 **Roadmap for Professional Photography**

- **Web Interface**: React/Vue.js web application
- **Mobile App**: iOS/Android mobile applications
- **Advanced Analytics**: Machine learning insights for client behavior
- **Payment Integration**: Stripe/PayPal integration
- **Multi-location Support**: Multiple studio locations
- **API Marketplace**: Third-party integrations
- **White-label Solution**: Resell to other photographers
- **Photography Guides**: Built-in session planning tools
- **Client Development Tracking**: Integration with business apps
- **Photo Gallery Sharing**: Secure client gallery sharing

---

**Transform your professional photography business with SnapStudio - comprehensive appointment scheduling and CRM management designed specifically for capturing life's most important moments!** 🎯📸✨
