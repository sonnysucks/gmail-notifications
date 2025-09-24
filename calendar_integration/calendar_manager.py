"""
Google Calendar API integration and event management
"""

import os
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import pytz

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config.config_manager import ConfigManager
from scheduler.models import Appointment

logger = logging.getLogger(__name__)

# Google Calendar API scopes
SCOPES = ['https://www.googleapis.com/auth/calendar']


class CalendarManager:
    """Manages Google Calendar operations and API integration"""
    
    def __init__(self, config_manager: ConfigManager):
        """Initialize calendar manager"""
        self.config = config_manager
        self.service = None
        self.credentials = None
        self.calendar_id = None
        
    def authenticate(self):
        """Authenticate with Google Calendar API"""
        try:
            creds = None
            token_path = 'token.json'
            
            # Check if we have valid credentials
            if os.path.exists(token_path):
                creds = Credentials.from_authorized_user_file(token_path, SCOPES)
            
            # If no valid credentials available, let the user log in
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.config.get_credentials_path(), SCOPES)
                    creds = flow.run_local_server(port=0)
                
                # Save the credentials for the next run
                with open(token_path, 'w') as token:
                    token.write(creds.to_json())
            
            self.credentials = creds
            self.service = build('calendar', 'v3', credentials=creds)
            
            # Get target calendar ID
            self.calendar_id = self.config.get('calendar.target_calendar_id', 'primary')
            
            logger.info("Successfully authenticated with Google Calendar API")
            
        except Exception as e:
            logger.error(f"Google Calendar authentication failed: {e}")
            raise
    
    def test_access(self):
        """Test calendar access and permissions"""
        try:
            if not self.service:
                raise RuntimeError("Calendar service not initialized. Call authenticate() first.")
            
            # Try to get calendar info
            calendar = self.service.calendars().get(calendarId=self.calendar_id).execute()
            
            logger.info(f"Successfully accessed calendar: {calendar.get('summary', 'Unknown')}")
            logger.info(f"Calendar ID: {self.calendar_id}")
            logger.info(f"Time zone: {calendar.get('timeZone', 'Unknown')}")
            
            return True
            
        except Exception as e:
            logger.error(f"Calendar access test failed: {e}")
            raise
    
    def create_event(self, appointment: Appointment) -> Dict[str, Any]:
        """Create a calendar event for an appointment"""
        try:
            if not self.service:
                raise RuntimeError("Calendar service not initialized. Call authenticate() first.")
            
            # Get business info
            business_info = self.config.get_business_info()
            business_name = business_info.get('name', 'Photography Business')
            business_address = business_info.get('address', '')
            
            # Format event details
            event = {
                'summary': f"{appointment.session_type} - {appointment.client_name}",
                'description': self._format_event_description(appointment),
                'start': {
                    'dateTime': appointment.start_time.isoformat(),
                    'timeZone': self.config.get('calendar.timezone', 'UTC')
                },
                'end': {
                    'dateTime': appointment.end_time.isoformat(),
                    'timeZone': self.config.get('calendar.timezone', 'UTC')
                },
                'location': business_address,
                'attendees': [
                    {'email': appointment.client_email, 'displayName': appointment.client_name}
                ],
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},  # 1 day before
                        {'method': 'popup', 'minutes': 30}        # 30 minutes before
                    ]
                },
                'colorId': self._get_color_id(appointment.session_type),
                'extendedProperties': {
                    'private': {
                        'appointment_id': appointment.id,
                        'session_type': appointment.session_type,
                        'client_name': appointment.client_name
                    }
                }
            }
            
            # Create the event
            created_event = self.service.events().insert(
                calendarId=self.calendar_id, body=event).execute()
            
            logger.info(f"Created calendar event: {created_event.get('id')}")
            return created_event
            
        except Exception as e:
            logger.error(f"Failed to create calendar event: {e}")
            raise
    
    def _format_event_description(self, appointment: Appointment) -> str:
        """Format event description with appointment details"""
        description = f"""
Session Type: {appointment.session_type}
Client: {appointment.client_name}
Duration: {appointment.duration} minutes

"""
        
        if appointment.notes:
            description += f"Notes: {appointment.notes}\n\n"
        
        description += f"Created by Gmail Photography Appointment Scheduler"
        return description.strip()
    
    def _get_color_id(self, session_type: str) -> str:
        """Get color ID based on session type"""
        # Map session types to Google Calendar colors
        color_map = {
            'portrait': '1',      # Lavender
            'family': '2',        # Sage
            'wedding': '3',       # Grape
            'engagement': '4',    # Flamingo
            'maternity': '5',     # Banana
            'newborn': '6',       # Tangerine
            'senior': '7',        # Peacock
            'headshot': '8',      # Graphite
            'event': '9',         # Blueberry
            'photoshoot': '10'    # Basil
        }
        
        return color_map.get(session_type.lower(), '1')  # Default to lavender
    
    def update_event(self, event_id: str, appointment: Appointment) -> Dict[str, Any]:
        """Update an existing calendar event"""
        try:
            if not self.service:
                raise RuntimeError("Calendar service not initialized. Call authenticate() first.")
            
            # Get existing event
            event = self.service.events().get(
                calendarId=self.calendar_id, eventId=event_id).execute()
            
            # Update event details
            event['summary'] = f"{appointment.session_type} - {appointment.client_name}"
            event['description'] = self._format_event_description(appointment)
            event['start']['dateTime'] = appointment.start_time.isoformat()
            event['end']['dateTime'] = appointment.end_time.isoformat()
            event['attendees'] = [
                {'email': appointment.client_email, 'displayName': appointment.client_name}
            ]
            
            # Update the event
            updated_event = self.service.events().update(
                calendarId=self.calendar_id, eventId=event_id, body=event).execute()
            
            logger.info(f"Updated calendar event: {event_id}")
            return updated_event
            
        except Exception as e:
            logger.error(f"Failed to update calendar event {event_id}: {e}")
            raise
    
    def cancel_event(self, event_id: str) -> bool:
        """Cancel/delete a calendar event"""
        try:
            if not self.service:
                raise RuntimeError("Calendar service not initialized. Call authenticate() first.")
            
            # Delete the event
            self.service.events().delete(
                calendarId=self.calendar_id, eventId=event_id).execute()
            
            logger.info(f"Cancelled calendar event: {event_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to cancel calendar event {event_id}: {e}")
            return False
    
    def get_event(self, event_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific calendar event"""
        try:
            if not self.service:
                raise RuntimeError("Calendar service not initialized. Call authenticate() first.")
            
            event = self.service.events().get(
                calendarId=self.calendar_id, eventId=event_id).execute()
            
            return event
            
        except Exception as e:
            logger.error(f"Failed to get calendar event {event_id}: {e}")
            return None
    
    def list_events(self, time_min: Optional[datetime] = None, 
                    time_max: Optional[datetime] = None, 
                    max_results: int = 100) -> List[Dict[str, Any]]:
        """List calendar events within a time range"""
        try:
            if not self.service:
                raise RuntimeError("Calendar service not initialized. Call authenticate() first.")
            
            # Set default time range if not provided
            if time_min is None:
                time_min = datetime.now()
            if time_max is None:
                time_max = time_min + timedelta(days=30)
            
            # Format time for API
            time_min_str = time_min.isoformat() + 'Z'
            time_max_str = time_max.isoformat() + 'Z'
            
            # Get events
            events_result = self.service.events().list(
                calendarId=self.calendar_id,
                timeMin=time_min_str,
                timeMax=time_max_str,
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            logger.info(f"Found {len(events)} calendar events")
            
            return events
            
        except Exception as e:
            logger.error(f"Failed to list calendar events: {e}")
            raise
    
    def find_appointment_events(self, days: int = 30) -> List[Dict[str, Any]]:
        """Find calendar events that are photography appointments"""
        try:
            events = self.list_events(max_results=1000)
            
            appointment_events = []
            for event in events:
                # Check if event has appointment properties
                extended_props = event.get('extendedProperties', {}).get('private', {})
                if extended_props.get('appointment_id'):
                    appointment_events.append(event)
                # Also check summary for photography keywords
                elif any(keyword in event.get('summary', '').lower() 
                        for keyword in ['portrait', 'session', 'photoshoot', 'wedding', 'family']):
                    appointment_events.append(event)
            
            logger.info(f"Found {len(appointment_events)} appointment events")
            return appointment_events
            
        except Exception as e:
            logger.error(f"Failed to find appointment events: {e}")
            raise
    
    def add_reminder(self, event_id: str, minutes_before: int, method: str = 'email') -> bool:
        """Add a custom reminder to an event"""
        try:
            if not self.service:
                raise RuntimeError("Calendar service not initialized. Call authenticate() first.")
            
            # Get existing event
            event = self.service.events().get(
                calendarId=self.calendar_id, eventId=event_id).execute()
            
            # Add new reminder
            if 'reminders' not in event:
                event['reminders'] = {'useDefault': False, 'overrides': []}
            
            new_reminder = {'method': method, 'minutes': minutes_before}
            event['reminders']['overrides'].append(new_reminder)
            
            # Update the event
            self.service.events().update(
                calendarId=self.calendar_id, eventId=event_id, body=event).execute()
            
            logger.info(f"Added {method} reminder {minutes_before} minutes before event {event_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add reminder to event {event_id}: {e}")
            return False
    
    def get_calendar_list(self) -> List[Dict[str, Any]]:
        """Get list of available calendars"""
        try:
            if not self.service:
                raise RuntimeError("Calendar service not initialized. Call authenticate() first.")
            
            calendar_list = self.service.calendarList().list().execute()
            calendars = calendar_list.get('items', [])
            
            logger.info(f"Found {len(calendars)} calendars")
            return calendars
            
        except Exception as e:
            logger.error(f"Failed to get calendar list: {e}")
            raise
    
    def check_availability(self, start_time: datetime, end_time: datetime) -> bool:
        """Check if a time slot is available (no conflicting events)"""
        try:
            if not self.service:
                raise RuntimeError("Calendar service not initialized. Call authenticate() first.")
            
            # Format time for API
            time_min = start_time.isoformat() + 'Z'
            time_max = end_time.isoformat() + 'Z'
            
            # Check for conflicting events
            events_result = self.service.events().list(
                calendarId=self.calendar_id,
                timeMin=time_min,
                timeMax=time_max,
                singleEvents=True
            ).execute()
            
            conflicting_events = events_result.get('items', [])
            
            # Filter out events that are not confirmed appointments
            confirmed_conflicts = [
                event for event in conflicting_events
                if event.get('status') != 'cancelled'
            ]
            
            is_available = len(confirmed_conflicts) == 0
            
            if not is_available:
                logger.info(f"Time slot {start_time} - {end_time} has {len(confirmed_conflicts)} conflicts")
            
            return is_available
            
        except Exception as e:
            logger.error(f"Failed to check availability: {e}")
            raise
    
    def get_business_hours(self) -> Dict[str, Any]:
        """Get business hours configuration"""
        return self.config.get('calendar.business_hours', {})
    
    def is_business_hour(self, check_time: datetime) -> bool:
        """Check if a time is within business hours"""
        business_hours = self.get_business_hours()
        
        if not business_hours:
            return True  # No restrictions if not configured
        
        # Get day of week
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_name = day_names[check_time.weekday()]
        
        # Check if day is a business day
        if day_name not in business_hours.get('days', []):
            return False
        
        # Check if time is within business hours
        start_time_str = business_hours.get('start', '09:00')
        end_time_str = business_hours.get('end', '17:00')
        
        try:
            start_hour, start_minute = map(int, start_time_str.split(':'))
            end_hour, end_minute = map(int, end_time_str.split(':'))
            
            check_time_only = check_time.time()
            start_time_only = check_time.replace(hour=start_hour, minute=start_minute).time()
            end_time_only = check_time.replace(hour=end_hour, minute=end_minute).time()
            
            return start_time_only <= check_time_only <= end_time_only
            
        except (ValueError, AttributeError):
            logger.warning("Invalid business hours format in configuration")
            return True
