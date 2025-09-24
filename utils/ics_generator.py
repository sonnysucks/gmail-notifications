#!/usr/bin/env python3
"""
ICS (iCalendar) File Generator for Photography Appointments
Generates calendar-compatible files for appointment import
"""

import os
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class ICSAppointment:
    """Represents an appointment for ICS export"""
    uid: str
    summary: str
    description: str
    start_time: datetime
    end_time: datetime
    location: str
    status: str
    reminder_minutes: List[int] = None
    client_name: str = ""
    client_email: str = ""
    session_type: str = ""
    notes: str = ""
    
    def __post_init__(self):
        if self.reminder_minutes is None:
            self.reminder_minutes = [60, 1440]  # 1 hour and 1 day before

class ICSGenerator:
    """Generates ICS (iCalendar) files for appointments"""
    
    def __init__(self, business_name: str = "Photography Business"):
        self.business_name = business_name
        self.timezone = "America/New_York"  # Default timezone
    
    def generate_ics_content(self, appointments: List[ICSAppointment]) -> str:
        """Generate ICS file content for multiple appointments"""
        
        ics_content = [
            "BEGIN:VCALENDAR",
            "VERSION:2.0",
            "PRODID:-//Photography Scheduler//Photography Business//EN",
            "CALSCALE:GREGORIAN",
            "METHOD:PUBLISH",
            f"X-WR-CALNAME:{self.business_name}",
            f"X-WR-TIMEZONE:{self.timezone}",
            ""
        ]
        
        for appointment in appointments:
            ics_content.extend(self._generate_event_content(appointment))
            ics_content.append("")  # Empty line between events
        
        ics_content.append("END:VCALENDAR")
        
        return "\r\n".join(ics_content)
    
    def _generate_event_content(self, appointment: ICSAppointment) -> List[str]:
        """Generate ICS content for a single appointment"""
        
        # Format datetime for ICS (YYYYMMDDTHHMMSSZ)
        start_utc = appointment.start_time.strftime("%Y%m%dT%H%M%SZ")
        end_utc = appointment.end_time.strftime("%Y%m%dT%H%M%SZ")
        created_utc = datetime.now().strftime("%Y%m%dT%H%M%SZ")
        
        # Escape special characters in description
        description = self._escape_ics_text(appointment.description)
        summary = self._escape_ics_text(appointment.summary)
        location = self._escape_ics_text(appointment.location)
        
        event_content = [
            "BEGIN:VEVENT",
            f"UID:{appointment.uid}",
            f"DTSTART:{start_utc}",
            f"DTEND:{end_utc}",
            f"DTSTAMP:{created_utc}",
            f"SUMMARY:{summary}",
            f"DESCRIPTION:{description}",
            f"LOCATION:{location}",
            f"STATUS:{appointment.status.upper()}",
            f"ORGANIZER:CN={self.business_name}:mailto:info@{self.business_name.lower().replace(' ', '')}.com",
            f"ATTENDEE:CN={appointment.client_name}:mailto:{appointment.client_email}",
            "TRANSP:OPAQUE",
            "SEQUENCE:0",
            ""
        ]
        
        # Add custom properties
        if appointment.client_name:
            event_content.append(f"X-CLIENT-NAME:{self._escape_ics_text(appointment.client_name)}")
        if appointment.session_type:
            event_content.append(f"X-SESSION-TYPE:{self._escape_ics_text(appointment.session_type)}")
        if appointment.notes:
            event_content.append(f"X-NOTES:{self._escape_ics_text(appointment.notes)}")
        
        # Add reminders/alarms
        for reminder_minutes in appointment.reminder_minutes:
            event_content.extend(self._generate_alarm_content(reminder_minutes))
        
        event_content.append("END:VEVENT")
        
        return event_content
    
    def _generate_alarm_content(self, minutes_before: int) -> List[str]:
        """Generate alarm/reminder content"""
        return [
            "BEGIN:VALARM",
            "ACTION:DISPLAY",
            f"TRIGGER:-PT{minutes_before}M",
            "DESCRIPTION:Photography Session Reminder",
            "END:VALARM"
        ]
    
    def _escape_ics_text(self, text: str) -> str:
        """Escape special characters for ICS format"""
        if not text:
            return ""
        
        # Replace special characters
        text = text.replace("\\", "\\\\")
        text = text.replace(",", "\\,")
        text = text.replace(";", "\\;")
        text = text.replace("\n", "\\n")
        text = text.replace("\r", "")
        
        # Limit line length (ICS spec recommends 75 characters)
        if len(text) > 75:
            # Split long lines
            lines = []
            while len(text) > 75:
                lines.append(text[:75])
                text = " " + text[75:]  # Indent continuation lines
            lines.append(text)
            text = "\r\n".join(lines)
        
        return text
    
    def save_ics_file(self, appointments: List[ICSAppointment], filename: str) -> str:
        """Save appointments to an ICS file"""
        
        ics_content = self.generate_ics_content(appointments)
        
        # Ensure exports directory exists
        exports_dir = "exports"
        os.makedirs(exports_dir, exist_ok=True)
        
        filepath = os.path.join(exports_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(ics_content)
        
        return filepath
    
    def create_appointment_ics(self, appointment_data: Dict[str, Any]) -> ICSAppointment:
        """Create ICSAppointment from appointment data"""
        
        # Parse start time
        if isinstance(appointment_data.get('start_time'), str):
            start_time = datetime.fromisoformat(appointment_data['start_time'].replace('Z', '+00:00'))
        else:
            start_time = appointment_data['start_time']
        
        # Calculate end time
        duration = appointment_data.get('duration', 60)
        end_time = start_time + timedelta(minutes=duration)
        
        # Create summary
        client_name = appointment_data.get('client_name', 'Unknown Client')
        session_type = appointment_data.get('session_type', 'Photography Session')
        summary = f"{client_name} - {session_type}"
        
        # Create description
        description_parts = [
            f"Client: {client_name}",
            f"Session Type: {session_type}",
            f"Duration: {duration} minutes"
        ]
        
        if appointment_data.get('client_email'):
            description_parts.append(f"Email: {appointment_data['client_email']}")
        
        if appointment_data.get('notes'):
            description_parts.append(f"Notes: {appointment_data['notes']}")
        
        if appointment_data.get('special_instructions'):
            description_parts.append(f"Special Instructions: {appointment_data['special_instructions']}")
        
        description = "\\n".join(description_parts)
        
        # Create ICS appointment
        return ICSAppointment(
            uid=str(uuid.uuid4()),
            summary=summary,
            description=description,
            start_time=start_time,
            end_time=end_time,
            location=appointment_data.get('location', 'Studio'),
            status=appointment_data.get('status', 'confirmed'),
            client_name=client_name,
            client_email=appointment_data.get('client_email', ''),
            session_type=session_type,
            notes=appointment_data.get('notes', ''),
            reminder_minutes=[60, 1440, 10080]  # 1 hour, 1 day, 1 week before
        )

def test_ics_generation():
    """Test the ICS generation functionality"""
    
    print("🧪 Testing ICS file generation...")
    
    # Create test appointment data
    test_appointment_data = {
        'client_name': 'Sarah Johnson',
        'client_email': 'sarah@example.com',
        'session_type': 'Newborn Session',
        'start_time': '2025-09-15T10:00:00',
        'duration': 120,
        'location': 'Studio',
        'status': 'confirmed',
        'notes': 'First-time parents, very excited!',
        'special_instructions': 'Bring extra blankets and pacifiers'
    }
    
    # Create ICS generator
    generator = ICSGenerator("Photography Studio")
    
    # Create ICS appointment
    ics_appointment = generator.create_appointment_ics(test_appointment_data)
    
    # Generate ICS content
    ics_content = generator.generate_ics_content([ics_appointment])
    
    # Save to file
    filename = f"test_appointment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.ics"
    filepath = generator.save_ics_file([ics_appointment], filename)
    
    print(f"✅ ICS file generated: {filepath}")
    print(f"📄 File size: {os.path.getsize(filepath)} bytes")
    
    # Display first few lines of the ICS content
    print("\n📋 ICS Content Preview:")
    print("-" * 40)
    lines = ics_content.split('\r\n')[:20]  # First 20 lines
    for line in lines:
        print(line)
    if len(ics_content.split('\r\n')) > 20:
        print("... (truncated)")
    
    print(f"\n🎉 ICS generation test successful!")
    print(f"📁 File saved to: {filepath}")
    print(f"📅 You can import this file into any calendar application (Google Calendar, Outlook, Apple Calendar, etc.)")
    
    return True

if __name__ == "__main__":
    test_ics_generation()
