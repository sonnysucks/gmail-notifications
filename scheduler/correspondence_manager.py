"""
Correspondence Manager for automated email scheduling and generation
Handles appointment-based email correspondence with SMTP integration
"""

import logging
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

from scheduler.models import Appointment, Client, Correspondence
from scheduler.crm_manager import CRMManager
from config.config_manager import ConfigManager
from gmail.gmail_manager import GmailManager

logger = logging.getLogger(__name__)


class CorrespondenceManager:
    """Manages automated email correspondence for appointments"""
    
    def __init__(self, config_manager: ConfigManager):
        """Initialize correspondence manager"""
        self.config = config_manager
        self.crm_manager = CRMManager(config_manager)
        self.gmail_manager = GmailManager(config_manager)
        
        # Email configuration
        self.smtp_config = self._get_smtp_config()
        self.business_info = config_manager.get_business_info()
        
    def _get_smtp_config(self) -> Dict[str, Any]:
        """Get SMTP configuration from config"""
        return {
            'smtp_server': self.config.get('email.smtp_server', 'smtp.gmail.com'),
            'smtp_port': self.config.get('email.smtp_port', 587),
            'username': self.config.get('email.username', ''),
            'password': self.config.get('email.password', ''),
            'use_tls': self.config.get('email.use_tls', True),
            'from_email': self.config.get('email.from_email', ''),
            'from_name': self.config.get('email.from_name', 'Sass and Whimsy Photography')
        }
    
    def _replace_template_placeholders(self, template: str, appointment: Appointment, client: Client) -> str:
        """Replace template placeholders with actual values"""
        business_name = self.business_info.get('name', 'Your Photography Business')
        
        replacements = {
            '{{ client_name }}': client.name,
            '{{ session_type }}': appointment.session_type,
            '{{ appointment_date }}': appointment.start_time.strftime('%A, %B %d, %Y at %I:%M %p'),
            '{{ business_name }}': business_name,
            '{{ client_email }}': client.email,
            '{{ client_phone }}': client.phone or '',
            '{{ appointment_duration }}': str(appointment.duration),
            '{{ appointment_location }}': appointment.location or 'Studio'
        }
        
        result = template
        for placeholder, value in replacements.items():
            result = result.replace(placeholder, value)
        
        return result
    
    def schedule_appointment_emails(self, appointment: Appointment) -> List[Correspondence]:
        """Schedule all emails for a new appointment"""
        try:
            correspondence_list = []
            
            # Get client information
            client = self.crm_manager.get_client(appointment.client_id)
            if not client:
                logger.error(f"Client {appointment.client_id} not found for appointment {appointment.id}")
                return []
            
            # 1. Contract & Checklist Email (14 days before)
            contract_email = self._create_contract_checklist_email(appointment, client)
            if contract_email:
                correspondence_list.append(contract_email)
            
            # 2. Session Package Email (7 days before)
            package_email = self._create_session_package_email(appointment, client)
            if package_email:
                correspondence_list.append(package_email)
            
            # 3. Reminder Email (3 days before)
            reminder_email = self._create_reminder_email(appointment, client)
            if reminder_email:
                correspondence_list.append(reminder_email)
            
            # 4. Thank You & Marketing Email (15 minutes after session start)
            thank_you_email = self._create_thank_you_email(appointment, client)
            if thank_you_email:
                correspondence_list.append(thank_you_email)
            
            # Save all correspondence to database
            for correspondence in correspondence_list:
                success = self.crm_manager.add_correspondence(correspondence)
                if success:
                    logger.info(f"Scheduled {correspondence.email_type} email for appointment {appointment.id}")
                else:
                    logger.error(f"Failed to schedule {correspondence.email_type} email for appointment {appointment.id}")
            
            return correspondence_list
            
        except Exception as e:
            logger.error(f"Failed to schedule emails for appointment {appointment.id}: {e}")
            return []
    
    def _create_contract_checklist_email(self, appointment: Appointment, client: Client) -> Optional[Correspondence]:
        """Create contract and checklist email (14 days before)"""
        try:
            scheduled_time = appointment.start_time - timedelta(days=14)
            
            # Get email template from config
            email_templates = self.config.get('email_templates', {})
            contract_template = email_templates.get('contract_checklist', {})
            
            # Use template or fallback to default
            subject_template = contract_template.get('subject', 'Your Photography Session Contract & Checklist - {{ client_name }}')
            body_template = contract_template.get('body', '''Dear {{ client_name }},

Thank you for booking your {{ session_type }} session with us! Your appointment is scheduled for {{ appointment_date }}.

Please find attached your photography contract and session checklist. Please review and sign the contract, and use the checklist to prepare for your session.

If you have any questions, please don't hesitate to contact us.

Best regards,
{{ business_name }}''')
            
            # Replace placeholders
            subject = self._replace_template_placeholders(subject_template, appointment, client)
            body = self._replace_template_placeholders(body_template, appointment, client)
            
            html_body = f"""
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #6366f1;">Contract & Checklist</h2>
        
        <p>Dear {client.name},</p>
        
        <p>Thank you for booking your <strong>{appointment.session_type}</strong> session with Sass and Whimsy Photography!</p>
        
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <h3 style="margin-top: 0;">Session Details</h3>
            <p><strong>Date:</strong> {appointment.start_time.strftime('%A, %B %d, %Y')}</p>
            <p><strong>Time:</strong> {appointment.start_time.strftime('%I:%M %p')}</p>
            <p><strong>Duration:</strong> {appointment.duration} minutes</p>
        </div>
        
        <h3>Attachments:</h3>
        <ul>
            <li>Photography Contract</li>
            <li>Session Checklist</li>
            <li>Preparation Guide</li>
        </ul>
        
        <p>Please review and sign the contract, and use the checklist to prepare for your session.</p>
        
        <p>If you have any questions, please don't hesitate to contact us.</p>
        
        <p>Best regards,<br>
        Sass and Whimsy Photography<br>
        {self.business_info.get('phone', '')}<br>
        {self.business_info.get('email', '')}</p>
    </div>
</body>
</html>
"""
            
            return Correspondence(
                appointment_id=appointment.id,
                client_id=client.id,
                client_name=client.name,
                client_email=client.email,
                email_type='contract_checklist',
                subject=subject,
                body=body,
                html_body=html_body,
                scheduled_time=scheduled_time,
                status='pending',
                template_used='contract_checklist_template',
                session_type=appointment.session_type,
                appointment_date=appointment.start_time,
                attachments=['contract.pdf', 'checklist.pdf', 'preparation_guide.pdf']
            )
            
        except Exception as e:
            logger.error(f"Failed to create contract checklist email: {e}")
            return None
    
    def _create_session_package_email(self, appointment: Appointment, client: Client) -> Optional[Correspondence]:
        """Create session package email (7 days before)"""
        try:
            scheduled_time = appointment.start_time - timedelta(days=7)
            
            # Get email template from config
            email_templates = self.config.get('email_templates', {})
            package_template = email_templates.get('session_package', {})
            
            # Use template or fallback to default
            subject_template = package_template.get('subject', 'Your Session Package & Preparation Guide - {{ client_name }}')
            body_template = package_template.get('body', '''Dear {{ client_name }},

Your {{ session_type }} session is coming up in just 7 days! We're excited to work with you.

Please find your session package attached, which includes:
- Session preparation guide
- What to expect during your session
- Wardrobe suggestions
- Location information

Your appointment is scheduled for {{ appointment_date }}. Please arrive 10 minutes early.

See you soon!
{{ business_name }}''')
            
            # Replace placeholders
            subject = self._replace_template_placeholders(subject_template, appointment, client)
            body = self._replace_template_placeholders(body_template, appointment, client)
            
            html_body = f"""
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #6366f1;">Session Package & Details</h2>
        
        <p>Dear {client.name},</p>
        
        <p>Your <strong>{appointment.session_type}</strong> session is coming up in one week!</p>
        
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <h3 style="margin-top: 0;">Session Details</h3>
            <p><strong>Date:</strong> {appointment.start_time.strftime('%A, %B %d, %Y')}</p>
            <p><strong>Time:</strong> {appointment.start_time.strftime('%I:%M %p')}</p>
            <p><strong>Duration:</strong> {appointment.duration} minutes</p>
            <p><strong>Location:</strong> {appointment.location or 'Studio'}</p>
        </div>
        
        <h3>Your Session Package Includes:</h3>
        <ul>
            <li>Session details and timeline</li>
            <li>What to expect during the session</li>
            <li>Wardrobe suggestions</li>
            <li>Props and setup information</li>
        </ul>
        
        <p>We're excited to capture these special moments for you!</p>
        
        <p>Best regards,<br>
        Sass and Whimsy Photography<br>
        {self.business_info.get('phone', '')}<br>
        {self.business_info.get('email', '')}</p>
    </div>
</body>
</html>
"""
            
            return Correspondence(
                appointment_id=appointment.id,
                client_id=client.id,
                client_name=client.name,
                client_email=client.email,
                email_type='session_package',
                subject=subject,
                body=body,
                html_body=html_body,
                scheduled_time=scheduled_time,
                status='pending',
                template_used='session_package_template',
                session_type=appointment.session_type,
                appointment_date=appointment.start_time,
                attachments=['session_package.pdf']
            )
            
        except Exception as e:
            logger.error(f"Failed to create session package email: {e}")
            return None
    
    def _create_reminder_email(self, appointment: Appointment, client: Client) -> Optional[Correspondence]:
        """Create reminder email (3 days before)"""
        try:
            scheduled_time = appointment.start_time - timedelta(days=3)
            
            # Get email template from config
            email_templates = self.config.get('email_templates', {})
            reminder_template = email_templates.get('reminder', {})
            
            # Use template or fallback to default
            subject_template = reminder_template.get('subject', 'Reminder: Your Photography Session is in 3 Days - {{ client_name }}')
            body_template = reminder_template.get('body', '''Hi {{ client_name }},

Just a friendly reminder that your {{ session_type }} session is scheduled for {{ appointment_date }}.

Please make sure you've reviewed the preparation materials we sent earlier. If you have any last-minute questions, feel free to reach out.

We're looking forward to capturing beautiful memories for you!

Best,
{{ business_name }}''')
            
            # Replace placeholders
            subject = self._replace_template_placeholders(subject_template, appointment, client)
            body = self._replace_template_placeholders(body_template, appointment, client)
            
            html_body = f"""
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #6366f1;">Session Reminder</h2>
        
        <p>Dear {client.name},</p>
        
        <p>This is a friendly reminder about your <strong>{appointment.session_type}</strong> session:</p>
        
        <div style="background-color: #fff3cd; padding: 15px; border-radius: 5px; margin: 20px 0; border-left: 4px solid #ffc107;">
            <h3 style="margin-top: 0;">Session Details</h3>
            <p><strong>Date:</strong> {appointment.start_time.strftime('%A, %B %d, %Y')}</p>
            <p><strong>Time:</strong> {appointment.start_time.strftime('%I:%M %p')}</p>
            <p><strong>Location:</strong> {appointment.location or 'Studio'}</p>
        </div>
        
        <p><strong>Please arrive 10 minutes early</strong> to allow time for setup and preparation.</p>
        
        <p>If you need to reschedule or have any questions, please contact us as soon as possible.</p>
        
        <p>We look forward to seeing you!</p>
        
        <p>Best regards,<br>
        Sass and Whimsy Photography<br>
        {self.business_info.get('phone', '')}<br>
        {self.business_info.get('email', '')}</p>
    </div>
</body>
</html>
"""
            
            return Correspondence(
                appointment_id=appointment.id,
                client_id=client.id,
                client_name=client.name,
                client_email=client.email,
                email_type='reminder',
                subject=subject,
                body=body,
                html_body=html_body,
                scheduled_time=scheduled_time,
                status='pending',
                template_used='reminder_template',
                session_type=appointment.session_type,
                appointment_date=appointment.start_time
            )
            
        except Exception as e:
            logger.error(f"Failed to create reminder email: {e}")
            return None
    
    def _create_thank_you_email(self, appointment: Appointment, client: Client) -> Optional[Correspondence]:
        """Create thank you and marketing email (15 minutes after session start)"""
        try:
            scheduled_time = appointment.start_time + timedelta(minutes=15)
            
            # Get email template from config
            email_templates = self.config.get('email_templates', {})
            thank_you_template = email_templates.get('thank_you', {})
            
            # Use template or fallback to default
            subject_template = thank_you_template.get('subject', 'Thank You for Your Session! - {{ client_name }}')
            body_template = thank_you_template.get('body', '''Dear {{ client_name }},

Thank you so much for choosing us for your {{ session_type }} session! We had a wonderful time working with you and your family.

Your photos will be ready for review in approximately 2-3 weeks. We'll send you a link to your private online gallery as soon as they're ready.

In the meantime, feel free to follow us on social media for photography tips and to see some of our recent work:
- Instagram: @yourphotography
- Facebook: Your Photography Business

Thank you again for trusting us with your precious memories!

Warm regards,
{{ business_name }}''')
            
            # Replace placeholders
            subject = self._replace_template_placeholders(subject_template, appointment, client)
            body = self._replace_template_placeholders(body_template, appointment, client)
            
            html_body = f"""
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #6366f1;">Thank You!</h2>
        
        <p>Dear {client.name},</p>
        
        <p>Thank you for choosing Sass and Whimsy Photography for your <strong>{appointment.session_type}</strong> session!</p>
        
        <p>We had a wonderful time capturing these special moments for you. Your photos will be ready for review within 2-3 weeks.</p>
        
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <h3 style="margin-top: 0;">What's Next:</h3>
            <ul>
                <li>We'll send you a link to your online gallery</li>
                <li>You can select your favorite images</li>
                <li>Additional prints and products are available</li>
            </ul>
        </div>
        
        <div style="background-color: #e7f3ff; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <h3 style="margin-top: 0; color: #0066cc;">Special Offers:</h3>
            <ul>
                <li><strong>20% off</strong> additional prints when ordered within 30 days</li>
                <li><strong>Refer a friend</strong> and both receive $50 off your next session</li>
                <li><strong>Follow us</strong> on social media for exclusive deals</li>
            </ul>
        </div>
        
        <p>Thank you again for trusting us with your precious memories!</p>
        
        <p>Best regards,<br>
        Sass and Whimsy Photography<br>
        {self.business_info.get('phone', '')}<br>
        {self.business_info.get('email', '')}</p>
    </div>
</body>
</html>
"""
            
            return Correspondence(
                appointment_id=appointment.id,
                client_id=client.id,
                client_name=client.name,
                client_email=client.email,
                email_type='thank_you',
                subject=subject,
                body=body,
                html_body=html_body,
                scheduled_time=scheduled_time,
                status='pending',
                template_used='thank_you_template',
                session_type=appointment.session_type,
                appointment_date=appointment.start_time
            )
            
        except Exception as e:
            logger.error(f"Failed to create thank you email: {e}")
            return None
    
    def send_pending_emails(self) -> int:
        """Send all pending emails that are due"""
        try:
            pending_correspondence = self.crm_manager.get_pending_correspondence()
            sent_count = 0
            
            for correspondence in pending_correspondence:
                try:
                    # Try Gmail API first
                    if self._is_gmail_configured():
                        success = self._send_via_gmail(correspondence)
                    else:
                        # Fallback to SMTP
                        success = self._send_via_smtp(correspondence)
                    
                    if success:
                        self.crm_manager.update_correspondence_status(
                            correspondence.id, 'sent', correspondence.email_message_id
                        )
                        sent_count += 1
                        logger.info(f"Sent {correspondence.email_type} email to {correspondence.client_email}")
                    else:
                        self.crm_manager.update_correspondence_status(correspondence.id, 'failed')
                        logger.error(f"Failed to send {correspondence.email_type} email to {correspondence.client_email}")
                        
                except Exception as e:
                    logger.error(f"Error sending email {correspondence.id}: {e}")
                    self.crm_manager.update_correspondence_status(correspondence.id, 'failed')
            
            return sent_count
            
        except Exception as e:
            logger.error(f"Failed to send pending emails: {e}")
            return 0
    
    def _is_gmail_configured(self) -> bool:
        """Check if Gmail API is properly configured"""
        try:
            # Check if Gmail service is available
            return self.gmail_manager.service is not None
        except:
            return False
    
    def _send_via_gmail(self, correspondence: Correspondence) -> bool:
        """Send email via Gmail API"""
        try:
            message_id = self.gmail_manager.send_email(
                to=correspondence.client_email,
                subject=correspondence.subject,
                body=correspondence.body,
                html_body=correspondence.html_body
            )
            
            correspondence.email_message_id = message_id
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email via Gmail: {e}")
            return False
    
    def _send_via_smtp(self, correspondence: Correspondence) -> bool:
        """Send email via SMTP"""
        try:
            if not self.smtp_config.get('username') or not self.smtp_config.get('password'):
                logger.warning("SMTP credentials not configured, email will be generated for correspondence page")
                return False
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{self.smtp_config['from_name']} <{self.smtp_config['from_email']}>"
            msg['To'] = correspondence.client_email
            msg['Subject'] = correspondence.subject
            
            # Add text and HTML parts
            text_part = MIMEText(correspondence.body, 'plain')
            msg.attach(text_part)
            
            if correspondence.html_body:
                html_part = MIMEText(correspondence.html_body, 'html')
                msg.attach(html_part)
            
            # Send email
            server = smtplib.SMTP(self.smtp_config['smtp_server'], self.smtp_config['smtp_port'])
            if self.smtp_config['use_tls']:
                server.starttls()
            server.login(self.smtp_config['username'], self.smtp_config['password'])
            
            text = msg.as_string()
            server.sendmail(self.smtp_config['from_email'], correspondence.client_email, text)
            server.quit()
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email via SMTP: {e}")
            return False
    
    def get_correspondence_for_appointment(self, appointment_id: str) -> List[Correspondence]:
        """Get all correspondence for a specific appointment"""
        return self.crm_manager.get_appointment_correspondence(appointment_id)
    
    def cancel_appointment_correspondence(self, appointment_id: str) -> bool:
        """Cancel all pending correspondence for an appointment"""
        try:
            correspondence_list = self.crm_manager.get_appointment_correspondence(appointment_id)
            
            for correspondence in correspondence_list:
                if correspondence.status == 'pending':
                    self.crm_manager.update_correspondence_status(correspondence.id, 'cancelled')
            
            logger.info(f"Cancelled correspondence for appointment {appointment_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to cancel correspondence for appointment {appointment_id}: {e}")
            return False
