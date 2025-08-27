# Gmail Photography Appointment Scheduler with CRM

A comprehensive appointment scheduling and Customer Relationship Management (CRM) system for photography businesses that integrates with Gmail and Google Calendar to automatically manage client appointments, send reminder notifications, and track customer relationships.

## 🚀 **New CRM Features**

- **Complete Customer Database**: Store comprehensive client information including contact details, preferences, and history
- **Appointment History Tracking**: Full appointment lifecycle management with financial tracking
- **Advanced Notes System**: Organized client notes with internal/external visibility controls
- **Business Intelligence**: Analytics dashboard with revenue tracking, client metrics, and performance insights
- **Marketing Campaign Management**: Track campaigns, referral sources, and client acquisition
- **Follow-up Task Management**: Automated follow-up reminders and task tracking
- **Client Segmentation**: Tag-based client organization and filtering
- **Financial Management**: Session pricing, payment tracking, and revenue analytics

## ✨ **Core Features**

- **Automatic Appointment Scheduling**: Create appointments directly from Gmail
- **Smart Reminder System**: Automated notifications at 2 weeks, 1 week, 3 days, 2 days, and 1 day before appointments
- **Google Calendar Integration**: Works with any Google Calendar as the target
- **Professional Email Templates**: Photography-specific email templates for confirmations and reminders
- **Time Zone Handling**: Automatic time zone detection and conversion
- **Gmail Integration**: Scan emails for appointment requests and manage communication

## 🏗️ **Architecture**

- **SQLite Database**: Robust CRM database with proper indexing and relationships
- **Modular Design**: Clean separation of concerns (Gmail, Calendar, Scheduler, CRM, Templates)
- **RESTful API Ready**: Designed for easy web interface integration
- **Scalable**: Can be upgraded to PostgreSQL or MySQL for production use

## 📊 **CRM Capabilities**

### **Client Management**
- Comprehensive client profiles with contact information
- Business details and industry classification
- Social media integration and website tracking
- Referral source tracking and analysis
- Client tags and categorization system
- Budget range and project type classification

### **Appointment Tracking**
- Full appointment lifecycle management
- Financial tracking (session fees, additional charges, discounts)
- Payment status monitoring
- Equipment and location requirements
- Priority levels and special instructions
- Follow-up task automation

### **Business Intelligence**
- Revenue analytics and forecasting
- Client acquisition and retention metrics
- Session type performance analysis
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

1. **Clone the repository**:
```bash
git clone <your-repo-url>
cd gmail-notifications
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up Google Cloud credentials**:
   - Create a project in Google Cloud Console
   - Enable Gmail API and Google Calendar API
   - Create OAuth 2.0 credentials
   - Download the credentials JSON file and save as `credentials.json`

4. **Configure the application**:
```bash
cp config.example.yaml config.yaml
# Edit config.yaml with your business settings
```

## ⚙️ **Configuration**

Edit `config.yaml` to configure:
- **Business Information**: Company details, contact info, tax information
- **Session Types & Pricing**: Predefined session types with durations and pricing
- **CRM Settings**: Client tags, referral sources, budget ranges, industries
- **Calendar Settings**: Target calendar, business hours, timezone
- **Email Templates**: Customizable email templates for all communications
- **Analytics**: KPI tracking and reporting preferences

## 🎯 **Usage**

### **Basic Setup**
```bash
python main.py --setup
```

### **Appointment Management**
```bash
# Schedule appointment with CRM integration
python main.py --schedule "Client Name" "2024-01-15 14:00" "Portrait Session" \
  --email "client@example.com" --fee 150.00 --location "Studio"

# List upcoming appointments
python main.py --list --days 30

# Cancel appointment
python main.py --cancel "appointment_id" "Client requested reschedule"
```

### **CRM Operations**
```bash
# Search for clients
python main.py crm search "John Doe"

# Get client details
python main.py crm client "client_id"

# Add client note
python main.py crm add-note "client_id" "Client prefers outdoor sessions" \
  --title "Session Preferences" --type "follow_up"

# View CRM analytics
python main.py crm analytics

# Check follow-up tasks
python main.py crm follow-ups
```

### **Reminder Service**
```bash
# Run reminder service manually
python main.py --reminders

# Sync from Gmail
python main.py --sync
```

## 🧪 **Testing**

### **Test Basic Functionality**
```bash
python test_scheduler.py
```

### **Test CRM System**
```bash
python test_crm.py
```

## 📁 **Project Structure**

```
gmail-notifications/
├── main.py                 # Main CLI application
├── config/                 # Configuration management
├── scheduler/              # Appointment scheduling + CRM
│   ├── models.py          # Data models (Client, Appointment, etc.)
│   ├── crm_manager.py     # CRM database operations
│   └── appointment_scheduler.py  # Scheduling logic
├── gmail/                  # Gmail API integration
├── calendar/               # Google Calendar operations
├── templates/              # Email templates
├── utils/                  # Utility functions
├── data/                   # CRM database and data storage
├── logs/                   # Application logs
├── config.example.yaml     # Example configuration
├── requirements.txt        # Python dependencies
├── test_scheduler.py       # Basic functionality tests
├── test_crm.py            # CRM system tests
└── README.md              # This file
```

## 🔧 **Advanced Features**

### **Database Management**
- SQLite database with proper indexing
- Automatic backup and recovery
- Data export capabilities
- Migration tools for future upgrades

### **API Integration Ready**
- RESTful API structure
- JSON data exchange
- Webhook support for external integrations
- Third-party service connectors

### **Reporting & Analytics**
- Automated report generation
- Multiple export formats (CSV, PDF, JSON)
- Scheduled reporting
- Custom KPI tracking

### **Marketing Tools**
- Email campaign management
- Referral program tracking
- Social media integration
- Client segmentation for targeted marketing

## 🔒 **Security Features**

- OAuth 2.0 authentication
- Secure credential storage
- API key protection
- Environment variable support
- Role-based access control ready

## 🚀 **Production Deployment**

For production use:
1. **Database**: Upgrade to PostgreSQL or MySQL
2. **Web Interface**: Add Flask/Django web interface
3. **Authentication**: Implement user management system
4. **Monitoring**: Add logging and monitoring tools
5. **Backup**: Set up automated backup procedures
6. **SSL**: Enable HTTPS for web interface

## 📈 **Business Benefits**

- **Increased Efficiency**: Automate appointment scheduling and reminders
- **Better Client Relationships**: Track all interactions and preferences
- **Revenue Optimization**: Analyze session performance and pricing
- **Marketing Insights**: Track referral sources and campaign effectiveness
- **Professional Image**: Automated, consistent communication
- **Data-Driven Decisions**: Comprehensive analytics and reporting

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

## 🔮 **Roadmap**

- **Web Interface**: React/Vue.js web application
- **Mobile App**: iOS/Android mobile applications
- **Advanced Analytics**: Machine learning insights
- **Payment Integration**: Stripe/PayPal integration
- **Multi-location Support**: Multiple studio locations
- **API Marketplace**: Third-party integrations
- **White-label Solution**: Resell to other photographers

---

**Transform your photography business with professional appointment scheduling and comprehensive CRM management!** 🎯📸
