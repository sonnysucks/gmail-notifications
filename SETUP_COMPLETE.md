# Gmail Notifications System - Setup Complete! 🎉

## 🚀 Quick Start

1. **Activate Virtual Environment:**
   ```bash
   source .venv/bin/activate  # On macOS/Linux
   # or
   .venv\Scripts\activate   # On Windows
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
