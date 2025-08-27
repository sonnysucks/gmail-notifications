"""
Data models for appointments and clients
"""

from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
import uuid


@dataclass
class Client:
    """Client information"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    email: str = ""
    phone: str = ""
    address: str = ""
    notes: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert client to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Client':
        """Create client from dictionary"""
        return cls(
            id=data.get('id', str(uuid.uuid4())),
            name=data.get('name', ''),
            email=data.get('email', ''),
            phone=data.get('phone', ''),
            address=data.get('address', ''),
            notes=data.get('notes', ''),
            created_at=datetime.fromisoformat(data.get('created_at', datetime.now().isoformat())),
            updated_at=datetime.fromisoformat(data.get('updated_at', datetime.now().isoformat()))
        )


@dataclass
class Appointment:
    """Appointment information"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str = ""
    client_email: str = ""
    start_time: datetime = field(default_factory=datetime.now)
    end_time: datetime = field(default_factory=datetime.now)
    duration: int = 60  # minutes
    session_type: str = ""
    notes: str = ""
    status: str = "confirmed"  # confirmed, cancelled, completed
    calendar_event_id: Optional[str] = None
    gmail_message_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Calculate end_time if not provided"""
        if self.end_time == self.created_at:
            self.end_time = self.start_time + timedelta(minutes=self.duration)
    
    @property
    def is_upcoming(self) -> bool:
        """Check if appointment is in the future"""
        return self.start_time > datetime.now()
    
    @property
    def is_today(self) -> bool:
        """Check if appointment is today"""
        today = datetime.now().date()
        return self.start_time.date() == today
    
    @property
    def days_until(self) -> int:
        """Days until appointment"""
        delta = self.start_time.date() - datetime.now().date()
        return delta.days
    
    @property
    def reminder_key(self) -> str:
        """Get reminder key for this appointment"""
        if self.days_until >= 14:
            return "reminder_2weeks"
        elif self.days_until >= 7:
            return "reminder_1week"
        elif self.days_until >= 3:
            return "reminder_3days"
        elif self.days_until >= 2:
            return "reminder_2days"
        elif self.days_until >= 1:
            return "reminder_1day"
        else:
            return "reminder_same_day"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert appointment to dictionary"""
        return {
            'id': self.id,
            'client_name': self.client_name,
            'client_email': self.client_email,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat(),
            'duration': self.duration,
            'session_type': self.session_type,
            'notes': self.notes,
            'status': self.status,
            'calendar_event_id': self.calendar_event_id,
            'gmail_message_id': self.gmail_message_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Appointment':
        """Create appointment from dictionary"""
        return cls(
            id=data.get('id', str(uuid.uuid4())),
            client_name=data.get('client_name', ''),
            client_email=data.get('client_email', ''),
            start_time=datetime.fromisoformat(data.get('start_time', datetime.now().isoformat())),
            end_time=datetime.fromisoformat(data.get('end_time', datetime.now().isoformat())),
            duration=data.get('duration', 60),
            session_type=data.get('session_type', ''),
            notes=data.get('notes', ''),
            status=data.get('status', 'confirmed'),
            calendar_event_id=data.get('calendar_event_id'),
            gmail_message_id=data.get('gmail_message_id'),
            created_at=datetime.fromisoformat(data.get('created_at', datetime.now().isoformat())),
            updated_at=datetime.fromisoformat(data.get('updated_at', datetime.now().isoformat()))
        )


@dataclass
class Reminder:
    """Reminder information"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    appointment_id: str = ""
    reminder_type: str = ""  # 2weeks, 1week, 3days, 2days, 1day
    scheduled_time: datetime = field(default_factory=datetime.now)
    sent_time: Optional[datetime] = None
    status: str = "pending"  # pending, sent, failed
    email_message_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert reminder to dictionary"""
        return {
            'id': self.id,
            'appointment_id': self.appointment_id,
            'reminder_type': self.reminder_type,
            'scheduled_time': self.scheduled_time.isoformat(),
            'sent_time': self.sent_time.isoformat() if self.sent_time else None,
            'status': self.status,
            'email_message_id': self.email_message_id,
            'created_at': self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Reminder':
        """Create reminder from dictionary"""
        return cls(
            id=data.get('id', str(uuid.uuid4())),
            appointment_id=data.get('appointment_id', ''),
            reminder_type=data.get('reminder_type', ''),
            scheduled_time=datetime.fromisoformat(data.get('scheduled_time', datetime.now().isoformat())),
            sent_time=datetime.fromisoformat(data.get('sent_time')) if data.get('sent_time') else None,
            status=data.get('status', 'pending'),
            email_message_id=data.get('email_message_id'),
            created_at=datetime.fromisoformat(data.get('created_at', datetime.now().isoformat()))
        )
