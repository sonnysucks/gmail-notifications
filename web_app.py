#!/usr/bin/env python3
"""
Gmail Photography Appointment Scheduler Web Application
Specialized for Maternity, Baby, Smash Cake, and Birthday Photography

A comprehensive web interface for photographers to:
- Configure and set up the system
- Manage appointments and clients
- Handle baby photography workflows
- Access CRM and business analytics
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import text
from datetime import datetime
import os
import json
import yaml
from datetime import datetime, timedelta
import uuid
from typing import Dict, Any, List, Optional

# Import ICS generator
from utils.ics_generator import ICSGenerator, ICSAppointment

# Import our existing modules
try:
    from scheduler.models import Client, Appointment, BabyMilestone, BirthdaySession, ClientNote, Package
    from scheduler.crm_manager import CRMManager
    from scheduler.appointment_scheduler import AppointmentScheduler
    from gmail.gmail_manager import GmailManager
    from calendar_integration.calendar_manager import CalendarManager
    from config.config_manager import ConfigManager
except ImportError:
    # Fallback for import issues
    print("Warning: Some modules couldn't be imported. Using mock data for demonstration.")
    # Create mock classes for demonstration
    class MockManager:
        def get_config(self): return {}
    def get(self, key, default=None): return default
    def get_business_info(self): return {}
    def get_calendar_config(self): return {}
    def get_appointment_config(self): return {}
    def get_email_config(self): return {}
    def get_gmail_config(self): return {}
    def get_session_types(self): return {
        'newborn': {'name': 'Newborn Session', 'base_price': 250, 'description': 'Perfect for babies 5-14 days old', 'includes': ['2-3 hours', '50+ edited images', 'Online gallery'], 'duration': '2-3 hours', 'recommended_age': '5-14 days'},
        'milestone': {'name': 'Milestone Session', 'base_price': 200, 'description': 'Capture special moments at 3, 6, 9, 12 months', 'includes': ['1 hour', '30+ edited images', 'Online gallery'], 'duration': '1 hour', 'recommended_age': '3-12 months'},
        'birthday': {'name': 'Birthday Session', 'base_price': 225, 'description': 'Celebrate birthdays with themed photography', 'includes': ['1.5 hours', '40+ edited images', 'Online gallery'], 'duration': '1.5 hours', 'recommended_age': '1+ years'}
    }
    def get_all_clients(self): return []
    def get_recent_clients(self, limit=5): return []
    def get_total_clients(self): return 0
    def get_client_acquisition_data(self): return {}
    def get_baby_milestones(self, client_id): return []
    def create_client(self, data): return type('MockClient', (), {'id': 1})()
    def update_client(self, client_id, data): return type('MockClient', (), {'id': client_id})()
    def get_client(self, client_id): return type('MockClient', (), {'id': client_id, 'name': 'Demo Client'})()
    
    class MockAppointmentScheduler:
        def get_appointments_by_date(self, date): return []
        def get_upcoming_appointments(self, limit=10): return []
        def get_all_appointments(self): return []
        def get_total_appointments(self): return 0
        def get_monthly_revenue(self): return 0
        def get_monthly_revenue_data(self): return {}
        def get_session_type_statistics(self): return {}
        def get_milestone_package_data(self): return {}
        def get_appointments_in_range(self, start, end): return []
        def get_client_appointments(self, client_id): return []
        def create_appointment(self, data): return type('MockAppointment', (), {'id': 1})()
        def update_appointment(self, appointment_id, data): return type('MockAppointment', (), {'id': appointment_id})()
        def get_appointment(self, appointment_id): return type('MockAppointment', (), {'id': appointment_id, 'start_time': datetime.now(), 'client_name': 'Demo Client', 'session_type': 'Newborn', 'status': 'confirmed'})()
    
    config_manager = MockManager()
    crm_manager = MockManager()
    appointment_scheduler = MockAppointmentScheduler()
    gmail_manager = MockManager()
    calendar_manager = MockManager()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.abspath("data/web_app.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize our managers
try:
    config_manager = ConfigManager()
    crm_manager = CRMManager(config_manager)
    appointment_scheduler = AppointmentScheduler(config_manager)
    gmail_manager = GmailManager(config_manager)
    calendar_manager = CalendarManager(config_manager)
except NameError:
    # Use mock managers if imports failed
    pass

# User model for web app authentication
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), default='photographer')  # photographer, admin, staff
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Context processor to make business settings available globally
@app.context_processor
def inject_business_config():
    """Make business configuration available in all templates"""
    try:
        config = config_manager.config
        business_config = config.get('business', {})
        
        return {
            'business': {
                'name': business_config.get('name', 'Your Photography Business'),
                'email': business_config.get('email', ''),
                'phone': business_config.get('phone', ''),
                'website': business_config.get('website', ''),
                'address': business_config.get('address', ''),
                'business_type': business_config.get('business_type', ''),
                'tax_id': business_config.get('tax_id', ''),
                'specialties': business_config.get('specialties', [])
            },
            'config': config  # Also make full config available
        }
    except Exception as e:
        print(f"Warning: Could not load business config: {e}")
        return {
            'business': {
                'name': 'Your Photography Business',
                'email': '',
                'phone': '',
                'website': '',
                'address': '',
                'business_type': '',
                'tax_id': '',
                'specialties': []
            },
            'config': {}
        }

# Routes
@app.route('/')
def index():
    """Landing page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            user.last_login = datetime.utcnow()
            db.session.commit()
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard"""
    # Get today's appointments (for stats)
    today = datetime.now().date()
    today_appointments = appointment_scheduler.get_appointments_by_date(today)
    
    # Get the next scheduled appointment (chronologically)
    next_appointment = appointment_scheduler.get_next_appointment()
    
    # Get upcoming appointments
    upcoming_appointments = appointment_scheduler.get_upcoming_appointments(limit=10)
    
    # Get recent clients
    recent_clients = crm_manager.get_recent_clients(limit=5)
    
    # Get business metrics
    total_clients = crm_manager.get_total_clients()
    total_appointments = appointment_scheduler.get_total_appointments()
    monthly_revenue = appointment_scheduler.get_monthly_revenue()
    
    return render_template('dashboard.html',
                         today_appointments=today_appointments,
                         next_appointment=next_appointment,
                         upcoming_appointments=upcoming_appointments,
                         recent_clients=recent_clients,
                         total_clients=total_clients,
                         total_appointments=total_appointments,
                         monthly_revenue=monthly_revenue,
                         today=today)

@app.route('/setup')
@login_required
def setup():
    """System setup and configuration"""
    config = config_manager.config
    return render_template('setup.html', config=config)

@app.route('/google-calendar-config')
@login_required
def google_calendar_config():
    """Google Calendar configuration and sync settings"""
    # Get current calendar configuration
    calendar_config = config_manager.get_calendar_config()
    
    # Get available calendars (this would come from Google Calendar API)
    available_calendars = [
        {'id': 'primary', 'name': 'Primary Calendar', 'description': 'Your main Google Calendar'},
        {'id': 'work', 'name': 'Work Calendar', 'description': 'Business appointments and meetings'},
        {'id': 'personal', 'name': 'Personal Calendar', 'description': 'Personal events and activities'}
    ]
    
    return render_template('google_calendar_config.html', 
                         calendar_config=calendar_config,
                         available_calendars=available_calendars)

@app.route('/google-calendar-config/save', methods=['POST'])
@login_required
def save_google_calendar_config():
    """Save Google Calendar configuration"""
    try:
        data = request.get_json()
        
        # Update calendar configuration
        config = config_manager.config
        if 'calendar' not in config:
            config['calendar'] = {}
        
        # Update calendar settings
        config['calendar'].update({
            # OAuth Credentials
            'client_id': data.get('client_id', ''),
            'client_secret': data.get('client_secret', ''),
            'google_account': data.get('google_account', ''),
            'calendar_id': data.get('calendar_id', 'primary'),
            'custom_calendar_id': data.get('custom_calendar_id', ''),
            
            # Calendar Settings
            'primary_calendar': data.get('primary_calendar', 'primary'),
            'sync_direction': data.get('sync_direction', 'bidirectional'),
            'sync_frequency': data.get('sync_frequency', 'realtime'),
            'default_duration': data.get('default_duration', '60'),
            'buffer_time': data.get('buffer_time', '15'),
            'working_hours_start': data.get('working_hours_start', '09:00'),
            'working_hours_end': data.get('working_hours_end', '17:00'),
            'auto_confirm': data.get('auto_confirm', False),
            'send_reminders': data.get('send_reminders', True),
            'event_title_format': data.get('event_title_format', '{client_name} - {session_type}'),
            'event_description_template': data.get('event_description_template', ''),
            'event_color': data.get('event_color', 'blue'),
            'event_visibility': data.get('event_visibility', 'default'),
            'last_updated': datetime.now().isoformat()
        })
        
        # Save configuration
        config_manager.save_config(config)
        
        return jsonify({'success': True, 'message': 'Calendar configuration saved successfully'})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/setup/save', methods=['POST'])
@login_required
def save_setup():
    """Save configuration changes"""
    try:
        config_data = request.get_json()
        config_manager.update_config(config_data)
        flash('Configuration saved successfully!', 'success')
        return jsonify({'success': True})
    except Exception as e:
        flash(f'Error saving configuration: {str(e)}', 'error')
        return jsonify({'success': False, 'error': str(e)})

@app.route('/change-password', methods=['POST'])
@login_required
def change_password():
    """Change user password"""
    try:
        data = request.get_json()
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')
        
        # Validate input
        if not current_password or not new_password or not confirm_password:
            return jsonify({'success': False, 'error': 'All fields are required'})
        
        if new_password != confirm_password:
            return jsonify({'success': False, 'error': 'New passwords do not match'})
        
        if len(new_password) < 6:
            return jsonify({'success': False, 'error': 'Password must be at least 6 characters long'})
        
        # Verify current password
        if not current_user.check_password(current_password):
            return jsonify({'success': False, 'error': 'Current password is incorrect'})
        
        # Update password
        current_user.set_password(new_password)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Password changed successfully!'})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/appointments')
@login_required
def appointments():
    """Appointment management"""
    appointments = appointment_scheduler.get_all_appointments()
    return render_template('appointments.html', appointments=appointments)

@app.route('/appointments/new', methods=['GET', 'POST'])
@login_required
def new_appointment():
    """Create new appointment"""
    if request.method == 'POST':
        try:
            appointment_data = request.get_json()
            
            # Extract required parameters (handle both form field names and method parameter names)
            client_id = appointment_data.get('client_id', '')
            client_name = appointment_data.get('client_name', '')
            datetime_str = appointment_data.get('datetime_str', appointment_data.get('start_time', ''))
            session_type = appointment_data.get('session_type', '')
            duration = appointment_data.get('duration', None)
            notes = appointment_data.get('notes', '')
            client_email = appointment_data.get('client_email', '')
            session_fee = appointment_data.get('session_fee', 0.0)
            
            # If we have client_id but no client_name, get the client name from the database
            if client_id and not client_name:
                client = crm_manager.get_client(client_id)
                if client:
                    client_name = client.name
                    client_email = client.email
            
            # Remove parameters we've already extracted to avoid duplicates
            additional_params = appointment_data.copy()
            additional_params.pop('client_id', None)
            additional_params.pop('client_name', None)
            additional_params.pop('datetime_str', None)
            additional_params.pop('start_time', None)
            additional_params.pop('session_type', None)
            additional_params.pop('duration', None)
            additional_params.pop('notes', None)
            additional_params.pop('client_email', None)
            additional_params.pop('session_fee', None)
            additional_params.pop('total_amount', None)  # Remove total_amount to avoid duplicate
            
            # Remove fields that are not part of the Appointment model
            additional_params.pop('baby_birth_date', None)  # Remove this field
            additional_params.pop('age_turning', None)     # Not in Appointment model
            additional_params.pop('theme', None)          # Not in Appointment model
            additional_params.pop('cake_flavor', None)     # Not in Appointment model
            additional_params.pop('cake_design', None)     # Not in Appointment model
            additional_params.pop('parent_vision', None)   # Not in Appointment model
            
            # Create appointment with individual parameters
            appointment = appointment_scheduler.create_appointment(
                client_name=client_name,
                datetime_str=datetime_str,
                session_type=session_type,
                duration=duration,
                notes=notes,
                client_email=client_email,
                session_fee=session_fee,
                **additional_params  # Pass any additional parameters
            )
            
            # Generate ICS file as fallback for calendar integration
            try:
                ics_generator = ICSGenerator(config_manager.get('business.name', 'Photography Business'))
                
                appointment_data = {
                    'client_name': client_name,
                    'client_email': client_email,
                    'session_type': session_type,
                    'start_time': datetime_str,
                    'duration': duration,
                    'location': additional_params.get('location', 'Studio'),
                    'status': 'confirmed',
                    'notes': notes,
                    'special_instructions': additional_params.get('special_instructions', '')
                }
                
                ics_appointment = ics_generator.create_appointment_ics(appointment_data)
                filename = f"appointment_{appointment.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.ics"
                ics_filepath = ics_generator.save_ics_file([ics_appointment], filename)
                
                flash('Appointment created successfully! ICS file generated for calendar import.', 'success')
                return jsonify({
                    'success': True, 
                    'appointment_id': appointment.id,
                    'ics_file': filename,
                    'message': 'Appointment created and ICS file generated for calendar import'
                })
                
            except Exception as ics_error:
                # If ICS generation fails, still return success for the appointment
                flash('Appointment created successfully! (ICS generation failed)', 'success')
                return jsonify({'success': True, 'appointment_id': appointment.id})
        except Exception as e:
            flash(f'Error creating appointment: {str(e)}', 'error')
            return jsonify({'success': False, 'error': str(e)})
    
    # Get available clients and session types
    clients = crm_manager.get_all_clients()
    session_types_dict = config_manager.get('appointments.session_types', {})
    
    # Convert session types dictionary to template format
    session_types = {}
    for key, session in session_types_dict.items():
        session_types[key] = {
            'name': session.get('name', ''),
            'duration': session.get('duration', 60),
            'base_price': session.get('base_price', 0.0),
            'description': session.get('description', ''),
            'props': session.get('props', [])
        }
    
    return render_template('new_appointment.html', clients=clients, session_types=session_types)

@app.route('/appointments/<appointment_id>')
@login_required
def view_appointment(appointment_id):
    """View appointment details"""
    appointment = appointment_scheduler.get_appointment(appointment_id)
    if not appointment:
        flash('Appointment not found', 'error')
        return redirect(url_for('appointments'))
    
    return render_template('view_appointment.html', appointment=appointment)

@app.route('/appointments/<appointment_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_appointment(appointment_id):
    """Edit appointment"""
    appointment = appointment_scheduler.get_appointment(appointment_id)
    if not appointment:
        flash('Appointment not found', 'error')
        return redirect(url_for('appointments'))
    
    if request.method == 'POST':
        try:
            appointment_data = request.get_json()
            updated_appointment = appointment_scheduler.update_appointment(appointment_id, appointment_data)
            flash('Appointment updated successfully!', 'success')
            return jsonify({'success': True})
        except Exception as e:
            flash(f'Error updating appointment: {str(e)}', 'error')
            return jsonify({'success': False, 'error': str(e)})
    
    clients = crm_manager.get_all_clients()
    session_types_dict = config_manager.get('appointments.session_types', {})
    
    # Convert session types dictionary to template format
    session_types = {}
    for key, session in session_types_dict.items():
        session_types[key] = {
            'name': session.get('name', ''),
            'duration': session.get('duration', 60),
            'base_price': session.get('base_price', 0.0),
            'description': session.get('description', ''),
            'props': session.get('props', [])
        }
    
    return render_template('edit_appointment.html', 
                         appointment=appointment, 
                         clients=clients, 
                         session_types=session_types)

@app.route('/clients')
@login_required
def clients():
    """Client management"""
    clients = crm_manager.get_all_clients()
    return render_template('clients.html', clients=clients, now=datetime.now())

@app.route('/clients/new', methods=['GET', 'POST'])
@login_required
def new_client():
    """Create new client"""
    if request.method == 'POST':
        try:
            client_data = request.get_json()
            client = crm_manager.create_client(client_data)
            flash('Client created successfully!', 'success')
            return jsonify({'success': True, 'client_id': client.id})
        except Exception as e:
            flash(f'Error creating client: {str(e)}', 'error')
            return jsonify({'success': False, 'error': str(e)})
    
    return render_template('new_client.html')

@app.route('/clients/<client_id>')
@login_required
def view_client(client_id):
    """View client details"""
    client = crm_manager.get_client(client_id)
    if not client:
        flash('Client not found', 'error')
        return redirect(url_for('clients'))
    
    # Get client appointments
    appointments = appointment_scheduler.get_client_appointments(client_id)
    
    # Get baby milestones
    milestones = crm_manager.get_baby_milestones(client_id)
    
    return render_template('view_client.html', 
                         client=client, 
                         appointments=appointments, 
                         milestones=milestones)

@app.route('/clients/<client_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_client(client_id):
    """Edit client"""
    client = crm_manager.get_client(client_id)
    if not client:
        flash('Client not found', 'error')
        return redirect(url_for('clients'))
    
    if request.method == 'POST':
        try:
            client_data = request.get_json()
            updated_client = crm_manager.update_client(client_id, client_data)
            flash('Client updated successfully!', 'success')
            return jsonify({'success': True})
        except Exception as e:
            flash(f'Error updating client: {str(e)}', 'error')
            return jsonify({'success': False, 'error': str(e)})
    
    return render_template('edit_client.html', client=client)

@app.route('/calendar')
@login_required
def calendar():
    """Calendar view"""
    # Get appointments for the current month
    now = datetime.now()
    start_date = now.replace(day=1).date()  # Convert to date object
    if now.month == 12:
        end_date = (now.replace(year=now.year + 1, month=1, day=1) - timedelta(days=1)).date()
    else:
        end_date = (now.replace(month=now.month + 1, day=1) - timedelta(days=1)).date()
    
    appointments = appointment_scheduler.get_appointments_in_range(start_date, end_date)
    
    # Format appointments for JavaScript
    formatted_appointments = []
    for appointment in appointments:
        formatted_appointments.append({
            'id': appointment.id,
            'client_name': appointment.client_name,
            'session_type': appointment.session_type,
            'start_time': appointment.start_time.strftime('%Y-%m-%d %H:%M') if appointment.start_time else '',
            'status': appointment.status,
            'baby_name': getattr(appointment, 'baby_name', ''),
            'duration': appointment.duration
        })
    
    return render_template('calendar.html', 
                         appointments=formatted_appointments,
                         current_month=now.strftime('%B %Y'))

@app.route('/analytics')
@login_required
def analytics():
    """Business analytics and reporting"""
    # Get revenue data
    monthly_revenue = appointment_scheduler.get_monthly_revenue_data()
    
    # Get session type statistics
    session_stats = appointment_scheduler.get_session_type_statistics()
    
    # Get client acquisition data
    client_acquisition = crm_manager.get_client_acquisition_data()
    
    # Get milestone package data
    milestone_packages = appointment_scheduler.get_milestone_package_data()
    
    return render_template('analytics.html',
                         monthly_revenue=monthly_revenue,
                         session_stats=session_stats,
                         client_acquisition=client_acquisition,
                         milestone_packages=milestone_packages)

@app.route('/customer-info')
@app.route('/customer-info/<client_id>')
@login_required
def customer_info(client_id=None):
    """Customer information and pricing page"""
    # Get session types for pricing display
    session_types_dict = config_manager.get('appointments.session_types', {})
    
    # Convert session types dictionary to template format
    session_types = {}
    for key, session in session_types_dict.items():
        session_types[key] = {
            'name': session.get('name', ''),
            'duration': session.get('duration', 60),
            'base_price': session.get('base_price', 0.0),
            'description': session.get('description', ''),
            'props': session.get('props', [])
        }
    
    # Get client data if client_id is provided
    client = None
    if client_id:
        client = crm_manager.get_client(client_id)
    
    return render_template('customer_info.html', 
                         session_types=session_types, 
                         client=client,
                         client_id=client_id)

@app.route('/contract-template')
@login_required
def contract_template():
    """Contract template for download"""
    return render_template('contract_template.html')

@app.route('/session-checklist')
@login_required
def session_checklist():
    """Session checklist for download"""
    return render_template('session_checklist.html')

@app.route('/api/appointments')
@login_required
def api_appointments():
    """API endpoint for appointments"""
    appointments = appointment_scheduler.get_all_appointments()
    return jsonify([appointment.to_dict() for appointment in appointments])

@app.route('/api/appointments/<appointment_id>', methods=['DELETE'])
@login_required
def delete_appointment(appointment_id):
    """Delete an appointment"""
    try:
        # Check if appointment exists
        appointment = appointment_scheduler.get_appointment(appointment_id)
        if not appointment:
            return jsonify({'success': False, 'error': 'Appointment not found'}), 404
        
        # Delete the appointment
        success = appointment_scheduler.delete_appointment(appointment_id)
        if success:
            return jsonify({'success': True, 'message': 'Appointment deleted successfully'})
        else:
            return jsonify({'success': False, 'error': 'Failed to delete appointment'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/clients')
@login_required
def api_clients():
    """API endpoint for clients"""
    try:
        clients = crm_manager.get_all_clients()
        return jsonify({
            'success': True,
            'clients': [client.to_dict() for client in clients]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/clients/<client_id>', methods=['DELETE'])
@login_required
def delete_client(client_id):
    """Delete a client"""
    try:
        # Check if client exists
        client = crm_manager.get_client(client_id)
        if not client:
            return jsonify({'success': False, 'error': 'Client not found'}), 404
        
        # Check if client has appointments
        appointments = appointment_scheduler.get_client_appointments(client_id)
        if appointments:
            return jsonify({
                'success': False, 
                'error': 'Cannot delete client with existing appointments. Please delete appointments first.'
            }), 400
        
        # Delete the client
        success = crm_manager.delete_client(client_id)
        if success:
            return jsonify({'success': True, 'message': 'Client deleted successfully'})
        else:
            return jsonify({'success': False, 'error': 'Failed to delete client'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/session-types')
@login_required
def api_session_types():
    """API endpoint for session types"""
    session_types_dict = config_manager.get('appointments.session_types', {})
    
    # Convert session types dictionary to API format
    session_types = {}
    for key, session in session_types_dict.items():
        session_types[key] = {
            'name': session.get('name', ''),
            'duration': session.get('duration', 60),
            'base_price': session.get('base_price', 0.0),
            'description': session.get('description', ''),
            'props': session.get('props', [])
        }
    
    return jsonify(session_types)

@app.route('/api/baby-milestones/<client_id>')
@login_required
def api_baby_milestones(client_id):
    """API endpoint for baby milestones"""
    milestones = crm_manager.get_baby_milestones(client_id)
    return jsonify([milestone.to_dict() for milestone in milestones])

@app.route('/backup-restore')
@login_required
def backup_restore():
    """Backup and restore system page"""
    return render_template('backup_restore.html')

@app.route('/packages')
@login_required
def packages():
    """Package management page"""
    return render_template('packages.html')

@app.route('/api/client-packet/<client_id>')
@login_required
def generate_client_packet(client_id):
    """Generate a complete client packet PDF"""
    try:
        # Get client data
        client = crm_manager.get_client(client_id)
        if not client:
            return jsonify({'error': 'Client not found'}), 404
        
        # Get client's appointments
        appointments = crm_manager.get_client_appointments(client_id)
        
        # Get recommended packages
        family_type = client.family_type or 'family'
        packages = crm_manager.get_packages_by_category(family_type)
        if not packages:
            packages = crm_manager.get_active_packages()[:3]  # Get top 3 packages
        
        # Get selected package if provided
        selected_package = None
        package_id = request.args.get('package_id')
        if package_id:
            selected_package = crm_manager.get_package(package_id)
        
        # Generate HTML content for PDF
        html_content = render_template('client_packet_template.html', 
                                     client=client, 
                                     appointments=appointments,
                                     packages=packages,
                                     selected_package=selected_package,
                                     business=config_manager.get_business_info())
        
        # For now, return the HTML content (in production, you'd use a PDF library like WeasyPrint)
        return html_content, 200, {'Content-Type': 'text/html'}
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/clients/<client_id>')
@login_required
def get_client(client_id):
    """Get a specific client by ID"""
    try:
        client = crm_manager.get_client(client_id)
        if not client:
            return jsonify({'success': False, 'error': 'Client not found'}), 404
        
        return jsonify({
            'success': True,
            'client': client.to_dict()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/backup', methods=['POST'])
@login_required
def create_backup():
    """Create a complete system backup"""
    try:
        import json
        import os
        from datetime import datetime
        
        # Create backup directory if it doesn't exist
        backup_dir = os.path.join(os.getcwd(), 'backups')
        os.makedirs(backup_dir, exist_ok=True)
        
        # Generate backup filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f'gmail_notifications_backup_{timestamp}.json'
        backup_path = os.path.join(backup_dir, backup_filename)
        
        # Collect all system data
        backup_data = {
            'backup_info': {
                'created_at': datetime.now().isoformat(),
                'version': '1.0',
                'system': 'Gmail Notifications System'
            },
            'clients': [],
            'appointments': [],
            'baby_milestones': [],
            'birthday_sessions': [],
            'client_notes': [],
            'marketing_campaigns': [],
            'configuration': {},
            'session_types': [],
            'themes': [],
            'props': []
        }
        
        # Get clients data
        try:
            clients = crm_manager.get_all_clients()
            for client in clients:
                # Handle both Client objects and dictionaries
                if hasattr(client, 'id'):
                    # It's a Client object
                    backup_data['clients'].append({
                        'id': client.id,
                        'name': client.name,
                        'email': client.email,
                        'phone': client.phone,
                        'address': client.address,
                        'children_count': client.children_count,
                        'children_names': client.children_names,
                        'children_birth_dates': client.children_birth_dates,
                        'preferences': client.preferences,
                        'created_at': client.created_at.isoformat() if client.created_at else None,
                        'updated_at': client.updated_at.isoformat() if client.updated_at else None
                    })
                else:
                    # It's a dictionary
                    backup_data['clients'].append(client)
        except Exception as e:
            backup_data['clients'] = [{'error': f'Could not backup clients: {str(e)}'}]
        
        # Get appointments data
        try:
            appointments = appointment_scheduler.get_all_appointments()
            for appointment in appointments:
                # Handle both Appointment objects and dictionaries
                if hasattr(appointment, 'id'):
                    # It's an Appointment object
                    backup_data['appointments'].append({
                        'id': appointment.id,
                        'client_id': appointment.client_id,
                        'client_name': getattr(appointment, 'client_name', ''),
                        'client_email': getattr(appointment, 'client_email', ''),
                        'session_type': appointment.session_type,
                        'start_time': appointment.start_time.isoformat() if appointment.start_time else None,
                        'end_time': appointment.end_time.isoformat() if appointment.end_time else None,
                        'duration': appointment.duration,
                        'status': appointment.status,
                        'notes': appointment.notes,
                        'baby_name': getattr(appointment, 'baby_name', ''),
                        'baby_age_days': getattr(appointment, 'baby_age_days', None),
                        'session_fee': getattr(appointment, 'session_fee', 0),
                        'total_amount': getattr(appointment, 'total_amount', 0),
                        'payment_status': getattr(appointment, 'payment_status', ''),
                        'created_at': appointment.created_at.isoformat() if appointment.created_at else None
                    })
                else:
                    # It's a dictionary
                    backup_data['appointments'].append(appointment)
        except Exception as e:
            backup_data['appointments'] = [{'error': f'Could not backup appointments: {str(e)}'}]
        
        # Get configuration data
        try:
            config = config_manager.config
            backup_data['configuration'] = config
        except Exception as e:
            backup_data['configuration'] = {'error': f'Could not backup configuration: {str(e)}'}
        
        # Get session types and other data
        try:
            backup_data['session_types'] = [
                'Newborn Session', 'Milestone Session', 'Birthday Session', 
                'Family Session', 'Maternity Session', 'Cake Smash'
            ]
            backup_data['themes'] = [
                'Classic', 'Vintage', 'Modern', 'Rustic', 'Elegant', 'Playful', 'Seasonal'
            ]
            backup_data['props'] = [
                'Blankets', 'Baskets', 'Hats', 'Headbands', 'Toys', 'Flowers', 'Balloons'
            ]
        except Exception as e:
            backup_data['session_types'] = [{'error': f'Could not backup session types: {str(e)}'}]
        
        # Write backup to file
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, indent=2, ensure_ascii=False)
        
        return jsonify({
            'success': True, 
            'message': f'Backup created successfully!',
            'filename': backup_filename,
            'file_size': os.path.getsize(backup_path),
            'backup_path': backup_path
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/restore', methods=['POST'])
@login_required
def restore_backup():
    """Restore system from backup file"""
    try:
        import json
        import os
        
        if 'backup_file' not in request.files:
            return jsonify({'success': False, 'error': 'No backup file provided'}), 400
        
        backup_file = request.files['backup_file']
        if backup_file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        if not backup_file.filename.endswith('.json'):
            return jsonify({'success': False, 'error': 'Invalid file format. Please upload a JSON backup file.'}), 400
        
        # Read and parse backup file
        try:
            backup_data = json.load(backup_file)
        except json.JSONDecodeError:
            return jsonify({'success': False, 'error': 'Invalid JSON file. Please check your backup file.'}), 400
        
        # Validate backup structure
        required_keys = ['backup_info', 'clients', 'appointments', 'configuration']
        for key in required_keys:
            if key not in backup_data:
                return jsonify({'success': False, 'error': f'Invalid backup file. Missing required key: {key}'}), 400
        
        # Store backup data in session for confirmation
        session['restore_data'] = backup_data
        session['restore_filename'] = backup_file.filename
        
        return jsonify({
            'success': True,
            'message': 'Backup file loaded successfully. Please review and confirm the restore operation.',
            'backup_info': backup_data.get('backup_info', {}),
            'summary': {
                'clients': len(backup_data.get('clients', [])),
                'appointments': len(backup_data.get('appointments', [])),
                'configuration': 'Available' if backup_data.get('configuration') else 'Not available'
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/restore/confirm', methods=['POST'])
@login_required
def restore_backup_confirm():
    """Confirm and execute the restore operation"""
    try:
        if 'restore_data' not in session:
            return jsonify({'success': False, 'error': 'No restore data found. Please upload a backup file first.'}), 400
        
        restore_data = session['restore_data']
        restore_filename = session.get('restore_filename', 'Unknown')
        
        # Clear existing data (optional - could be made configurable)
        # This is a destructive operation, so we'll log it
        
        # Restore configuration
        try:
            if restore_data.get('configuration') and not restore_data['configuration'].get('error'):
                config_manager.update_config(restore_data['configuration'])
        except Exception as e:
            return jsonify({'success': False, 'error': f'Failed to restore configuration: {str(e)}'}), 500
        
        # Note: Full data restore would require database operations
        # For now, we'll just restore the configuration and provide guidance
        
        # Clear session data
        session.pop('restore_data', None)
        session.pop('restore_filename', None)
        
        return jsonify({
            'success': True,
            'message': f'Restore completed successfully from {restore_filename}! Configuration has been restored. Note: Full data restore requires database access.',
            'restored_items': ['Configuration']
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/backup/download/<filename>')
@login_required
def download_backup(filename):
    """Download a specific backup file"""
    try:
        import os
        from flask import send_file
        
        backup_dir = os.path.join(os.getcwd(), 'backups')
        backup_path = os.path.join(backup_dir, filename)
        
        if not os.path.exists(backup_path):
            return jsonify({'success': False, 'error': 'Backup file not found'}), 400
        
        return send_file(backup_path, as_attachment=True, download_name=filename)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/backup/list', methods=['GET'])
@login_required
def list_backups():
    """List all available backup files"""
    try:
        import os
        from datetime import datetime
        
        backup_dir = os.path.join(os.getcwd(), 'backups')
        if not os.path.exists(backup_dir):
            return jsonify({'success': True, 'backups': []})
        
        backups = []
        for filename in os.listdir(backup_dir):
            if filename.endswith('.json'):
                file_path = os.path.join(backup_dir, filename)
                file_stat = os.stat(file_path)
                backups.append({
                    'filename': filename,
                    'size': file_stat.st_size,
                    'created_at': datetime.fromtimestamp(file_stat.st_ctime).isoformat(),
                    'modified_at': datetime.fromtimestamp(file_stat.st_mtime).isoformat()
                })
        
        # Sort by creation date, newest first
        backups.sort(key=lambda x: x['created_at'], reverse=True)
        
        return jsonify({'success': True, 'backups': backups})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/backup/delete/<filename>', methods=['DELETE'])
@login_required
def delete_backup(filename):
    """Delete a specific backup file"""
    try:
        import os
        
        backup_dir = os.path.join(os.getcwd(), 'backups')
        backup_path = os.path.join(backup_dir, filename)
        
        if not os.path.exists(backup_path):
            return jsonify({'success': False, 'error': 'Backup file not found'}), 404
        
        # Security check - only allow deletion of JSON files in backups directory
        if not filename.endswith('.json') or not os.path.abspath(backup_path).startswith(os.path.abspath(backup_dir)):
            return jsonify({'success': False, 'error': 'Invalid file path'}), 400
        
        os.remove(backup_path)
        
        return jsonify({
            'success': True,
            'message': f'Backup file "{filename}" deleted successfully'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/appointments/<appointment_id>/export/ics')
@login_required
def export_appointment_ics(appointment_id):
    """Export a single appointment as ICS file"""
    try:
        appointment = appointment_scheduler.get_appointment(appointment_id)
        if not appointment:
            return jsonify({'error': 'Appointment not found'}), 404
        
        # Convert appointment to ICS format
        ics_generator = ICSGenerator(config_manager.get('business.name', 'Photography Business'))
        
        # Create appointment data for ICS
        appointment_data = {
            'client_name': appointment.client_name,
            'client_email': appointment.client_email,
            'session_type': appointment.session_type,
            'start_time': appointment.start_time,
            'duration': appointment.duration,
            'location': appointment.location,
            'status': appointment.status,
            'notes': appointment.notes,
            'special_instructions': appointment.special_instructions
        }
        
        ics_appointment = ics_generator.create_appointment_ics(appointment_data)
        
        # Generate filename
        filename = f"appointment_{appointment_id}_{appointment.start_time.strftime('%Y%m%d')}.ics"
        
        # Save ICS file
        filepath = ics_generator.save_ics_file([ics_appointment], filename)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'filepath': filepath,
            'message': 'ICS file generated successfully'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/appointments/export/ics')
@login_required
def export_all_appointments_ics():
    """Export all appointments as ICS file"""
    try:
        appointments = appointment_scheduler.get_all_appointments()
        if not appointments:
            return jsonify({'error': 'No appointments found'}), 404
        
        # Convert appointments to ICS format
        ics_generator = ICSGenerator(config_manager.get('business.name', 'Photography Business'))
        ics_appointments = []
        
        for appointment in appointments:
            appointment_data = {
                'client_name': appointment.client_name,
                'client_email': appointment.client_email,
                'session_type': appointment.session_type,
                'start_time': appointment.start_time,
                'duration': appointment.duration,
                'location': appointment.location,
                'status': appointment.status,
                'notes': appointment.notes,
                'special_instructions': appointment.special_instructions
            }
            
            ics_appointment = ics_generator.create_appointment_ics(appointment_data)
            ics_appointments.append(ics_appointment)
        
        # Generate filename
        filename = f"all_appointments_{datetime.now().strftime('%Y%m%d_%H%M%S')}.ics"
        
        # Save ICS file
        filepath = ics_generator.save_ics_file(ics_appointments, filename)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'filepath': filepath,
            'count': len(ics_appointments),
            'message': f'ICS file with {len(ics_appointments)} appointments generated successfully'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/appointments/export/ics/download/<filename>')
@login_required
def download_ics_file(filename):
    """Download an ICS file"""
    try:
        from flask import send_file
        
        filepath = os.path.join('exports', filename)
        
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(filepath, as_attachment=True, download_name=filename)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Package Management API Endpoints

@app.route('/api/packages', methods=['GET'])
@login_required
def get_packages():
    """Get all packages"""
    try:
        packages = crm_manager.get_all_packages()
        return jsonify({
            'success': True,
            'packages': [package.to_dict() for package in packages]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/packages/active', methods=['GET'])
@login_required
def get_active_packages():
    """Get all active packages"""
    try:
        packages = crm_manager.get_active_packages()
        return jsonify({
            'success': True,
            'packages': [package.to_dict() for package in packages]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/packages/category/<category>', methods=['GET'])
@login_required
def get_packages_by_category(category):
    """Get packages by category"""
    try:
        packages = crm_manager.get_packages_by_category(category)
        return jsonify({
            'success': True,
            'packages': [package.to_dict() for package in packages]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/packages/<package_id>', methods=['GET'])
@login_required
def get_package(package_id):
    """Get a specific package"""
    try:
        package = crm_manager.get_package(package_id)
        if not package:
            return jsonify({'success': False, 'error': 'Package not found'}), 404
        
        return jsonify({
            'success': True,
            'package': package.to_dict()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/packages', methods=['POST'])
@login_required
def create_package():
    """Create a new package"""
    try:
        data = request.get_json()
        
        # Create package from data
        package = Package(
            name=data.get('name', ''),
            description=data.get('description', ''),
            category=data.get('category', ''),
            base_price=float(data.get('base_price', 0.0)),
            duration_minutes=int(data.get('duration_minutes', 60)),
            is_customizable=data.get('is_customizable', True),
            includes=data.get('includes', []),
            add_ons=data.get('add_ons', []),
            requirements=data.get('requirements', []),
            recommended_age=data.get('recommended_age', ''),
            recommended_weeks=data.get('recommended_weeks', ''),
            optimal_timing=data.get('optimal_timing', ''),
            customizable_fields=data.get('customizable_fields', []),
            price_ranges=data.get('price_ranges', {}),
            is_active=data.get('is_active', True),
            is_featured=data.get('is_featured', False),
            display_order=int(data.get('display_order', 0))
        )
        
        success = crm_manager.add_package(package)
        if success:
            return jsonify({
                'success': True,
                'message': 'Package created successfully',
                'package': package.to_dict()
            })
        else:
            return jsonify({'success': False, 'error': 'Failed to create package'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/packages/<package_id>', methods=['PUT'])
@login_required
def update_package(package_id):
    """Update an existing package"""
    try:
        package = crm_manager.get_package(package_id)
        if not package:
            return jsonify({'success': False, 'error': 'Package not found'}), 404
        
        data = request.get_json()
        
        # Update package fields
        package.name = data.get('name', package.name)
        package.description = data.get('description', package.description)
        package.category = data.get('category', package.category)
        package.base_price = float(data.get('base_price', package.base_price))
        package.duration_minutes = int(data.get('duration_minutes', package.duration_minutes))
        package.is_customizable = data.get('is_customizable', package.is_customizable)
        package.includes = data.get('includes', package.includes)
        package.add_ons = data.get('add_ons', package.add_ons)
        package.requirements = data.get('requirements', package.requirements)
        package.recommended_age = data.get('recommended_age', package.recommended_age)
        package.recommended_weeks = data.get('recommended_weeks', package.recommended_weeks)
        package.optimal_timing = data.get('optimal_timing', package.optimal_timing)
        package.customizable_fields = data.get('customizable_fields', package.customizable_fields)
        package.price_ranges = data.get('price_ranges', package.price_ranges)
        package.is_active = data.get('is_active', package.is_active)
        package.is_featured = data.get('is_featured', package.is_featured)
        package.display_order = int(data.get('display_order', package.display_order))
        
        success = crm_manager.update_package(package)
        if success:
            return jsonify({
                'success': True,
                'message': 'Package updated successfully',
                'package': package.to_dict()
            })
        else:
            return jsonify({'success': False, 'error': 'Failed to update package'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/packages/<package_id>', methods=['DELETE'])
@login_required
def delete_package(package_id):
    """Delete a package"""
    try:
        success = crm_manager.delete_package(package_id)
        if success:
            return jsonify({
                'success': True,
                'message': 'Package deleted successfully'
            })
        else:
            return jsonify({'success': False, 'error': 'Failed to delete package'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

@app.route('/health')
def health_check():
    """Health check endpoint for container monitoring"""
    try:
        # Check database connection
        db.session.execute(text('SELECT 1'))
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'database': 'connected',
            'version': 'SnapStudio Containerized'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'timestamp': datetime.now().isoformat(),
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Initialize CRM database
        try:
            crm_manager._init_database()
            print("CRM database initialized successfully")
        except Exception as e:
            print(f"Warning: Could not initialize CRM database: {e}")
        
        # Create default admin user if none exists
        if not User.query.filter_by(username='admin').first():
            admin_user = User(username='admin', email='admin@example.com', role='admin')
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            db.session.commit()
            print("Default admin user created: username='admin', password='admin123'")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
