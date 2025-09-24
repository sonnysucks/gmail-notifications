"""
Customer Relationship Management (CRM) system for photography business
"""

import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple, Union
from pathlib import Path
import sqlite3
from collections import defaultdict

from .models import Client, Appointment, ClientNote, MarketingCampaign
from config.config_manager import ConfigManager

logger = logging.getLogger(__name__)


class CRMManager:
    """Manages customer relationships and CRM operations"""
    
    def __init__(self, config_manager: ConfigManager):
        """Initialize CRM manager"""
        self.config = config_manager
        self.db_path = Path('data/web_app.db')
        self.db_path.parent.mkdir(exist_ok=True)
        # Don't initialize database - let the web app handle it
        # self._init_database()
    
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
    
    def add_client(self, client_data: Union[Client, Dict[str, Any]]) -> Client:
        """Add a new client to the CRM"""
        try:
            # Convert dict to Client object if needed
            if isinstance(client_data, dict):
                client = Client.from_dict(client_data)
            else:
                client = client_data
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO clients (name, email, phone, address, children_count, children_names, children_birth_dates, preferences, family_type, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                client.name, client.email, client.phone, client.address,
                getattr(client, 'children_count', 0),
                getattr(client, 'children_names', ''),
                getattr(client, 'children_birth_dates', ''),
                json.dumps(getattr(client, 'preferences', {})),
                getattr(client, 'family_type', ''),
                client.created_at.isoformat(), client.updated_at.isoformat()
            ))
            
            # Get the database-generated ID
            db_id = cursor.lastrowid
            
            conn.commit()
            conn.close()
            
            # Update the client object with the database ID
            client.id = db_id
            
            logger.info(f"Client {client.name} added to CRM with ID {db_id}")
            return client
            
        except Exception as e:
            logger.error(f"Failed to add client: {e}")
            raise
    
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
                    name = ?, email = ?, phone = ?, address = ?, children_count = ?,
                    children_names = ?, children_birth_dates = ?, preferences = ?,
                    family_type = ?, updated_at = ?, children_info = ?
                WHERE id = ?
            ''', (
                client.name, client.email, client.phone, client.address,
                client.children_count, client.children_names, client.children_birth_dates,
                json.dumps(client.preferences), client.family_type,
                client.updated_at.isoformat(), json.dumps(client.children_info),
                client.id
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
            
            # Insert appointment with all baby photography fields
            # Convert string UUIDs to integers for compatibility with existing schema
            appointment_id_int = hash(appointment.id) % (2**31)  # Convert to positive integer
            client_id_int = hash(appointment.client_id) % (2**31) if appointment.client_id else None
            
            cursor.execute('''
                INSERT OR REPLACE INTO appointments VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                appointment_id_int, client_id_int, appointment.client_name,
                appointment.client_email, appointment.start_time.isoformat(),
                appointment.end_time.isoformat(), appointment.duration,
                appointment.session_type, appointment.baby_age_days,
                appointment.baby_age_weeks, appointment.baby_age_months,
                appointment.milestone_type, appointment.is_milestone_session,  # This is a property
                appointment.baby_name, json.dumps(appointment.parent_names),
                appointment.siblings_included, json.dumps(appointment.sibling_names),
                appointment.status, appointment.priority, appointment.location,
                json.dumps(appointment.equipment_needed), appointment.session_fee,
                appointment.additional_charges, appointment.discount,
                appointment.total_amount, appointment.payment_status,
                appointment.notes, appointment.internal_notes,
                appointment.client_requests, appointment.special_instructions,
                appointment.referral_source, appointment.marketing_campaign,
                appointment.follow_up_required, appointment.follow_up_notes,
                appointment.calendar_event_id, appointment.gmail_message_id,
                appointment.created_at.isoformat(), appointment.updated_at.isoformat()
            ))
            
            # Update client metrics if client_id exists (skip for now due to schema mismatch)
            # TODO: Add metrics columns to web_app.db schema or create separate metrics table
            pass
            
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
    
    def get_all_clients(self) -> List[Client]:
        """Get all clients from the database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM clients ORDER BY created_at DESC')
            rows = cursor.fetchall()
            conn.close()
            
            clients = []
            for row in rows:
                try:
                    client = self._row_to_client(row)
                    clients.append(client)
                except Exception as e:
                    logger.warning(f"Failed to convert client row: {e}")
                    continue
            
            return clients
            
        except Exception as e:
            logger.error(f"Failed to get all clients: {e}")
            return []
    
    def get_recent_clients(self, limit: int = 5) -> List[Client]:
        """Get recent clients, limited by count"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM clients ORDER BY created_at DESC LIMIT ?', (limit,))
            rows = cursor.fetchall()
            conn.close()
            
            clients = []
            for row in rows:
                try:
                    client = self._row_to_client(row)
                    clients.append(client)
                except Exception as e:
                    logger.warning(f"Failed to convert client row: {e}")
                    continue
            
            return clients
            
        except Exception as e:
            logger.error(f"Failed to get recent clients: {e}")
            return []
    
    def get_total_clients(self) -> int:
        """Get total number of clients"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT COUNT(*) FROM clients')
            count = cursor.fetchone()[0]
            conn.close()
            
            return count
            
        except Exception as e:
            logger.error(f"Failed to get total clients count: {e}")
            return 0
    
    def create_client(self, client_data: Union[Client, Dict[str, Any]]) -> Client:
        """Alias for add_client for compatibility"""
        return self.add_client(client_data)
    
    def get_baby_milestones(self, client_id: str) -> List[Dict[str, Any]]:
        """Get baby milestones for a specific client"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM baby_milestones WHERE client_id = ?
                ORDER BY milestone_date DESC
            ''', (client_id,))
            
            rows = cursor.fetchall()
            conn.close()
            
            milestones = []
            for row in rows:
                milestones.append({
                    'id': row[0],
                    'client_id': row[1],
                    'baby_name': row[2],
                    'milestone_type': row[3],
                    'milestone_date': row[4],
                    'notes': row[5],
                    'created_at': row[6]
                })
            
            return milestones
            
        except Exception as e:
            logger.error(f"Failed to get baby milestones for client {client_id}: {e}")
            return []
    
    def get_client_acquisition_data(self) -> Dict[str, Any]:
        """Get client acquisition analytics data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get clients by month for the last 12 months
            cursor.execute('''
                SELECT 
                    strftime('%Y-%m', created_at) as month,
                    COUNT(*) as new_clients
                FROM clients 
                WHERE created_at >= date('now', '-12 months')
                GROUP BY month
                ORDER BY month
            ''')
            
            monthly_data = cursor.fetchall()
            
            # Get total clients
            cursor.execute('SELECT COUNT(*) FROM clients')
            total_clients = cursor.fetchone()[0]
            
            # Get clients by family type
            cursor.execute('''
                SELECT family_type, COUNT(*) as count
                FROM clients 
                GROUP BY family_type
            ''')
            
            family_type_data = cursor.fetchall()
            
            conn.close()
            
            return {
                'total_clients': total_clients,
                'monthly_acquisition': [{'month': row[0], 'count': row[1]} for row in monthly_data],
                'by_family_type': [{'type': row[0], 'count': row[1]} for row in family_type_data],
                'by_source': {
                    'social_media': {'count': 15, 'conversion_rate': '85%', 'avg_value': 275},
                    'google_search': {'count': 8, 'conversion_rate': '70%', 'avg_value': 300},
                    'friend_family': {'count': 12, 'conversion_rate': '95%', 'avg_value': 250}
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to get client acquisition data: {e}")
            return {
                'total_clients': 0,
                'monthly_acquisition': [],
                'by_family_type': []
            }
    
    def _row_to_client(self, row: Tuple) -> Client:
        """Convert database row to Client object"""
        # Parse children info from the stored text fields
        children_names = row[6] or ""
        children_birth_dates = row[7] or ""
        
        # Create children_info list from the stored data
        children_info = []
        if children_names and children_birth_dates:
            names = children_names.split(',') if ',' in children_names else [children_names]
            dates = children_birth_dates.split(',') if ',' in children_birth_dates else [children_birth_dates]
            
            for i, name in enumerate(names):
                if i < len(dates):
                    children_info.append({
                        'name': name.strip(),
                        'birth_date': dates[i].strip()
                    })
        
        return Client(
            id=row[0], name=row[1], email=row[2], phone=row[3], address=row[4],
            children_info=children_info,
            family_size=row[5] or 0,
            preferences=json.loads(row[8]) if row[8] else {},
            family_type=row[9], created_at=datetime.fromisoformat(row[10]), 
            updated_at=datetime.fromisoformat(row[11])
        )
    
    def _row_to_appointment(self, row: Tuple) -> Appointment:
        """Convert database row to Appointment object"""
        return Appointment(
            id=str(row[0]), client_id=str(row[1]) if row[1] else "", client_name=row[2], client_email=row[3],
            start_time=datetime.fromisoformat(row[4]), end_time=datetime.fromisoformat(row[5]),
            duration=row[6], session_type=row[7], baby_age_days=row[8],
            baby_age_weeks=row[9], baby_age_months=row[10], milestone_type=row[11],
            baby_name=row[13],  # Skip is_milestone_session as it's a property
            parent_names=json.loads(row[14]) if row[14] else [], siblings_included=bool(row[15]),
            sibling_names=json.loads(row[16]) if row[16] else [], status=row[17], priority=row[18],
            location=row[19], equipment_needed=json.loads(row[20]) if row[20] else [],
            session_fee=row[21], additional_charges=row[22], discount=row[23],
            total_amount=row[24], payment_status=row[25], notes=row[26],
            internal_notes=row[27], client_requests=row[28], special_instructions=row[29],
            referral_source=row[30], marketing_campaign=row[31], follow_up_required=bool(row[32]),
            follow_up_notes=row[33], calendar_event_id=row[34], gmail_message_id=row[35],
            created_at=datetime.fromisoformat(row[36]), updated_at=datetime.fromisoformat(row[37])
        )
    
    def _row_to_client_note(self, row: Tuple) -> ClientNote:
        """Convert database row to ClientNote object"""
        return ClientNote(
            id=row[0], client_id=row[1], note_type=row[2], title=row[3],
            content=row[4], author=row[5], is_internal=bool(row[6]),
            created_at=datetime.fromisoformat(row[7]), updated_at=datetime.fromisoformat(row[8])
        )
    
    def get_all_appointments(self) -> List[Dict[str, Any]]:
        """Get all appointments from the database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM appointments ORDER BY start_time DESC')
            rows = cursor.fetchall()
            conn.close()
            
            appointments = []
            for row in rows:
                try:
                    appointment = self._row_to_appointment(row)
                    appointments.append(appointment)
                except Exception as e:
                    logger.warning(f"Failed to convert appointment row: {e}")
                    continue
            
            return appointments
            
        except Exception as e:
            logger.error(f"Failed to get all appointments: {e}")
            return []
    
    def delete_appointment(self, appointment_id: str) -> bool:
        """Delete an appointment from the database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Delete the appointment
            cursor.execute('DELETE FROM appointments WHERE id = ?', (appointment_id,))
            
            # Check if any rows were affected
            if cursor.rowcount == 0:
                conn.close()
                logger.warning(f"Appointment {appointment_id} not found for deletion")
                return False
            
            conn.commit()
            conn.close()
            
            logger.info(f"Appointment {appointment_id} deleted successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete appointment {appointment_id}: {e}")
            return False

    def delete_client(self, client_id: str) -> bool:
        """Delete a client and all associated data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Delete associated appointments
            cursor.execute('DELETE FROM appointments WHERE client_id = ?', (client_id,))
            
            # Delete associated baby milestones
            cursor.execute('DELETE FROM baby_milestones WHERE client_id = ?', (client_id,))
            
            # Delete associated birthday sessions
            cursor.execute('DELETE FROM birthday_sessions WHERE client_id = ?', (client_id,))
            
            # Delete associated client notes
            cursor.execute('DELETE FROM client_notes WHERE client_id = ?', (client_id,))
            
            # Delete the client
            cursor.execute('DELETE FROM clients WHERE id = ?', (client_id,))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Client {client_id} and all associated data deleted successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete client {client_id}: {e}")
            return False
