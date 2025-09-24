"""
Data models for appointments, clients, and CRM functionality
Specialized for maternity, baby, smash cake, and birthday photography
"""

from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
import uuid


@dataclass
class BabyMilestone:
    """Track baby development milestones for photography planning"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    client_id: str = ""
    baby_name: str = ""
    birth_date: Optional[datetime] = None
    milestone_type: str = ""  # newborn, 3month, 6month, 9month, 1year, etc.
    milestone_date: Optional[datetime] = None
    age_in_days: int = 0
    age_in_weeks: int = 0
    age_in_months: int = 0
    notes: str = ""
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    
    def calculate_age(self):
        """Calculate baby's current age"""
        if not self.birth_date:
            return
        
        now = datetime.now()
        delta = now - self.birth_date
        
        self.age_in_days = delta.days
        self.age_in_weeks = delta.days // 7
        self.age_in_months = (delta.days // 30)
    
    def get_next_milestone(self) -> str:
        """Get the next recommended milestone"""
        if self.age_in_days < 14:
            return "newborn"
        elif self.age_in_days < 90:
            return "3month"
        elif self.age_in_days < 180:
            return "6month"
        elif self.age_in_days < 270:
            return "9month"
        elif self.age_in_days < 365:
            return "1year"
        elif self.age_in_days < 730:
            return "18month"
        else:
            return "2year"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert milestone to dictionary"""
        return {
            'id': self.id,
            'client_id': self.client_id,
            'baby_name': self.baby_name,
            'birth_date': self.birth_date.isoformat() if self.birth_date else None,
            'milestone_type': self.milestone_type,
            'milestone_date': self.milestone_date.isoformat() if self.milestone_date else None,
            'age_in_days': self.age_in_days,
            'age_in_weeks': self.age_in_weeks,
            'age_in_months': self.age_in_months,
            'notes': self.notes,
            'completed': self.completed,
            'created_at': self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BabyMilestone':
        """Create milestone from dictionary"""
        return cls(
            id=data.get('id', str(uuid.uuid4())),
            client_id=data.get('client_id', ''),
            baby_name=data.get('baby_name', ''),
            birth_date=datetime.fromisoformat(data.get('birth_date')) if data.get('birth_date') else None,
            milestone_type=data.get('milestone_type', ''),
            milestone_date=datetime.fromisoformat(data.get('milestone_date')) if data.get('milestone_date') else None,
            age_in_days=data.get('age_in_days', 0),
            age_in_weeks=data.get('age_in_weeks', 0),
            age_in_months=data.get('age_in_months', 0),
            notes=data.get('notes', ''),
            completed=data.get('completed', False),
            created_at=datetime.fromisoformat(data.get('created_at', datetime.now().isoformat()))
        )


@dataclass
class BirthdaySession:
    """Specialized birthday photography session details"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    appointment_id: str = ""
    child_name: str = ""
    age_turning: int = 0
    birthday_date: Optional[datetime] = None
    session_date: Optional[datetime] = None
    theme: str = ""  # princess, superhero, farm, etc.
    colors: List[str] = field(default_factory=list)
    props_needed: List[str] = field(default_factory=list)
    cake_flavor: str = ""
    cake_design: str = ""
    special_requests: str = ""
    parent_vision: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert birthday session to dictionary"""
        return {
            'id': self.id,
            'appointment_id': self.appointment_id,
            'child_name': self.child_name,
            'age_turning': self.age_turning,
            'birthday_date': self.birthday_date.isoformat() if self.birthday_date else None,
            'session_date': self.session_date.isoformat() if self.session_date else None,
            'theme': self.theme,
            'colors': self.colors,
            'props_needed': self.props_needed,
            'cake_flavor': self.cake_flavor,
            'cake_design': self.cake_design,
            'special_requests': self.special_requests,
            'parent_vision': self.parent_vision,
            'created_at': self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BirthdaySession':
        """Create birthday session from dictionary"""
        return cls(
            id=data.get('id', str(uuid.uuid4())),
            appointment_id=data.get('appointment_id', ''),
            child_name=data.get('child_name', ''),
            age_turning=data.get('age_turning', 0),
            birthday_date=datetime.fromisoformat(data.get('birthday_date')) if data.get('birthday_date') else None,
            session_date=datetime.fromisoformat(data.get('session_date')) if data.get('session_date') else None,
            theme=data.get('theme', ''),
            colors=data.get('colors', []),
            props_needed=data.get('props_needed', []),
            cake_flavor=data.get('cake_flavor', ''),
            cake_design=data.get('cake_design', ''),
            special_requests=data.get('special_requests', ''),
            parent_vision=data.get('parent_vision', ''),
            created_at=datetime.fromisoformat(data.get('created_at', datetime.now().isoformat()))
        )


@dataclass
class Client:
    """Client information with comprehensive CRM data for baby photography"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    email: str = ""
    phone: str = ""
    address: str = ""
    city: str = ""
    state: str = ""
    zip_code: str = ""
    country: str = "USA"
    
    # CRM Fields
    company: str = ""
    website: str = ""
    social_media: Dict[str, str] = field(default_factory=dict)  # Instagram, Facebook, etc.
    referral_source: str = ""  # How they found you
    marketing_consent: bool = False
    tags: List[str] = field(default_factory=list)  # VIP, New Client, etc.
    
    # Baby Photography Specific Fields
    family_type: str = ""  # expecting, newborn, baby, toddler, multiple_children
    due_date: Optional[datetime] = None
    children_count: int = 0
    children_names: str = ""
    children_birth_dates: str = ""
    children_info: List[Dict[str, Any]] = field(default_factory=list)  # List of children details
    family_size: int = 1
    previous_photographer: str = ""
    photography_experience: str = ""  # first_time, experienced, professional
    
    # Business Information
    industry: str = ""
    budget_range: str = ""  # $500-1000, $1000-2000, etc.
    project_type: str = ""  # Personal, Business, Event, etc.
    
    # Notes and History
    notes: str = ""
    internal_notes: str = ""  # Staff-only notes
    preferences: Dict[str, Any] = field(default_factory=dict)  # Style preferences, etc.
    
    # Timestamps
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    last_contact: Optional[datetime] = None
    last_appointment: Optional[datetime] = None
    
    # CRM Metrics
    total_appointments: int = 0
    total_spent: float = 0.0
    average_session_value: float = 0.0
    customer_lifetime_value: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert client to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'country': self.country,
            'company': self.company,
            'website': self.website,
            'social_media': self.social_media,
            'referral_source': self.referral_source,
            'marketing_consent': self.marketing_consent,
            'tags': self.tags,
            'family_type': self.family_type,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'children_info': self.children_info,
            'family_size': self.family_size,
            'previous_photographer': self.previous_photographer,
            'photography_experience': self.photography_experience,
            'industry': self.industry,
            'budget_range': self.budget_range,
            'project_type': self.project_type,
            'notes': self.notes,
            'internal_notes': self.internal_notes,
            'preferences': self.preferences,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'last_contact': self.last_contact.isoformat() if self.last_contact else None,
            'last_appointment': self.last_appointment.isoformat() if self.last_appointment else None,
            'total_appointments': self.total_appointments,
            'total_spent': self.total_spent,
            'average_session_value': self.average_session_value,
            'customer_lifetime_value': self.customer_lifetime_value
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
            city=data.get('city', ''),
            state=data.get('state', ''),
            zip_code=data.get('zip_code', ''),
            country=data.get('country', 'USA'),
            company=data.get('company', ''),
            website=data.get('website', ''),
            social_media=data.get('social_media', {}),
            referral_source=data.get('referral_source', ''),
            marketing_consent=data.get('marketing_consent', False),
            tags=data.get('tags', []),
            family_type=data.get('family_type', ''),
            due_date=datetime.fromisoformat(data.get('due_date')) if data.get('due_date') else None,
            children_info=data.get('children_info', []),
            family_size=data.get('family_size', 1),
            previous_photographer=data.get('previous_photographer', ''),
            photography_experience=data.get('photography_experience', ''),
            industry=data.get('industry', ''),
            budget_range=data.get('budget_range', ''),
            project_type=data.get('project_type', ''),
            notes=data.get('notes', ''),
            internal_notes=data.get('internal_notes', ''),
            preferences=data.get('preferences', {}),
            created_at=datetime.fromisoformat(data.get('created_at', datetime.now().isoformat())),
            updated_at=datetime.fromisoformat(data.get('updated_at', datetime.now().isoformat())),
            last_contact=datetime.fromisoformat(data.get('last_contact')) if data.get('last_contact') else None,
            last_appointment=datetime.fromisoformat(data.get('last_appointment')) if data.get('last_appointment') else None,
            total_appointments=data.get('total_appointments', 0),
            total_spent=data.get('total_spent', 0.0),
            average_session_value=data.get('average_session_value', 0.0),
            customer_lifetime_value=data.get('customer_lifetime_value', 0.0)
        )
    
    def update_metrics(self, appointment_value: float = 0.0):
        """Update CRM metrics after appointment"""
        self.total_appointments += 1
        self.total_spent += appointment_value
        self.average_session_value = self.total_spent / self.total_appointments
        self.customer_lifetime_value = self.total_spent
        self.last_appointment = datetime.now()
        self.updated_at = datetime.now()
    
    def add_note(self, note: str, internal: bool = False):
        """Add a note to the client record"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        formatted_note = f"[{timestamp}] {note}\n"
        
        if internal:
            self.internal_notes += formatted_note
        else:
            self.notes += formatted_note
        
        self.updated_at = datetime.now()
    
    def add_tag(self, tag: str):
        """Add a tag to the client"""
        if tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.now()
    
    def remove_tag(self, tag: str):
        """Remove a tag from the client"""
        if tag in self.tags:
            self.tags.remove(tag)
            self.updated_at = datetime.now()
    
    def add_child(self, child_info: Dict[str, Any]):
        """Add child information to the client"""
        self.children_info.append(child_info)
        self.family_size = len(self.children_info)
        self.updated_at = datetime.now()
    
    def get_children_names(self) -> List[str]:
        """Get list of children names"""
        return [child.get('name', '') for child in self.children_info if child.get('name')]
    
    def is_expecting(self) -> bool:
        """Check if client is expecting"""
        return self.family_type == "expecting" and self.due_date is not None
    
    def get_days_until_due(self) -> Optional[int]:
        """Get days until due date"""
        if not self.due_date:
            return None
        delta = self.due_date.date() - datetime.now().date()
        return delta.days


@dataclass
class Appointment:
    """Appointment information with enhanced CRM tracking for baby photography"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    client_id: str = ""  # Reference to Client
    client_name: str = ""
    client_email: str = ""
    start_time: datetime = field(default_factory=datetime.now)
    end_time: datetime = field(default_factory=datetime.now)
    duration: int = 60  # minutes
    session_type: str = ""
    
    # Baby Photography Specific Fields
    baby_age_days: Optional[int] = None
    baby_age_weeks: Optional[int] = None
    baby_age_months: Optional[int] = None
    milestone_type: str = ""  # newborn, 3month, 6month, 9month, 1year, etc.
    baby_name: str = ""
    parent_names: List[str] = field(default_factory=list)
    siblings_included: bool = False
    sibling_names: List[str] = field(default_factory=list)
    
    # CRM and Business Fields
    status: str = "confirmed"  # confirmed, cancelled, completed, rescheduled
    priority: str = "normal"  # low, normal, high, urgent
    location: str = ""
    equipment_needed: List[str] = field(default_factory=list)
    
    # Financial Information
    session_fee: float = 0.0
    additional_charges: float = 0.0
    discount: float = 0.0
    total_amount: float = 0.0
    payment_status: str = "pending"  # pending, partial, paid, overdue
    
    # Notes and Communication
    notes: str = ""
    internal_notes: str = ""
    client_requests: str = ""
    special_instructions: str = ""
    
    # CRM Tracking
    referral_source: str = ""
    marketing_campaign: str = ""
    follow_up_required: bool = False
    follow_up_notes: str = ""
    
    # Technical Details
    calendar_event_id: Optional[str] = None
    gmail_message_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Calculate end_time and total_amount if not provided"""
        if self.end_time == self.created_at:
            self.end_time = self.start_time + timedelta(minutes=self.duration)
        
        if self.total_amount == 0.0:
            self.total_amount = self.session_fee + self.additional_charges - self.discount
    
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
    
    @property
    def is_paid(self) -> bool:
        """Check if appointment is fully paid"""
        return self.payment_status == "paid"
    
    @property
    def outstanding_amount(self) -> float:
        """Calculate outstanding payment amount"""
        if self.payment_status == "paid":
            return 0.0
        return self.total_amount
    
    @property
    def is_newborn_session(self) -> bool:
        """Check if this is a newborn session"""
        return self.milestone_type == "newborn" or (self.baby_age_days and self.baby_age_days <= 14)
    
    @property
    def is_milestone_session(self) -> bool:
        """Check if this is a milestone session"""
        return self.milestone_type in ["3month", "6month", "9month", "1year", "18month", "2year"]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert appointment to dictionary"""
        return {
            'id': self.id,
            'client_id': self.client_id,
            'client_name': self.client_name,
            'client_email': self.client_email,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat(),
            'duration': self.duration,
            'session_type': self.session_type,
            'baby_age_days': self.baby_age_days,
            'baby_age_weeks': self.baby_age_weeks,
            'baby_age_months': self.baby_age_months,
            'milestone_type': self.milestone_type,
            'is_milestone_session': self.is_milestone_session,
            'baby_name': self.baby_name,
            'parent_names': self.parent_names,
            'siblings_included': self.siblings_included,
            'sibling_names': self.sibling_names,
            'status': self.status,
            'priority': self.priority,
            'location': self.location,
            'equipment_needed': self.equipment_needed,
            'session_fee': self.session_fee,
            'additional_charges': self.additional_charges,
            'discount': self.discount,
            'total_amount': self.total_amount,
            'payment_status': self.payment_status,
            'notes': self.notes,
            'internal_notes': self.internal_notes,
            'client_requests': self.client_requests,
            'special_instructions': self.special_instructions,
            'referral_source': self.referral_source,
            'marketing_campaign': self.marketing_campaign,
            'follow_up_required': self.follow_up_required,
            'follow_up_notes': self.follow_up_notes,
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
            client_id=data.get('client_id', ''),
            client_name=data.get('client_name', ''),
            client_email=data.get('client_email', ''),
            start_time=datetime.fromisoformat(data.get('start_time', datetime.now().isoformat())),
            end_time=datetime.fromisoformat(data.get('end_time', datetime.now().isoformat())),
            duration=data.get('duration', 60),
            session_type=data.get('session_type', ''),
            baby_age_days=data.get('baby_age_days'),
            baby_age_weeks=data.get('baby_age_weeks'),
            baby_age_months=data.get('baby_age_months'),
            milestone_type=data.get('milestone_type', ''),
            is_milestone_session=data.get('is_milestone_session', False),
            baby_name=data.get('baby_name', ''),
            parent_names=data.get('parent_names', []),
            siblings_included=data.get('siblings_included', False),
            sibling_names=data.get('sibling_names', []),
            status=data.get('status', 'confirmed'),
            priority=data.get('priority', 'normal'),
            location=data.get('location', ''),
            equipment_needed=data.get('equipment_needed', []),
            session_fee=data.get('session_fee', 0.0),
            additional_charges=data.get('additional_charges', 0.0),
            discount=data.get('discount', 0.0),
            total_amount=data.get('total_amount', 0.0),
            payment_status=data.get('payment_status', 'pending'),
            notes=data.get('notes', ''),
            internal_notes=data.get('internal_notes', ''),
            client_requests=data.get('client_requests', ''),
            special_instructions=data.get('special_instructions', ''),
            referral_source=data.get('referral_source', ''),
            marketing_campaign=data.get('marketing_campaign', ''),
            follow_up_required=data.get('follow_up_required', False),
            follow_up_notes=data.get('follow_up_notes', ''),
            calendar_event_id=data.get('calendar_event_id'),
            gmail_message_id=data.get('gmail_message_id'),
            created_at=datetime.fromisoformat(data.get('created_at', datetime.now().isoformat())),
            updated_at=datetime.fromisoformat(data.get('updated_at', datetime.now().isoformat()))
        )
    
    def add_note(self, note: str, internal: bool = False):
        """Add a note to the appointment"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        formatted_note = f"[{timestamp}] {note}\n"
        
        if internal:
            self.internal_notes += formatted_note
        else:
            self.notes += formatted_note
        
        self.updated_at = datetime.now()
    
    def update_payment_status(self, amount_paid: float):
        """Update payment status based on amount paid"""
        if amount_paid >= self.total_amount:
            self.payment_status = "paid"
        elif amount_paid > 0:
            self.payment_status = "partial"
        else:
            self.payment_status = "pending"
    
    def calculate_baby_age(self, birth_date: datetime):
        """Calculate baby's age for the appointment"""
        if not birth_date:
            return
        
        delta = self.start_time - birth_date
        self.baby_age_days = delta.days
        self.baby_age_weeks = delta.days // 7
        self.baby_age_months = (delta.days // 30)


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


@dataclass
class ClientNote:
    """Individual client notes for better organization"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    client_id: str = ""
    note_type: str = "general"  # general, follow_up, marketing, internal, etc.
    title: str = ""
    content: str = ""
    author: str = ""  # Staff member who created the note
    is_internal: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert client note to dictionary"""
        return {
            'id': self.id,
            'client_id': self.client_id,
            'note_type': self.note_type,
            'title': self.title,
            'content': self.content,
            'author': self.author,
            'is_internal': self.is_internal,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ClientNote':
        """Create client note from dictionary"""
        return cls(
            id=data.get('id', str(uuid.uuid4())),
            note_type=data.get('note_type', 'general'),
            title=data.get('title', ''),
            content=data.get('content', ''),
            author=data.get('author', ''),
            is_internal=data.get('is_internal', False),
            created_at=datetime.fromisoformat(data.get('created_at', datetime.now().isoformat())),
            updated_at=datetime.fromisoformat(data.get('updated_at', datetime.now().isoformat()))
        )


@dataclass
class MarketingCampaign:
    """Marketing campaign tracking"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    campaign_type: str = ""  # email, social_media, referral, etc.
    start_date: datetime = field(default_factory=datetime.now)
    end_date: Optional[datetime] = None
    budget: float = 0.0
    status: str = "active"  # active, paused, completed, cancelled
    target_audience: List[str] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)  # clicks, conversions, etc.
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert marketing campaign to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'campaign_type': self.campaign_type,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'budget': self.budget,
            'status': self.status,
            'target_audience': self.target_audience,
            'metrics': self.metrics,
            'created_at': self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MarketingCampaign':
        """Create marketing campaign from dictionary"""
        return cls(
            id=data.get('id', str(uuid.uuid4())),
            name=data.get('name', ''),
            description=data.get('description', ''),
            campaign_type=data.get('campaign_type', ''),
            start_date=datetime.fromisoformat(data.get('start_date', datetime.now().isoformat())),
            end_date=datetime.fromisoformat(data.get('end_date')) if data.get('end_date') else None,
            budget=data.get('budget', 0.0),
            status=data.get('status', 'active'),
            target_audience=data.get('target_audience', []),
            metrics=data.get('metrics', {}),
            created_at=datetime.fromisoformat(data.get('created_at', datetime.now().isoformat()))
        )
