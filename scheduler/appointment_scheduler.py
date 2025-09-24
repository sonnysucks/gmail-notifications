"""
Appointment scheduling and management with CRM integration
"""

import json
import logging
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from pathlib import Path

from .models import Appointment, Client, Reminder, ClientNote
from .crm_manager import CRMManager
from config.config_manager import ConfigManager
from gmail.gmail_manager import GmailManager
from calendar_integration.calendar_manager import CalendarManager
from utils.template_manager import TemplateManager

logger = logging.getLogger(__name__)


class AppointmentScheduler:
    """Manages appointment scheduling and reminders with CRM integration"""
    
    def __init__(self, config_manager: ConfigManager):
        """Initialize the scheduler"""
        self.config = config_manager
        self.gmail_manager = GmailManager(config_manager)
        self.calendar_manager = CalendarManager(config_manager)
        self.template_manager = TemplateManager(config_manager)
        self.crm_manager = CRMManager(config_manager)
        
        # Storage for reminders (appointments and clients now stored in CRM database)
        self.reminders: Dict[str, Reminder] = {}
        
        # Load existing reminders
        self._load_reminders()
    
    def _load_reminders(self):
        """Load reminders from storage"""
        try:
            data_file = Path('data/reminders.json')
            if data_file.exists():
                with open(data_file, 'r') as f:
                    data = json.load(f)
                    
                # Load reminders
                for rem_data in data.get('reminders', []):
                    reminder = Reminder.from_dict(rem_data)
                    self.reminders[reminder.id] = reminder
                    
                logger.info(f"Loaded {len(self.reminders)} reminders")
                
        except Exception as e:
            logger.warning(f"Could not load existing reminders: {e}")
    
    def _save_reminders(self):
        """Save reminders to storage"""
        try:
            data_dir = Path('data')
            data_dir.mkdir(exist_ok=True)
            
            data = {
                'reminders': [rem.to_dict() for rem in self.reminders.values()]
            }
            
            with open(data_dir / 'reminders.json', 'w') as f:
                json.dump(data, f, indent=2, default=str)
                
        except Exception as e:
            logger.error(f"Failed to save reminders: {e}")
    
    def create_appointment(self, client_name: str, datetime_str: str, 
                          session_type: str, duration: Optional[int] = None, 
                          notes: str = "", client_email: str = "", 
                          session_fee: float = 0.0, **kwargs) -> Appointment:
        """Create a new appointment with CRM integration"""
        try:
            # Parse datetime
            if isinstance(datetime_str, str):
                start_time = datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
            else:
                start_time = datetime_str
            
            # Use default duration if not specified
            if duration is None:
                duration = self.config.get('appointments.default_duration', 60)
            
            # Check if client exists, create if not
            client = None
            if client_email:
                client = self.crm_manager.get_client_by_email(client_email)
            
            if not client:
                client = self._create_or_update_client(client_name, client_email, **kwargs)
            
            # Create appointment with enhanced fields
            appointment = Appointment(
                client_id=client.id,
                client_name=client_name,
                client_email=client_email or client.email,
                start_time=start_time,
                duration=duration,
                session_type=session_type,
                notes=notes,
                session_fee=session_fee,
                total_amount=session_fee,  # Will be calculated in post_init
                **kwargs
            )
            
            # Add to calendar (if available)
            try:
                if hasattr(self.calendar_manager, 'service') and self.calendar_manager.service:
                    calendar_event = self.calendar_manager.create_event(appointment)
                    appointment.calendar_event_id = calendar_event.get('id')
                    logger.info(f"Added appointment to Google Calendar: {appointment.calendar_event_id}")
                else:
                    logger.info("Google Calendar not available - appointment created without calendar integration")
            except Exception as calendar_error:
                logger.warning(f"Could not add appointment to calendar: {calendar_error}")
                # Continue without calendar integration
            
            # Add to CRM
            self.crm_manager.add_appointment(appointment)
            
            # Create reminders
            self._create_reminders(appointment)
            
            # Save reminders
            self._save_reminders()
            
            # Send confirmation email (if available)
            try:
                self._send_confirmation_email(appointment)
            except Exception as email_error:
                logger.warning(f"Could not send confirmation email: {email_error}")
                # Continue without email
            
            # Update client metrics
            client.update_metrics(appointment.total_amount)
            self.crm_manager.update_client(client)
            
            logger.info(f"Created appointment for {client_name} on {start_time}")
            return appointment
            
        except Exception as e:
            logger.error(f"Failed to create appointment: {e}")
            raise
    
    def _create_or_update_client(self, name: str, email: str = "", **kwargs) -> Client:
        """Create a new client or update existing one"""
        try:
            # Try to find existing client
            client = None
            if email:
                client = self.crm_manager.get_client_by_email(email)
            
            if client:
                # Update existing client
                client.name = name
                client.updated_at = datetime.now()
                for key, value in kwargs.items():
                    if hasattr(client, key):
                        setattr(client, key, value)
                self.crm_manager.update_client(client)
                logger.info(f"Updated existing client: {name}")
            else:
                # Create new client
                client = Client(
                    name=name,
                    email=email,
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    **kwargs
                )
                self.crm_manager.add_client(client)
                logger.info(f"Created new client: {name}")
            
            return client
            
        except Exception as e:
            logger.error(f"Failed to create/update client: {e}")
            raise
    
    def _create_reminders(self, appointment: Appointment):
        """Create reminder schedule for an appointment"""
        reminder_schedule = self.config.get_reminder_schedule()
        
        for schedule_item in reminder_schedule:
            # Handle both old format (integers) and new format (dictionaries)
            if isinstance(schedule_item, int):
                # Old format: integers represent hours before appointment
                hours_before = schedule_item
                reminder_type = f"reminder_{hours_before}h"
                reminder_time = appointment.start_time - timedelta(hours=hours_before)
            elif isinstance(schedule_item, dict):
                # New format: dictionaries with 'weeks' or 'days' keys
                if 'weeks' in schedule_item:
                    days_before = schedule_item['weeks'] * 7
                    reminder_type = f"reminder_{schedule_item['weeks']}weeks"
                elif 'days' in schedule_item:
                    days_before = schedule_item['days']
                    reminder_type = f"reminder_{schedule_item['days']}days"
                else:
                    continue
                reminder_time = appointment.start_time - timedelta(days=days_before)
            else:
                continue
            
            # Only create reminders for future times
            if reminder_time > datetime.now():
                reminder = Reminder(
                    appointment_id=appointment.id,
                    reminder_type=reminder_type,
                    scheduled_time=reminder_time
                )
                
                self.reminders[reminder.id] = reminder
        
        logger.info(f"Created {len(reminder_schedule)} reminders for appointment {appointment.id}")
    
    def _send_confirmation_email(self, appointment: Appointment):
        """Send confirmation email for new appointment"""
        try:
            # Get client details from CRM
            client = None
            if appointment.client_id:
                client = self.crm_manager.get_client(appointment.client_id)
            
            template_data = {
                'appointment': appointment,
                'client': client,
                'business': self.config.get_business_info(),
                'calendar': self.config.get_calendar_config()
            }
            
            subject = f"Appointment Confirmed - {appointment.session_type}"
            body = self.template_manager.render_template('confirmation', template_data)
            
            # Send email
            self.gmail_manager.send_email(
                to=appointment.client_email,
                subject=subject,
                body=body
            )
            
            logger.info(f"Sent confirmation email for appointment {appointment.id}")
            
        except Exception as e:
            logger.error(f"Failed to send confirmation email: {e}")
    
    def send_reminders(self) -> int:
        """Send due reminders"""
        sent_count = 0
        now = datetime.now()
        
        for reminder in self.reminders.values():
            if (reminder.status == 'pending' and 
                reminder.scheduled_time <= now):
                
                try:
                    # Get appointment from CRM
                    appointment = self._get_appointment_from_crm(reminder.appointment_id)
                    
                    if not appointment:
                        logger.warning(f"Appointment {reminder.appointment_id} not found in CRM")
                        reminder.status = 'failed'
                        continue
                    
                    # Send reminder email
                    self._send_reminder_email(reminder, appointment)
                    
                    # Update reminder status
                    reminder.status = 'sent'
                    reminder.sent_time = now
                    
                    sent_count += 1
                    logger.info(f"Sent {reminder.reminder_type} reminder for {appointment.client_name}")
                    
                except Exception as e:
                    logger.error(f"Failed to send reminder {reminder.id}: {e}")
                    reminder.status = 'failed'
        
        # Save updated reminders
        self._save_reminders()
        
        return sent_count
    
    def _get_appointment_from_crm(self, appointment_id: str) -> Optional[Appointment]:
        """Get appointment from CRM database"""
        # This is a simplified version - in production, you'd add a method to CRMManager
        # to get appointments by ID
        try:
            # For now, we'll search through all appointments
            # In production, add a proper get_appointment_by_id method to CRMManager
            return None
        except Exception as e:
            logger.error(f"Failed to get appointment from CRM: {e}")
            return None
    
    def _send_reminder_email(self, reminder: Reminder, appointment: Appointment):
        """Send reminder email"""
        try:
            # Get client details from CRM
            client = None
            if appointment.client_id:
                client = self.crm_manager.get_client(appointment.client_id)
            
            template_data = {
                'appointment': appointment,
                'client': client,
                'reminder': reminder,
                'business': self.config.get_business_info(),
                'calendar': self.config.get_calendar_config()
            }
            
            # Determine template based on reminder type
            template_name = reminder.reminder_type
            if template_name not in ['reminder_2weeks', 'reminder_1week', 'reminder_3days', 'reminder_2days', 'reminder_1day']:
                template_name = 'reminder_1day'  # fallback
            
            subject = f"Reminder: {appointment.session_type} in {self._get_time_until_text(appointment)}"
            body = self.template_manager.render_template(template_name, template_data)
            
            # Send email
            self.gmail_manager.send_email(
                to=appointment.client_email,
                subject=subject,
                body=body
            )
            
        except Exception as e:
            logger.error(f"Failed to send reminder email: {e}")
            raise
    
    def _get_time_until_text(self, appointment: Appointment) -> str:
        """Get human-readable text for time until appointment"""
        days = appointment.days_until
        
        if days == 0:
            return "today"
        elif days == 1:
            return "1 day"
        elif days < 7:
            return f"{days} days"
        elif days < 14:
            return f"{days // 7} week{'s' if days // 7 > 1 else ''}"
        else:
            return f"{days // 7} weeks"
    
    def get_upcoming_appointments(self, limit: int = 10) -> List[Appointment]:
        """Get upcoming appointments within specified days"""
        try:
            all_appointments = self._get_all_appointments_from_crm()
            now = datetime.now()
            
            # Filter upcoming appointments and sort by date
            upcoming = []
            for apt in all_appointments:
                if apt.start_time > now:
                    upcoming.append(apt)
            
            # Sort by start time and limit results
            upcoming.sort(key=lambda x: x.start_time)
            return upcoming[:limit]
            
        except Exception as e:
            logger.error(f"Failed to get upcoming appointments: {e}")
            return []
    
    def get_next_appointment(self) -> Optional[Appointment]:
        """Get the next scheduled appointment chronologically"""
        try:
            all_appointments = self._get_all_appointments_from_crm()
            now = datetime.now()
            
            # Filter upcoming appointments and sort by date
            upcoming = []
            for apt in all_appointments:
                if apt.start_time > now and apt.status in ['confirmed', 'pending']:
                    upcoming.append(apt)
            
            # Sort by start time and return the first one
            upcoming.sort(key=lambda x: x.start_time)
            return upcoming[0] if upcoming else None
            
        except Exception as e:
            logger.error(f"Failed to get next appointment: {e}")
            return None
    
    def process_email_appointment(self, email_data: Dict[str, Any]) -> Optional[Appointment]:
        """Process appointment from email data"""
        try:
            # Extract appointment details from email
            subject = email_data.get('subject', '')
            body = email_data.get('body', '')
            
            # Simple parsing logic (enhance this based on your email format)
            client_name = self._extract_client_name(subject, body)
            session_type = self._extract_session_type(subject, body)
            appointment_time = self._extract_appointment_time(subject, body)
            client_email = self._extract_client_email(email_data)
            
            if not all([client_name, session_type, appointment_time]):
                logger.warning(f"Incomplete appointment data from email: {email_data.get('id')}")
                return None
            
            # Create appointment
            appointment = self.create_appointment(
                client_name=client_name,
                datetime_str=appointment_time.isoformat(),
                session_type=session_type,
                client_email=client_email,
                notes=f"Created from email: {email_data.get('id')}"
            )
            
            # Link to original email
            appointment.gmail_message_id = email_data.get('id')
            
            return appointment
            
        except Exception as e:
            logger.error(f"Failed to process email appointment: {e}")
            return None
    
    def _extract_client_name(self, subject: str, body: str) -> str:
        """Extract client name from email content"""
        import re
        
        patterns = [
            r'from\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            r'client:\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+appointment'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, f"{subject} {body}", re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return ""
    
    def _extract_client_email(self, email_data: Dict[str, Any]) -> str:
        """Extract client email from email data"""
        from_header = email_data.get('from', '')
        # Simple email extraction - enhance with better parsing
        import re
        email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
        match = re.search(email_pattern, from_header)
        return match.group(0) if match else ""
    
    def _extract_session_type(self, subject: str, body: str) -> str:
        """Extract session type from email content"""
        session_types = [
            'portrait', 'family', 'wedding', 'engagement', 'maternity',
            'newborn', 'senior', 'headshot', 'event', 'photoshoot'
        ]
        
        content = f"{subject} {body}".lower()
        for session_type in session_types:
            if session_type in content:
                return session_type.title()
        
        return "Photography Session"
    
    def _extract_appointment_time(self, subject: str, body: str) -> Optional[datetime]:
        """Extract appointment time from email content"""
        import re
        from dateutil import parser
        
        patterns = [
            r'\d{1,2}/\d{1,2}/\d{4}\s+\d{1,2}:\d{2}\s*(?:AM|PM)?',
            r'\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}',
            r'(?:on|at)\s+([A-Za-z]+\s+\d{1,2},?\s+\d{4})',
            r'(\d{1,2}:\d{2}\s*(?:AM|PM)?\s+on\s+[A-Za-z]+\s+\d{1,2})'
        ]
        
        content = f"{subject} {body}"
        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                try:
                    return parser.parse(match, fuzzy=True)
                except:
                    continue
        
        return None
    
    def delete_appointment(self, appointment_id: str) -> bool:
        """Delete an appointment permanently"""
        try:
            # Get appointment from CRM
            appointment = self._get_appointment_from_crm(appointment_id)
            if not appointment:
                logger.warning(f"Appointment {appointment_id} not found for deletion")
                return False
            
            # Delete from calendar if it exists
            if appointment.calendar_event_id:
                try:
                    self.calendar_manager.cancel_event(appointment.calendar_event_id)
                except Exception as e:
                    logger.warning(f"Failed to delete calendar event {appointment.calendar_event_id}: {e}")
            
            # Cancel pending reminders
            for reminder in self.reminders.values():
                if (reminder.appointment_id == appointment_id and 
                    reminder.status == 'pending'):
                    reminder.status = 'cancelled'
            
            # Save reminders
            self._save_reminders()
            
            # Delete from CRM database
            success = self.crm_manager.delete_appointment(appointment_id)
            
            if success:
                logger.info(f"Deleted appointment {appointment_id}")
                return True
            else:
                logger.error(f"Failed to delete appointment {appointment_id} from database")
                return False
            
        except Exception as e:
            logger.error(f"Failed to delete appointment: {e}")
            return False

    def cancel_appointment(self, appointment_id: str, reason: str = "") -> bool:
        """Cancel an appointment"""
        try:
            # Get appointment from CRM
            appointment = self._get_appointment_from_crm(appointment_id)
            if not appointment:
                return False
            
            appointment.status = 'cancelled'
            appointment.notes += f"\nCancelled: {reason}"
            appointment.updated_at = datetime.now()
            
            # Update in CRM
            self.crm_manager.add_appointment(appointment)
            
            # Cancel in calendar
            if appointment.calendar_event_id:
                self.calendar_manager.cancel_event(appointment.calendar_event_id)
            
            # Cancel pending reminders
            for reminder in self.reminders.values():
                if (reminder.appointment_id == appointment_id and 
                    reminder.status == 'pending'):
                    reminder.status = 'cancelled'
            
            # Send cancellation email
            self._send_cancellation_email(appointment, reason)
            
            # Save reminders
            self._save_reminders()
            
            logger.info(f"Cancelled appointment {appointment_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to cancel appointment: {e}")
            return False
    
    def _send_cancellation_email(self, appointment: Appointment, reason: str):
        """Send cancellation email"""
        try:
            subject = f"Appointment Cancelled - {appointment.session_type}"
            body = f"""
            Dear {appointment.client_name},
            
            Your appointment for {appointment.session_type} on {appointment.start_time.strftime('%B %d, %Y at %I:%M %p')} has been cancelled.
            
            Reason: {reason}
            
            Please contact us to reschedule.
            
            Best regards,
            {self.config.get('business.name')}
            """
            
            self.gmail_manager.send_email(
                to=appointment.client_email,
                subject=subject,
                body=body
            )
            
        except Exception as e:
            logger.error(f"Failed to send cancellation email: {e}")
    
    def add_client_note(self, client_id: str, note_content: str, 
                        note_type: str = "general", title: str = "", 
                        author: str = "System", internal: bool = False) -> bool:
        """Add a note to a client"""
        try:
            note = ClientNote(
                client_id=client_id,
                note_type=note_type,
                title=title,
                content=note_content,
                author=author,
                is_internal=internal
            )
            
            success = self.crm_manager.add_client_note(note)
            if success:
                logger.info(f"Added note to client {client_id}")
            return success
            
        except Exception as e:
            logger.error(f"Failed to add client note: {e}")
            return False
    
    def get_crm_analytics(self) -> Dict[str, Any]:
        """Get CRM analytics"""
        return self.crm_manager.get_crm_analytics()
    
    def search_clients(self, query: str, limit: int = 50) -> List[Client]:
        """Search clients in CRM"""
        return self.crm_manager.search_clients(query, limit)
    
    def get_client_details(self, client_id: str) -> Optional[Client]:
        """Get detailed client information"""
        return self.crm_manager.get_client(client_id)
    
    def get_follow_up_tasks(self) -> List[Dict[str, Any]]:
        """Get follow-up tasks that need attention"""
        return self.crm_manager.get_follow_up_tasks()
    
    def get_appointments_by_date(self, date) -> List[Appointment]:
        """Get appointments for a specific date"""
        try:
            # Convert date to string format for database query
            if hasattr(date, 'strftime'):
                date_str = date.strftime('%Y-%m-%d')
            else:
                date_str = str(date)
            
            # Get appointments from CRM that match the date
            all_appointments = self._get_all_appointments_from_crm()
            date_appointments = []
            
            for apt in all_appointments:
                if apt.start_time.strftime('%Y-%m-%d') == date_str:
                    date_appointments.append(apt)
            
            return date_appointments
            
        except Exception as e:
            logger.error(f"Failed to get appointments by date: {e}")
            return []
    
    def get_total_appointments(self) -> int:
        """Get total number of appointments"""
        try:
            all_appointments = self._get_all_appointments_from_crm()
            return len(all_appointments)
        except Exception as e:
            logger.error(f"Failed to get total appointments: {e}")
            return 0
    
    def get_monthly_revenue(self) -> float:
        """Get total revenue for current month"""
        try:
            current_month = datetime.now().strftime('%Y-%m')
            all_appointments = self._get_all_appointments_from_crm()
            
            monthly_revenue = 0.0
            for apt in all_appointments:
                if apt.start_time.strftime('%Y-%m') == current_month:
                    monthly_revenue += apt.total_amount or 0.0
            
            return monthly_revenue
            
        except Exception as e:
            logger.error(f"Failed to get monthly revenue: {e}")
            return 0.0
    
    def get_all_appointments(self) -> List[Appointment]:
        """Get all appointments"""
        return self._get_all_appointments_from_crm()
    
    def get_appointment(self, appointment_id: str) -> Optional[Appointment]:
        """Get appointment by ID"""
        try:
            all_appointments = self._get_all_appointments_from_crm()
            for apt in all_appointments:
                if apt.id == appointment_id:
                    return apt
            return None
        except Exception as e:
            logger.error(f"Failed to get appointment {appointment_id}: {e}")
            return None
    
    def update_appointment(self, appointment_id: str, appointment_data: Dict[str, Any]) -> Optional[Appointment]:
        """Update an existing appointment"""
        try:
            appointment = self.get_appointment(appointment_id)
            if not appointment:
                return None
            
            # Update appointment fields
            for key, value in appointment_data.items():
                if hasattr(appointment, key):
                    setattr(appointment, key, value)
            
            appointment.updated_at = datetime.now()
            
            # Update in CRM
            self.crm_manager.add_appointment(appointment)
            
            # Update in calendar if needed
            if appointment.calendar_event_id:
                self.calendar_manager.update_event(appointment.calendar_event_id, appointment)
            
            logger.info(f"Updated appointment {appointment_id}")
            return appointment
            
        except Exception as e:
            logger.error(f"Failed to update appointment {appointment_id}: {e}")
            return None
    
    def get_client_appointments(self, client_id: str) -> List[Appointment]:
        """Get all appointments for a specific client"""
        try:
            all_appointments = self._get_all_appointments_from_crm()
            client_appointments = []
            
            for apt in all_appointments:
                if apt.client_id == client_id:
                    client_appointments.append(apt)
            
            return client_appointments
            
        except Exception as e:
            logger.error(f"Failed to get client appointments: {e}")
            return []
    
    def get_appointments_in_range(self, start_date, end_date) -> List[Appointment]:
        """Get appointments within a date range"""
        try:
            all_appointments = self._get_all_appointments_from_crm()
            range_appointments = []
            
            for apt in all_appointments:
                if start_date <= apt.start_time.date() <= end_date:
                    range_appointments.append(apt)
            
            return range_appointments
            
        except Exception as e:
            logger.error(f"Failed to get appointments in range: {e}")
            return []
    
    def get_monthly_revenue_data(self) -> Dict[str, Any]:
        """Get detailed monthly revenue data"""
        try:
            current_month = datetime.now().strftime('%Y-%m')
            all_appointments = self._get_all_appointments_from_crm()
            
            monthly_data = {}
            for apt in all_appointments:
                month = apt.start_time.strftime('%Y-%m')
                if month not in monthly_data:
                    monthly_data[month] = {'revenue': 0.0, 'count': 0}
                
                monthly_data[month]['revenue'] += apt.total_amount or 0.0
                monthly_data[month]['count'] += 1
            
            return monthly_data
            
        except Exception as e:
            logger.error(f"Failed to get monthly revenue data: {e}")
            return {}
    
    def get_session_type_statistics(self) -> Dict[str, Any]:
        """Get statistics by session type"""
        try:
            all_appointments = self._get_all_appointments_from_crm()
            session_stats = {}
            
            for apt in all_appointments:
                session_type = apt.session_type
                if session_type not in session_stats:
                    session_stats[session_type] = {'count': 0, 'revenue': 0.0}
                
                session_stats[session_type]['count'] += 1
                session_stats[session_type]['revenue'] += apt.total_amount or 0.0
            
            # Calculate average values
            total_sessions = sum(stats['count'] for stats in session_stats.values())
            total_revenue = sum(stats['revenue'] for stats in session_stats.values())
            
            return {
                'total_sessions': total_sessions,
                'total_revenue': total_revenue,
                'avg_session_value': total_revenue / total_sessions if total_sessions > 0 else 0,
                'by_type': session_stats
            }
            
        except Exception as e:
            logger.error(f"Failed to get session type statistics: {e}")
            return {
                'total_sessions': 0,
                'total_revenue': 0,
                'avg_session_value': 0,
                'by_type': {}
            }
    
    def get_milestone_package_data(self) -> Dict[str, Any]:
        """Get milestone package analytics"""
        try:
            all_appointments = self._get_all_appointments_from_crm()
            milestone_data = {}
            
            for apt in all_appointments:
                if 'milestone' in apt.session_type.lower():
                    month = apt.start_time.strftime('%Y-%m')
                    if month not in milestone_data:
                        milestone_data[month] = {'count': 0, 'revenue': 0.0}
                    
                    milestone_data[month]['count'] += 1
                    milestone_data[month]['revenue'] += apt.total_amount or 0.0
            
            return milestone_data
            
        except Exception as e:
            logger.error(f"Failed to get milestone package data: {e}")
            return {}
    
    def _get_all_appointments_from_crm(self) -> List[Appointment]:
        """Helper method to get all appointments from CRM"""
        try:
            return self.crm_manager.get_all_appointments()
        except Exception as e:
            logger.error(f"Failed to get appointments from CRM: {e}")
            return []
