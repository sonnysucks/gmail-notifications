# Setup Guide for Gmail Photography Appointment Scheduler

This guide will walk you through setting up the Gmail Photography Appointment Scheduler step by step.

## Prerequisites

- Python 3.8 or higher
- Google Cloud Platform account
- Gmail account
- Google Calendar access

## Step 1: Clone and Setup the Repository

```bash
# Clone the repository
git clone <your-repo-url>
cd gmail-notifications

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Google Cloud Platform Setup

### 2.1 Create a New Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Enter a project name (e.g., "Photography Scheduler")
4. Click "Create"

### 2.2 Enable APIs

1. In your project, go to "APIs & Services" → "Library"
2. Search for and enable these APIs:
   - Gmail API
   - Google Calendar API

### 2.3 Create OAuth 2.0 Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth 2.0 Client IDs"
3. Choose "Desktop application"
4. Give it a name (e.g., "Photography Scheduler Desktop")
5. Click "Create"
6. Download the JSON file and save it as `credentials.json` in your project root

## Step 3: Configuration

### 3.1 Copy Configuration File

```bash
cp config.example.yaml config.yaml
```

### 3.2 Edit Configuration

Open `config.yaml` and customize it for your business:

```yaml
# Business Information
business:
  name: "Your Photography Business Name"
  email: "your-email@gmail.com"
  phone: "+1-555-0123"
  website: "https://yourphotography.com"
  address: "123 Photography St, City, State 12345"

# Google Calendar Settings
calendar:
  target_calendar_id: "primary"  # Use "primary" for main calendar
  timezone: "America/New_York"    # Your business timezone
  business_hours:
    start: "09:00"
    end: "17:00"
    days: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

# Appointment Settings
appointments:
  default_duration: 60  # minutes
  buffer_time: 15       # minutes between appointments
  reminder_schedule:
    - weeks: 2          # 2 weeks before
    - weeks: 1          # 1 week before
    - days: 3           # 3 days before
    - days: 2           # 2 days before
    - days: 1           # 1 day before

# Email Templates
email:
  from_name: "Your Photography Business"
  reply_to: "your-email@gmail.com"
```

## Step 4: Initial Setup

### 4.1 Run Setup Command

```bash
python main.py --setup
```

This will:
- Authenticate with Google (opens browser for OAuth)
- Create necessary Gmail labels
- Test calendar access
- Create default email templates

### 4.2 Verify Setup

```bash
# Test the system
python test_scheduler.py

# Check available commands
python main.py --help
```

## Step 5: Using the System

### 5.1 Schedule an Appointment

```bash
python main.py --schedule "John Doe" "2024-01-15 14:00" "Portrait Session" --duration 90 --notes "Outdoor location preferred"
```

### 5.2 List Appointments

```bash
python main.py --list --days 30
```

### 5.3 Run Reminders Manually

```bash
python main.py --reminders
```

### 5.4 Sync from Gmail

```bash
python main.py --sync
```

## Step 6: Automation (Optional)

### 6.1 Cron Job for Reminders

Set up a cron job to run reminders automatically:

```bash
# Edit crontab
crontab -e

# Add this line to run reminders every hour
0 * * * * cd /path/to/your/project && python run_reminders.py

# Or run reminders daily at 9 AM
0 9 * * * cd /path/to/your/project && python run_reminders.py
```

### 6.2 Systemd Service (Linux)

Create a systemd service for automated reminders:

```bash
sudo nano /etc/systemd/system/photography-reminders.service
```

Add this content:

```ini
[Unit]
Description=Photography Appointment Reminders
After=network.target

[Service]
Type=oneshot
User=your-username
WorkingDirectory=/path/to/your/project
ExecStart=/usr/bin/python3 run_reminders.py
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl enable photography-reminders.service
sudo systemctl start photography-reminders.service
```

## Step 7: Testing

### 7.1 Test Appointment Creation

1. Create a test appointment for tomorrow
2. Check your Google Calendar
3. Verify confirmation email was sent

### 7.2 Test Reminders

1. Create an appointment for 3 days from now
2. Wait for the reminder to be sent
3. Check the logs: `tail -f logs/appointments.log`

### 7.3 Test Gmail Integration

1. Send yourself an email with "appointment" in the subject
2. Run: `python main.py --sync`
3. Check if appointment was created

## Troubleshooting

### Common Issues

#### Authentication Errors
- Ensure `credentials.json` is in the project root
- Check that APIs are enabled in Google Cloud Console
- Verify OAuth consent screen is configured

#### Calendar Access Issues
- Check calendar ID in config.yaml
- Ensure calendar is shared with your account
- Verify calendar permissions

#### Email Sending Issues
- Check Gmail API quotas
- Verify sender email in configuration
- Check logs for specific error messages

### Logs

Check the logs for detailed information:

```bash
# View recent logs
tail -f logs/appointments.log

# View reminder logs
tail -f logs/reminders.log
```

### Debug Mode

Run commands with verbose logging:

```bash
python main.py --verbose --setup
```

## Security Considerations

- Keep `credentials.json` secure and never commit it to version control
- Use environment variables for sensitive configuration in production
- Regularly rotate OAuth tokens
- Monitor API usage and quotas

## Support

If you encounter issues:

1. Check the logs for error messages
2. Verify your configuration
3. Test with the provided test script
4. Check Google Cloud Console for API quotas and errors

## Next Steps

Once the basic system is working:

1. Customize email templates in the `templates/` directory
2. Set up automated reminder scheduling
3. Integrate with your existing workflow
4. Monitor and optimize performance

## Production Deployment

For production use:

1. Use a proper database instead of JSON files
2. Set up proper logging and monitoring
3. Use environment variables for configuration
4. Set up backup and recovery procedures
5. Monitor API usage and costs
