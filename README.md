# Gmail Photography Appointment Scheduler

A professional appointment scheduling system for photography businesses that integrates with Gmail and Google Calendar to automatically manage client appointments and send reminder notifications.

## Features

- **Automatic Appointment Scheduling**: Create appointments directly from Gmail
- **Smart Reminder System**: Automated notifications at 2 weeks, 1 week, 3 days, 2 days, and 1 day before appointments
- **Google Calendar Integration**: Works with any Google Calendar as the target
- **Professional Templates**: Photography-specific email templates for confirmations and reminders
- **Client Management**: Track client information and appointment history
- **Time Zone Handling**: Automatic time zone detection and conversion

## Prerequisites

- Python 3.8+
- Google Cloud Platform account
- Gmail API enabled
- Google Calendar API enabled
- OAuth 2.0 credentials

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd gmail-notifications
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up Google Cloud credentials:
   - Create a project in Google Cloud Console
   - Enable Gmail API and Google Calendar API
   - Create OAuth 2.0 credentials
   - Download the credentials JSON file and save as `credentials.json`

4. Configure the application:
```bash
cp config.example.yaml config.yaml
# Edit config.yaml with your settings
```

## Configuration

Edit `config.yaml` to configure:
- Target Google Calendar ID
- Photography business details
- Email templates
- Reminder schedules
- Time zone settings

## Usage

### Basic Setup
```bash
python main.py --setup
```

### Schedule Appointment
```bash
python main.py --schedule "Client Name" "2024-01-15 14:00" "Portrait Session"
```

### Run Reminder Service
```bash
python main.py --reminders
```

### Check Appointments
```bash
python main.py --list
```

## Architecture

- **main.py**: Main application entry point
- **scheduler/**: Core scheduling logic
- **gmail/**: Gmail API integration
- **calendar/**: Google Calendar operations
- **templates/**: Email templates
- **utils/**: Utility functions
- **config/**: Configuration management

## Security

- OAuth 2.0 authentication
- Secure credential storage
- API key protection
- Environment variable usage for sensitive data

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For support and questions, please open an issue in the repository.
