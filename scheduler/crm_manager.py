"""
Customer Relationship Management (CRM) system for photography business
"""

import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import sqlite3
from collections import defaultdict

from .models import Client, Appointment, ClientNote, MarketingCampaign
from ..config.config_manager import ConfigManager

logger = logging.getLogger(__name__)


class CRMManager:
    """Manages customer relationships and CRM operations"""
    
    def __init__(self, config_manager: ConfigManager):
        """Initialize CRM manager"""
        self.config = config_manager
        self.db_path = Path('data/crm.db')
        self.db_path.parent.mkdir(exist_ok=True)
        self._init_database()
    
    def _init_database(self):
        """Initialize SQLite database with CRM tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Clients table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS clients (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE,
                    phone TEXT,
                    address TEXT,
                    city TEXT,
                    state TEXT,
                    zip_code TEXT,
                    country TEXT,
                    company TEXT,
                    website TEXT,
                    social_media TEXT,
                    referral_source TEXT,
                    marketing_consent BOOLEAN,
                    tags TEXT,
                    industry TEXT,
                    budget_range TEXT,
                    project_type TEXT,
                    notes TEXT,
                    internal_notes TEXT,
                    preferences TEXT,
                    created_at TEXT,
                    updated_at TEXT,
                    last_contact TEXT,
                    last_appointment TEXT,
                    total_appointments INTEGER,
                    total_spent REAL,
                    average_session_value REAL,
                    customer_lifetime_value REAL
                )
            ''')
            
            # Appointments table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS appointments (
                    id TEXT PRIMARY KEY,
                    client_id TEXT,
                    client_name TEXT NOT NULL,
                    client_email TEXT,
                    start_time TEXT,
                    end_time TEXT,
                    duration INTEGER,
                    session_type TEXT,
                    status TEXT,
                    priority TEXT,
                    location TEXT,
                    equipment_needed TEXT,
                    session_fee REAL,
                    additional_charges REAL,
                    discount REAL,
                    total_amount REAL,
                    payment_status TEXT,
                    notes TEXT,
                    internal_notes TEXT,
                    client_requests TEXT,
                    special_instructions TEXT,
                    referral_source TEXT,
                    marketing_campaign TEXT,
                    follow_up_required BOOLEAN,
                    follow_up_notes TEXT,
                    calendar_event_id TEXT,
                    gmail_message_id TEXT,
                    created_at TEXT,
                    updated_at TEXT,
                    FOREIGN KEY (client_id) REFERENCES clients (id)
                )
            ''')
            
            # Client notes table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS client_notes (
                    id TEXT PRIMARY KEY,
                    client_id TEXT,
                    note_type TEXT,
                    title TEXT,
                    content TEXT,
                    author TEXT,
                    is_internal BOOLEAN,
                    created_at TEXT,
                    updated_at TEXT,
                    FOREIGN KEY (client_id) REFERENCES clients (id)
                )
            ''')
            
            # Marketing campaigns table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS marketing_campaigns (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    campaign_type TEXT,
                    start_date TEXT,
                    end_date TEXT,
                    budget REAL,
                    status TEXT,
                    target_audience TEXT,
                    metrics TEXT,
                    created_at TEXT
                )
            ''')
            
            # Create indexes for better performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_clients_email ON clients(email)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_appointments_client_id ON appointments(client_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_appointments_start_time ON appointments(start_time)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_client_notes_client_id ON client_notes(client_id)')
            
            conn.commit()
            conn.close()
            
            logger.info("CRM database initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize CRM database: {e}")
            raise
    
    def add_client(self, client: Client) -> bool:
        """Add a new client to the CRM"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO clients VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                client.id, client.name, client.email, client.phone, client.address,
                client.city, client.state, client.zip_code, client.country,
                client.company, client.website, json.dumps(client.social_media),
                client.referral_source, client.marketing_consent, json.dumps(client.tags),
                client.industry, client.budget_range, client.project_type,
                client.notes, client.internal_notes, json.dumps(client.preferences),
                client.created_at.isoformat(), client.updated_at.isoformat(),
                client.last_contact.isoformat() if client.last_contact else None,
                client.last_appointment.isoformat() if client.last_appointment else None,
                client.total_appointments, client.total_spent,
                client.average_session_value, client.customer_lifetime_value
            ))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Client {client.name} added to CRM")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add client {client.name}: {e}")
            return False
    
    def get_client(self, client_id: str) -> Optional[Client]:
        """Get client by ID"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM clients WHERE id = ?', (client_id,))
            row = cursor.fetchone()
            
            conn.close()
            
            if row:
                return self._row_to_client(row)
            return None
            
        except Exception as e:
            logger.error(f"Failed to get client {client_id}: {e}")
            return None
    
    def get_client_by_email(self, email: str) -> Optional[Client]:
        """Get client by email"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM clients WHERE email = ?', (email,))
            row = cursor.fetchone()
            
            conn.close()
            
            if row:
                return self._row_to_client(row)
            return None
            
        except Exception as e:
            logger.error(f"Failed to get client by email {email}: {e}")
            return None
    
    def search_clients(self, query: str, limit: int = 50) -> List[Client]:
        """Search clients by name, email, or company"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            search_query = f"%{query}%"
            cursor.execute('''
                SELECT * FROM clients 
                WHERE name LIKE ? OR email LIKE ? OR company LIKE ? OR phone LIKE ?
                ORDER BY name
                LIMIT ?
            ''', (search_query, search_query, search_query, search_query, limit))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [self._row_to_client(row) for row in rows]
            
        except Exception as e:
            logger.error(f"Failed to search clients: {e}")
            return []
    
    def get_clients_by_tag(self, tag: str) -> List[Client]:
        """Get all clients with a specific tag"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM clients WHERE tags LIKE ?', (f'%{tag}%',))
            rows = cursor.fetchall()
            
            conn.close()
            
            return [self._row_to_client(row) for row in rows]
            
        except Exception as e:
            logger.error(f"Failed to get clients by tag {tag}: {e}")
            return []
    
    def update_client(self, client: Client) -> bool:
        """Update existing client"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE clients SET
                    name = ?, email = ?, phone = ?, address = ?, city = ?, state = ?,
                    zip_code = ?, country = ?, company = ?, website = ?, social_media = ?,
                    referral_source = ?, marketing_consent = ?, tags = ?, industry = ?,
                    budget_range = ?, project_type = ?, notes = ?, internal_notes = ?,
                    preferences = ?, updated_at = ?, last_contact = ?, last_appointment = ?,
                    total_appointments = ?, total_spent = ?, average_session_value = ?,
                    customer_lifetime_value = ?
                WHERE id = ?
            ''', (
                client.name, client.email, client.phone, client.address, client.city,
                client.state, client.zip_code, client.country, client.company,
                client.website, json.dumps(client.social_media), client.referral_source,
                client.marketing_consent, json.dumps(client.tags), client.industry,
                client.budget_range, client.project_type, client.notes,
                client.internal_notes, json.dumps(client.preferences),
                client.updated_at.isoformat(),
                client.last_contact.isoformat() if client.last_contact else None,
                client.last_appointment.isoformat() if client.last_appointment else None,
                client.total_appointments, client.total_spent,
                client.average_session_value, client.customer_lifetime_value, client.id
            ))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Client {client.name} updated in CRM")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update client {client.name}: {e}")
            return False
    
    def add_appointment(self, appointment: Appointment) -> bool:
        """Add appointment to CRM and update client metrics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Insert appointment
            cursor.execute('''
                INSERT OR REPLACE INTO appointments VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                appointment.id, appointment.client_id, appointment.client_name,
                appointment.client_email, appointment.start_time.isoformat(),
                appointment.end_time.isoformat(), appointment.duration,
                appointment.session_type, appointment.status, appointment.priority,
                appointment.location, json.dumps(appointment.equipment_needed),
                appointment.session_fee, appointment.additional_charges,
                appointment.discount, appointment.total_amount,
                appointment.payment_status, appointment.notes,
                appointment.internal_notes, appointment.client_requests,
                appointment.special_instructions, appointment.referral_source,
                appointment.marketing_campaign, appointment.follow_up_required,
                appointment.follow_up_notes, appointment.calendar_event_id,
                appointment.gmail_message_id, appointment.created_at.isoformat(),
                appointment.updated_at.isoformat()
            ))
            
            # Update client metrics if client_id exists
            if appointment.client_id:
                cursor.execute('''
                    UPDATE clients SET
                        total_appointments = total_appointments + 1,
                        total_spent = total_spent + ?,
                        last_appointment = ?,
                        updated_at = ?
                    WHERE id = ?
                ''', (appointment.total_amount, appointment.start_time.isoformat(), datetime.now().isoformat(), appointment.client_id))
                
                # Recalculate average session value
                cursor.execute('''
                    UPDATE clients SET
                        average_session_value = total_spent / total_appointments,
                        customer_lifetime_value = total_spent
                    WHERE id = ?
                ''', (appointment.client_id,))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Appointment {appointment.id} added to CRM")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add appointment {appointment.id}: {e}")
            return False
    
    def get_client_appointments(self, client_id: str) -> List[Appointment]:
        """Get all appointments for a specific client"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM appointments WHERE client_id = ? ORDER BY start_time DESC', (client_id,))
            rows = cursor.fetchall()
            
            conn.close()
            
            return [self._row_to_appointment(row) for row in rows]
            
        except Exception as e:
            logger.error(f"Failed to get appointments for client {client_id}: {e}")
            return []
    
    def add_client_note(self, note: ClientNote) -> bool:
        """Add a note to a client"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO client_notes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                note.id, note.client_id, note.note_type, note.title,
                note.content, note.author, note.is_internal,
                note.created_at.isoformat(), note.updated_at.isoformat()
            ))
            
            # Update client's last_contact
            cursor.execute('''
                UPDATE clients SET last_contact = ?, updated_at = ? WHERE id = ?
            ''', (datetime.now().isoformat(), datetime.now().isoformat(), note.client_id))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Note added to client {note.client_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add note: {e}")
            return False
    
    def get_client_notes(self, client_id: str, include_internal: bool = True) -> List[ClientNote]:
        """Get all notes for a client"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if include_internal:
                cursor.execute('SELECT * FROM client_notes WHERE client_id = ? ORDER BY created_at DESC', (client_id,))
            else:
                cursor.execute('SELECT * FROM client_notes WHERE client_id = ? AND is_internal = 0 ORDER BY created_at DESC', (client_id,))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [self._row_to_client_note(row) for row in rows]
            
        except Exception as e:
            logger.error(f"Failed to get notes for client {client_id}: {e}")
            return []
    
    def get_crm_analytics(self) -> Dict[str, Any]:
        """Get comprehensive CRM analytics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            analytics = {}
            
            # Total clients
            cursor.execute('SELECT COUNT(*) FROM clients')
            analytics['total_clients'] = cursor.fetchone()[0]
            
            # New clients this month
            month_ago = (datetime.now() - timedelta(days=30)).isoformat()
            cursor.execute('SELECT COUNT(*) FROM clients WHERE created_at >= ?', (month_ago,))
            analytics['new_clients_month'] = cursor.fetchone()[0]
            
            # Total appointments
            cursor.execute('SELECT COUNT(*) FROM appointments')
            analytics['total_appointments'] = cursor.fetchone()[0]
            
            # Appointments this month
            cursor.execute('SELECT COUNT(*) FROM appointments WHERE start_time >= ?', (month_ago,))
            analytics['appointments_month'] = cursor.fetchone()[0]
            
            # Total revenue
            cursor.execute('SELECT SUM(total_amount) FROM appointments WHERE payment_status = "paid"')
            total_revenue = cursor.fetchone()[0] or 0
            analytics['total_revenue'] = total_revenue
            
            # Monthly revenue
            cursor.execute('SELECT SUM(total_amount) FROM appointments WHERE payment_status = "paid" AND start_time >= ?', (month_ago,))
            monthly_revenue = cursor.fetchone()[0] or 0
            analytics['monthly_revenue'] = monthly_revenue
            
            # Average session value
            cursor.execute('SELECT AVG(total_amount) FROM appointments WHERE payment_status = "paid"')
            avg_session = cursor.fetchone()[0] or 0
            analytics['average_session_value'] = avg_session
            
            # Top referral sources
            cursor.execute('''
                SELECT referral_source, COUNT(*) as count 
                FROM clients 
                WHERE referral_source IS NOT NULL AND referral_source != ''
                GROUP BY referral_source 
                ORDER BY count DESC 
                LIMIT 5
            ''')
            analytics['top_referral_sources'] = dict(cursor.fetchall())
            
            # Client tags distribution
            cursor.execute('SELECT tags FROM clients WHERE tags IS NOT NULL AND tags != "[]"')
            tag_rows = cursor.fetchall()
            tag_counts = defaultdict(int)
            for row in tag_rows:
                tags = json.loads(row[0])
                for tag in tags:
                    tag_counts[tag] += 1
            analytics['tag_distribution'] = dict(tag_counts)
            
            # Payment status distribution
            cursor.execute('''
                SELECT payment_status, COUNT(*) as count 
                FROM appointments 
                GROUP BY payment_status
            ''')
            analytics['payment_status_distribution'] = dict(cursor.fetchall())
            
            conn.close()
            
            return analytics
            
        except Exception as e:
            logger.error(f"Failed to get CRM analytics: {e}")
            return {}
    
    def get_follow_up_tasks(self) -> List[Dict[str, Any]]:
        """Get all follow-up tasks that need attention"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT a.id, a.client_name, a.follow_up_notes, a.start_time, c.email, c.phone
                FROM appointments a
                LEFT JOIN clients c ON a.client_id = c.id
                WHERE a.follow_up_required = 1
                ORDER BY a.start_time DESC
            ''')
            
            rows = cursor.fetchall()
            conn.close()
            
            follow_ups = []
            for row in rows:
                follow_ups.append({
                    'appointment_id': row[0],
                    'client_name': row[1],
                    'follow_up_notes': row[2],
                    'appointment_date': row[3],
                    'client_email': row[4],
                    'client_phone': row[5]
                })
            
            return follow_ups
            
        except Exception as e:
            logger.error(f"Failed to get follow-up tasks: {e}")
            return []
    
    def export_client_data(self, client_id: str) -> Dict[str, Any]:
        """Export comprehensive client data for reporting"""
        try:
            client = self.get_client(client_id)
            if not client:
                return {}
            
            appointments = self.get_client_appointments(client_id)
            notes = self.get_client_notes(client_id)
            
            return {
                'client': client.to_dict(),
                'appointments': [apt.to_dict() for apt in appointments],
                'notes': [note.to_dict() for note in notes],
                'export_date': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to export client data: {e}")
            return {}
    
    def _row_to_client(self, row: Tuple) -> Client:
        """Convert database row to Client object"""
        return Client(
            id=row[0], name=row[1], email=row[2], phone=row[3], address=row[4],
            city=row[5], state=row[6], zip_code=row[7], country=row[8],
            company=row[9], website=row[10], social_media=json.loads(row[11]) if row[11] else {},
            referral_source=row[12], marketing_consent=bool(row[13]), tags=json.loads(row[14]) if row[14] else [],
            industry=row[15], budget_range=row[16], project_type=row[17],
            notes=row[18], internal_notes=row[19], preferences=json.loads(row[20]) if row[20] else {},
            created_at=datetime.fromisoformat(row[21]), updated_at=datetime.fromisoformat(row[22]),
            last_contact=datetime.fromisoformat(row[23]) if row[23] else None,
            last_appointment=datetime.fromisoformat(row[24]) if row[24] else None,
            total_appointments=row[25], total_spent=row[26],
            average_session_value=row[27], customer_lifetime_value=row[28]
        )
    
    def _row_to_appointment(self, row: Tuple) -> Appointment:
        """Convert database row to Appointment object"""
        return Appointment(
            id=row[0], client_id=row[1], client_name=row[2], client_email=row[3],
            start_time=datetime.fromisoformat(row[4]), end_time=datetime.fromisoformat(row[5]),
            duration=row[6], session_type=row[7], status=row[8], priority=row[9],
            location=row[10], equipment_needed=json.loads(row[11]) if row[11] else [],
            session_fee=row[12], additional_charges=row[13], discount=row[14],
            total_amount=row[15], payment_status=row[16], notes=row[17],
            internal_notes=row[18], client_requests=row[19], special_instructions=row[20],
            referral_source=row[21], marketing_campaign=row[22], follow_up_required=bool(row[23]),
            follow_up_notes=row[24], calendar_event_id=row[25], gmail_message_id=row[26],
            created_at=datetime.fromisoformat(row[27]), updated_at=datetime.fromisoformat(row[28])
        )
    
    def _row_to_client_note(self, row: Tuple) -> ClientNote:
        """Convert database row to ClientNote object"""
        return ClientNote(
            id=row[0], client_id=row[1], note_type=row[2], title=row[3],
            content=row[4], author=row[5], is_internal=bool(row[6]),
            created_at=datetime.fromisoformat(row[7]), updated_at=datetime.fromisoformat(row[8])
        )
