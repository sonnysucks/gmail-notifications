# Gmail Photography Appointment Scheduler with CRM
## Specialized for Maternity, Baby, Smash Cake, and Birthday Photography

A comprehensive **web-based** appointment scheduling and Customer Relationship Management (CRM) system **specifically designed for baby photography businesses**. Features a modern Flask web application with interactive calendar, business analytics, and complete backup/restore functionality.

## 🌐 **Web Application (Primary Interface)**

**Quick Start**: `python run_web_app.py` → Open `http://localhost:5001` → Login: `admin` / `admin123`

### **Key Web Features**
- **📊 Dashboard**: Business overview with metrics and quick actions
- **📅 Interactive Calendar**: Visual appointment management with clickable days
- **👥 Client Management**: Complete CRM with family and baby tracking
- **📈 Analytics**: Revenue tracking, session statistics, client metrics
- **💾 Backup & Restore**: Complete system backup and data management
- **⚙️ Configuration**: Comprehensive business setup and customization

## 🍼 **Baby Photography Specialization**

This system is **tailor-made** for photographers specializing in:
- **Maternity Photography** - Beautiful pregnancy sessions (28-36 weeks)
- **Newborn Photography** - Precious first 14 days of life
- **Baby Milestone Sessions** - 3, 6, 9, 12, 18, 24 months
- **Smash Cake Photography** - 1st birthday celebrations
- **Birthday Photography** - Themed sessions for all ages
- **Family Portraits** - Growing family memories

## 🚀 **Specialized Baby Photography Features**

### **Milestone Tracking & Automation**
- **Automatic Age Calculations**: Track baby age in days, weeks, and months
- **Milestone Reminders**: Automated notifications for upcoming milestones
- **Session Planning**: Age-appropriate session recommendations
- **Package Management**: Complete first-year milestone packages

### **Baby-Specific Client Management**
- **Family Type Tracking**: Expecting, newborn, baby, toddler, multiple children
- **Due Date Management**: Countdown to baby's arrival
- **Children Database**: Track multiple children per family
- **Photography Experience**: First-time vs. experienced parents
- **Referral Sources**: Pediatrician, hospital, daycare referrals

### **Specialized Session Types**
- **Maternity Sessions**: 90-minute sessions with props included
- **Newborn Sessions**: 3-hour sessions with backup date flexibility
- **Milestone Sessions**: Age-specific timing and duration
- **Smash Cake Sessions**: Cake included with cleanup service
- **Birthday Sessions**: Theme selection with props and colors
- **Package Deals**: Discounted milestone packages

### **Advanced Baby Photography Tools**
- **Theme Management**: Princess, superhero, farm, space, ocean themes
- **Color Coordination**: Predefined color palettes for sessions
- **Props Tracking**: Balloons, banners, crowns, capes, stuffed animals
- **Cake Management**: Flavors, designs, and dietary preferences
- **Sibling Integration**: Include siblings in milestone sessions

## ✨ **Core Features**

- **Automatic Appointment Scheduling**: Create appointments directly from Gmail
- **Smart Reminder System**: Automated notifications at 2 weeks, 1 week, 3 days, 2 days, and 1 day before appointments
- **Google Calendar Integration**: Works with any Google Calendar as the target
- **Professional Email Templates**: Baby photography-specific email templates for all communications
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
- **Baby Photography Focused**: Built specifically for baby photography workflows

## 📊 **CRM Capabilities for Baby Photography**

### **Client Management**
- Comprehensive client profiles with family information
- Baby tracking with birth dates and milestone planning
- Family size and composition management
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
- Revenue analytics by session type
- Client acquisition and retention metrics
- Milestone package performance analysis
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
cd gmail-notifications
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

## ⚙️ **Configuration for Baby Photography**

Edit `config.yaml` to configure:
- **Business Information**: Studio details, contact info, tax information
- **Session Types & Pricing**: Predefined baby photography services with pricing
- **Baby Photography Settings**: Milestone tracking, newborn preferences, smash cake options
- **CRM Settings**: Client tags, referral sources, family types, experience levels
- **Calendar Settings**: Target calendar, business hours, timezone
- **Email Templates**: Customizable templates for all baby photography communications
- **Analytics**: KPI tracking and reporting preferences

## 🎯 **Usage for Baby Photography**

### **Web Application Usage (Recommended)**

1. **Access the web interface**: `http://localhost:5001`
2. **Login**: `admin` / `admin123`
3. **Navigate through the interface**:
   - **Dashboard**: Overview of business metrics
   - **Appointments**: Create, edit, view appointments
   - **Calendar**: Interactive calendar with appointment visualization
   - **Clients**: Manage client information and family details
   - **Analytics**: View business performance and revenue
   - **Setup**: Configure business settings and preferences
   - **Backup & Restore**: Manage system backups

### **CLI Application Usage (Legacy)**

#### **Basic Setup**
```bash
python main.py --setup
```

#### **Baby Photography Appointment Management**
```bash
# Schedule newborn session with baby details
python main.py --schedule "Sarah Johnson" "2024-01-15 10:00" "Newborn Session" \
  --baby-name "Baby Emma" --baby-age-days 7 --milestone-type "newborn" \
  --parent-names "Sarah, Mike" --email "sarah@email.com" --fee 350.00

# Schedule milestone session
python main.py --schedule "Lisa Smith" "2024-02-01 14:00" "6 Month Milestone" \
  --baby-name "Baby Liam" --baby-age-days 180 --milestone-type "6month" \
  --email "lisa@email.com" --fee 225.00

# Schedule smash cake session
python main.py --schedule "Jennifer Davis" "2024-03-15 11:00" "Smash Cake Session" \
  --baby-name "Baby Ava" --baby-age-days 365 --milestone-type "1year" \
  --email "jennifer@email.com" --fee 275.00
```

### **Baby Photography CRM Operations**
```bash
# Add baby information to client
python main.py baby add-baby "client_id" "Baby Emma" "2024-01-08" \
  --notes "First baby, very excited parents"

# Check upcoming milestones
python main.py baby milestones "client_id"

# Update family information
python main.py baby update-family "client_id" --due-date "2024-06-15" \
  --family-type "expecting" --photography-experience "first_time"

# Search for maternity clients
python main.py crm search "maternity"

# View client details with baby information
python main.py crm client "client_id"

# Add client note about baby preferences
python main.py crm add-note "client_id" "Baby prefers natural lighting" \
  --title "Lighting Preferences" --type "follow_up"
```

### **Reminder Service**
```bash
# Run reminder service manually
python main.py --reminders

# Sync from Gmail
python main.py --sync
```

## 🧪 **Testing Baby Photography Features**

### **Test Basic Functionality**
```bash
python test_scheduler.py
```

### **Test CRM System**
```bash
python test_crm.py
```

### **Test Baby Photography Features**
```bash
python test_baby_photography.py
```

## 📁 **Project Structure**

```
gmail-notifications/
├── web_app.py              # Flask web application (main entry point)
├── run_web_app.py         # Web application launcher
├── main.py                # CLI application (legacy)
├── scheduler/             # Core business logic
│   ├── models.py         # Data models (Client, Appointment, BabyMilestone, BirthdaySession)
│   ├── crm_manager.py    # CRM database operations
│   └── appointment_scheduler.py  # Scheduling logic with baby photography
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
├── config.example.yaml    # Example configuration for baby photography
├── requirements.txt       # Python dependencies
├── test_scheduler.py      # Basic functionality tests
├── test_crm.py           # CRM system tests
├── test_baby_photography.py # Baby photography specific tests
└── README.md             # This file
```

## 🔧 **Advanced Baby Photography Features**

### **Database Management**
- SQLite database with proper indexing for baby photography data
- Automatic backup and recovery
- Data export capabilities
- Migration tools for future upgrades

### **API Integration Ready**
- RESTful API structure for baby photography workflows
- JSON data exchange
- Webhook support for external integrations
- Third-party service connectors

### **Reporting & Analytics for Baby Photography**
- Automated report generation by session type
- Multiple export formats (CSV, PDF, JSON)
- Scheduled reporting
- Custom KPI tracking for baby photography business

### **Marketing Tools for Baby Photography**
- Email campaign management for milestone reminders
- Referral program tracking
- Social media integration
- Client segmentation for targeted marketing

## 🔒 **Security Features**

- OAuth 2.0 authentication
- Secure credential storage
- API key protection
- Environment variable support
- Role-based access control ready

## 🚀 **Production Deployment for Baby Photography**

For production use:
1. **Database**: Upgrade to PostgreSQL or MySQL
2. **Web Interface**: Add Flask/Django web interface
3. **Authentication**: Implement user management system
4. **Monitoring**: Add logging and monitoring tools
5. **Backup**: Set up automated backup procedures
6. **SSL**: Enable HTTPS for web interface

## 📈 **Business Benefits for Baby Photography**

- **Increased Efficiency**: Automate milestone tracking and session scheduling
- **Better Client Relationships**: Track baby development and family preferences
- **Revenue Optimization**: Analyze session performance and package sales
- **Marketing Insights**: Track referral sources and campaign effectiveness
- **Professional Image**: Automated, consistent communication
- **Data-Driven Decisions**: Comprehensive analytics and reporting
- **Milestone Package Sales**: Increase revenue with bundled services
- **Client Retention**: Keep families coming back for each milestone

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

## 🔮 **Roadmap for Baby Photography**

- **Web Interface**: React/Vue.js web application
- **Mobile App**: iOS/Android mobile applications
- **Advanced Analytics**: Machine learning insights for milestone timing
- **Payment Integration**: Stripe/PayPal integration
- **Multi-location Support**: Multiple studio locations
- **API Marketplace**: Third-party integrations
- **White-label Solution**: Resell to other baby photographers
- **Milestone Photography Guides**: Built-in session planning tools
- **Baby Development Tracking**: Integration with pediatric apps
- **Family Photo Sharing**: Secure gallery sharing for families

---

**Transform your baby photography business with professional appointment scheduling and comprehensive CRM management designed specifically for capturing life's precious moments!** 🎯📸👶
