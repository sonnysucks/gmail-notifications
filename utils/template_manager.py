"""
Email template management and rendering
"""

import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from jinja2 import Environment, FileSystemLoader, Template

from config.config_manager import ConfigManager

logger = logging.getLogger(__name__)


class TemplateManager:
    """Manages email templates and rendering"""
    
    def __init__(self, config_manager: ConfigManager):
        """Initialize template manager"""
        self.config = config_manager
        self.template_dir = Path('templates')
        self.env = None
        self._setup_jinja()
    
    def _setup_jinja(self):
        """Setup Jinja2 environment"""
        try:
            # Create templates directory if it doesn't exist
            self.template_dir.mkdir(exist_ok=True)
            
            # Setup Jinja2 environment
            self.env = Environment(
                loader=FileSystemLoader(str(self.template_dir)),
                autoescape=True,
                trim_blocks=True,
                lstrip_blocks=True
            )
            
            # Add custom filters
            self.env.filters['format_date'] = self._format_date
            self.env.filters['format_time'] = self._format_time
            self.env.filters['format_duration'] = self._format_duration
            
            logger.info(f"Template environment initialized with directory: {self.template_dir}")
            
        except Exception as e:
            logger.error(f"Failed to setup template environment: {e}")
            raise
    
    def render_template(self, template_name: str, context: Dict[str, Any]) -> str:
        """Render a template with the given context"""
        try:
            # Get template path from config
            template_path = self.config.get_template_path(template_name)
            
            if template_path and os.path.exists(template_path):
                # Use configured template path
                with open(template_path, 'r', encoding='utf-8') as f:
                    template_content = f.read()
                
                template = Template(template_content)
            else:
                # Try to load from templates directory
                template = self.env.get_template(f"{template_name}.html")
            
            # Render template
            rendered = template.render(**context)
            logger.debug(f"Rendered template {template_name}")
            
            return rendered
            
        except Exception as e:
            logger.error(f"Failed to render template {template_name}: {e}")
            # Return fallback template
            return self._get_fallback_template(template_name, context)
    
    def _get_fallback_template(self, template_name: str, context: Dict[str, Any]) -> str:
        """Get a fallback template if the main template fails"""
        try:
            if template_name == 'confirmation':
                return self._render_confirmation_fallback(context)
            elif 'reminder' in template_name:
                return self._render_reminder_fallback(context)
            else:
                return self._render_generic_fallback(context)
                
        except Exception as e:
            logger.error(f"Failed to render fallback template: {e}")
            return "Email content could not be rendered."
    
    def _render_confirmation_fallback(self, context: Dict[str, Any]) -> str:
        """Render fallback confirmation email"""
        appointment = context.get('appointment', {})
        business = context.get('business', {})
        
        return f"""
Dear {appointment.get('client_name', 'Client')},

Your appointment has been confirmed!

Details:
- Session: {appointment.get('session_type', 'Photography Session')}
- Date: {appointment.get('start_time', 'TBD')}
- Duration: {appointment.get('duration', 60)} minutes

We look forward to working with you!

Best regards,
{business.get('name', 'Your Photography Business')}

Contact Information:
Phone: {business.get('phone', 'N/A')}
Email: {business.get('email', 'N/A')}
Website: {business.get('website', 'N/A')}
"""
    
    def _render_reminder_fallback(self, context: Dict[str, Any]) -> str:
        """Render fallback reminder email"""
        appointment = context.get('appointment', {})
        business = context.get('business', {})
        
        return f"""
Dear {appointment.get('client_name', 'Client')},

This is a friendly reminder about your upcoming appointment!

Details:
- Session: {appointment.get('session_type', 'Photography Session')}
- Date: {appointment.get('start_time', 'TBD')}
- Duration: {appointment.get('duration', 60)} minutes

Please arrive 10 minutes early to ensure we start on time.

If you need to reschedule or have any questions, please contact us as soon as possible.

Best regards,
{business.get('name', 'Your Photography Business')}

Contact Information:
Phone: {business.get('phone', 'N/A')}
Email: {business.get('email', 'N/A')}
"""
    
    def _render_generic_fallback(self, context: Dict[str, Any]) -> str:
        """Render generic fallback email"""
        business = context.get('business', {})
        
        return f"""
Dear Client,

This is an automated message from {business.get('name', 'Your Photography Business')}.

If you have any questions, please contact us.

Best regards,
{business.get('name', 'Your Photography Business')}

Contact Information:
Phone: {business.get('phone', 'N/A')}
Email: {business.get('email', 'N/A')}
"""
    
    def _format_date(self, date_obj) -> str:
        """Format date for display"""
        try:
            if hasattr(date_obj, 'strftime'):
                return date_obj.strftime('%B %d, %Y')
            return str(date_obj)
        except:
            return str(date_obj)
    
    def _format_time(self, time_obj) -> str:
        """Format time for display"""
        try:
            if hasattr(time_obj, 'strftime'):
                return time_obj.strftime('%I:%M %p')
            return str(time_obj)
        except:
            return str(time_obj)
    
    def _format_duration(self, minutes: int) -> str:
        """Format duration in minutes to human readable format"""
        try:
            minutes = int(minutes)
            if minutes < 60:
                return f"{minutes} minutes"
            elif minutes == 60:
                return "1 hour"
            else:
                hours = minutes // 60
                remaining_minutes = minutes % 60
                if remaining_minutes == 0:
                    return f"{hours} hours"
                else:
                    return f"{hours} hours {remaining_minutes} minutes"
        except:
            return f"{minutes} minutes"
    
    def create_default_templates(self):
        """Create default email templates if they don't exist"""
        try:
            templates = {
                'confirmation.html': self._get_confirmation_template(),
                'reminder_2weeks.html': self._get_reminder_template(2, 'weeks'),
                'reminder_1week.html': self._get_reminder_template(1, 'week'),
                'reminder_3days.html': self._get_reminder_template(3, 'days'),
                'reminder_2days.html': self._get_reminder_template(2, 'days'),
                'reminder_1day.html': self._get_reminder_template(1, 'day')
            }
            
            for filename, content in templates.items():
                template_path = self.template_dir / filename
                if not template_path.exists():
                    with open(template_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    logger.info(f"Created default template: {filename}")
            
        except Exception as e:
            logger.error(f"Failed to create default templates: {e}")
    
    def _get_confirmation_template(self) -> str:
        """Get default confirmation email template"""
        return """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Appointment Confirmation</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background-color: #f8f9fa; padding: 20px; text-align: center; border-radius: 5px; }
        .content { padding: 20px; }
        .details { background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0; }
        .footer { text-align: center; padding: 20px; color: #666; font-size: 14px; }
        .button { display: inline-block; padding: 10px 20px; background-color: #007bff; color: white; text-decoration: none; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Appointment Confirmed!</h1>
            <p>Your photography session has been scheduled</p>
        </div>
        
        <div class="content">
            <p>Dear {{ appointment.client_name }},</p>
            
            <p>Great news! Your appointment has been confirmed and we're excited to work with you.</p>
            
            <div class="details">
                <h3>Appointment Details:</h3>
                <ul>
                    <li><strong>Session Type:</strong> {{ appointment.session_type }}</li>
                    <li><strong>Date:</strong> {{ appointment.start_time|format_date }}</li>
                    <li><strong>Time:</strong> {{ appointment.start_time|format_time }}</li>
                    <li><strong>Duration:</strong> {{ appointment.duration|format_duration }}</li>
                    {% if appointment.notes %}
                    <li><strong>Notes:</strong> {{ appointment.notes }}</li>
                    {% endif %}
                </ul>
            </div>
            
            <p>Please arrive 10 minutes before your scheduled time to ensure we start promptly.</p>
            
            <p>If you need to reschedule or have any questions, please contact us as soon as possible.</p>
            
            <p>We look forward to creating beautiful memories with you!</p>
        </div>
        
        <div class="footer">
            <p><strong>{{ business.name }}</strong></p>
            <p>Phone: {{ business.phone }} | Email: {{ business.email }}</p>
            {% if business.website %}
            <p>Website: <a href="{{ business.website }}">{{ business.website }}</a></p>
            {% endif %}
            {% if business.address %}
            <p>Address: {{ business.address }}</p>
            {% endif %}
        </div>
    </div>
</body>
</html>"""
    
    def _get_reminder_template(self, amount: int, unit: str) -> str:
        """Get default reminder email template"""
        return """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Appointment Reminder</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background-color: #fff3cd; padding: 20px; text-align: center; border-radius: 5px; border: 1px solid #ffeaa7; }
        .content { padding: 20px; }
        .details { background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0; }
        .footer { text-align: center; padding: 20px; color: #666; font-size: 14px; }
        .urgent { color: #dc3545; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Appointment Reminder</h1>
            <p>Your session is coming up in """ + str(amount) + " " + unit + ("s" if amount > 1 else "") + """!</p>
        </div>
        
        <div class="content">
            <p>Dear {{ appointment.client_name }},</p>
            
            <p>This is a friendly reminder about your upcoming photography session.</p>
            
            <div class="details">
                <h3>Appointment Details:</h3>
                <ul>
                    <li><strong>Session Type:</strong> {{ appointment.session_type }}</li>
                    <li><strong>Date:</strong> {{ appointment.start_time|format_date }}</li>
                    <li><strong>Time:</strong> {{ appointment.start_time|format_time }}</li>
                    <li><strong>Duration:</strong> {{ appointment.duration|format_duration }}</li>
                    {% if appointment.notes %}
                    <li><strong>Notes:</strong> {{ appointment.notes }}</li>
                    {% endif %}
                </ul>
            </div>
            
            <p class="urgent">Please arrive 10 minutes early to ensure we start on time.</p>
            
            <p>If you need to reschedule or have any questions, please contact us immediately.</p>
            
            <p>We're looking forward to capturing your special moments!</p>
        </div>
        
        <div class="footer">
            <p><strong>{{ business.name }}</strong></p>
            <p>Phone: {{ business.phone }} | Email: {{ business.email }}</p>
            {% if business.website %}
            <p>Website: <a href="{{ business.website }}">{{ business.website }}</a></p>
            {% endif %}
            {% if business.address %}
            <p>Address: {{ business.address }}</p>
            {% endif %}
        </div>
    </div>
</body>
</html>"""
