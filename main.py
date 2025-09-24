#!/usr/bin/env python3
"""
Gmail Photography Appointment Scheduler with CRM
Specialized for Maternity, Baby, Smash Cake, and Birthday Photography
Main application entry point
"""

import click
import logging
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from config.config_manager import ConfigManager
from scheduler.appointment_scheduler import AppointmentScheduler
from gmail.gmail_manager import GmailManager
from calendar_integration.calendar_manager import CalendarManager
from utils.logger import setup_logging


@click.group()
@click.option('--config', '-c', default='config.yaml', help='Configuration file path')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
@click.pass_context
def cli(ctx, config, verbose):
    """Gmail Photography Appointment Scheduler with CRM - Specialized for Baby Photography"""
    ctx.ensure_object(dict)
    ctx.obj['config'] = config
    ctx.obj['verbose'] = verbose
    
    # Setup logging
    log_level = logging.DEBUG if verbose else logging.INFO
    setup_logging(log_level)
    
    # Load configuration
    try:
        config_manager = ConfigManager(config)
        ctx.obj['config_manager'] = config_manager
    except Exception as e:
        click.echo(f"Error loading configuration: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.pass_context
def setup(ctx):
    """Initial setup and authentication"""
    try:
        config_manager = ctx.obj['config_manager']
        
        # Initialize managers
        gmail_manager = GmailManager(config_manager)
        calendar_manager = CalendarManager(config_manager)
        
        click.echo("Setting up Gmail Baby Photography Appointment Scheduler with CRM...")
        
        # Authenticate with Google
        click.echo("Authenticating with Google...")
        gmail_manager.authenticate()
        calendar_manager.authenticate()
        
        # Create necessary labels and folders
        click.echo("Setting up Gmail labels...")
        gmail_manager.setup_labels()
        
        # Test calendar access
        click.echo("Testing calendar access...")
        calendar_manager.test_access()
        
        # Initialize CRM database
        click.echo("Initializing CRM database...")
        from scheduler.crm_manager import CRMManager
        crm_manager = CRMManager(config_manager)
        
        click.echo("Setup completed successfully!")
        click.echo("You can now use the scheduler to manage baby photography appointments and clients.")
        
    except Exception as e:
        click.echo(f"Setup failed: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('client_name')
@click.argument('datetime')
@click.argument('session_type')
@click.option('--duration', '-d', default=None, help='Duration in minutes')
@click.option('--notes', '-n', help='Additional notes')
@click.option('--email', '-e', help='Client email address')
@click.option('--fee', '-f', type=float, help='Session fee')
@click.option('--location', '-l', help='Session location')
@click.option('--priority', '-p', default='normal', help='Priority (low, normal, high, urgent)')
@click.option('--baby-name', help='Baby/child name for the session')
@click.option('--baby-age-days', type=int, help='Baby age in days')
@click.option('--milestone-type', help='Milestone type (newborn, 3month, 6month, etc.)')
@click.option('--parent-names', help='Parent names (comma-separated)')
@click.option('--siblings', help='Sibling names (comma-separated)')
@click.pass_context
def schedule(ctx, client_name, datetime, session_type, duration, notes, email, fee, location, priority, baby_name, baby_age_days, milestone_type, parent_names, siblings):
    """Schedule a new baby photography appointment"""
    try:
        config_manager = ctx.obj['config_manager']
        scheduler = AppointmentScheduler(config_manager)
        
        click.echo(f"Scheduling {session_type} appointment for {client_name}...")
        
        # Parse additional fields
        parent_list = [p.strip() for p in parent_names.split(',')] if parent_names else []
        sibling_list = [s.strip() for s in siblings.split(',')] if siblings else []
        
        appointment = scheduler.create_appointment(
            client_name=client_name,
            datetime_str=datetime,
            session_type=session_type,
            duration=duration,
            notes=notes or "",
            client_email=email or "",
            session_fee=fee or 0.0,
            location=location or "",
            priority=priority,
            baby_name=baby_name or "",
            baby_age_days=baby_age_days,
            milestone_type=milestone_type or "",
            parent_names=parent_list,
            siblings_included=len(sibling_list) > 0,
            sibling_names=sibling_list
        )
        
        click.echo(f"Appointment scheduled successfully!")
        click.echo(f"ID: {appointment.id}")
        click.echo(f"Date: {appointment.start_time}")
        click.echo(f"Duration: {appointment.duration} minutes")
        click.echo(f"Client ID: {appointment.client_id}")
        if baby_name:
            click.echo(f"Baby/Child: {baby_name}")
        if milestone_type:
            click.echo(f"Milestone: {milestone_type}")
        
    except Exception as e:
        click.echo(f"Failed to schedule appointment: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.pass_context
def reminders(ctx):
    """Run the reminder service to send notifications"""
    try:
        config_manager = ctx.obj['config_manager']
        scheduler = AppointmentScheduler(config_manager)
        
        click.echo("Running reminder service...")
        sent_count = scheduler.send_reminders()
        
        click.echo(f"Reminder service completed. Sent {sent_count} reminders.")
        
    except Exception as e:
        click.echo(f"Reminder service failed: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--days', '-d', default=30, help='Number of days to look ahead')
@click.pass_context
def list(ctx, days):
    """List upcoming appointments"""
    try:
        config_manager = ctx.obj['config_manager']
        scheduler = AppointmentScheduler(config_manager)
        
        appointments = scheduler.get_upcoming_appointments(days)
        
        if not appointments:
            click.echo("No upcoming appointments found.")
            return
        
        click.echo(f"Upcoming appointments (next {days} days):")
        click.echo("-" * 80)
        
        for apt in appointments:
            click.echo(f"{apt.start_time.strftime('%Y-%m-%d %H:%M')} - {apt.client_name}")
            click.echo(f"  Session: {apt.session_type}")
            click.echo(f"  Duration: {apt.duration} minutes")
            if apt.baby_name:
                click.echo(f"  Baby/Child: {apt.baby_name}")
            if apt.milestone_type:
                click.echo(f"  Milestone: {apt.milestone_type}")
            if apt.notes:
                click.echo(f"  Notes: {apt.notes}")
            click.echo()
        
    except Exception as e:
        click.echo(f"Failed to list appointments: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.pass_context
def sync(ctx):
    """Sync appointments from Gmail to calendar"""
    try:
        config_manager = ctx.obj['config_manager']
        gmail_manager = GmailManager(config_manager)
        scheduler = AppointmentScheduler(config_manager)
        
        click.echo("Syncing appointments from Gmail...")
        
        # Scan Gmail for appointment emails
        emails = gmail_manager.scan_for_appointments()
        
        if not emails:
            click.echo("No new appointment emails found.")
            return
        
        click.echo(f"Found {len(emails)} potential appointment emails.")
        
        # Process each email
        processed = 0
        for email in emails:
            try:
                appointment = scheduler.process_email_appointment(email)
                if appointment:
                    processed += 1
                    click.echo(f"Processed appointment for {appointment.client_name}")
            except Exception as e:
                click.echo(f"Failed to process email {email['id']}: {e}")
        
        click.echo(f"Sync completed. Processed {processed} appointments.")
        
    except Exception as e:
        click.echo(f"Sync failed: {e}", err=True)
        sys.exit(1)


# CRM Commands
@cli.group()
def crm():
    """Customer Relationship Management commands"""
    pass


@crm.command()
@click.argument('query')
@click.option('--limit', '-l', default=20, help='Maximum number of results')
@click.pass_context
def search(ctx, query, limit):
    """Search for clients"""
    try:
        config_manager = ctx.obj['config_manager']
        scheduler = AppointmentScheduler(config_manager)
        
        click.echo(f"Searching for clients matching '{query}'...")
        clients = scheduler.search_clients(query, limit)
        
        if not clients:
            click.echo("No clients found.")
            return
        
        click.echo(f"Found {len(clients)} clients:")
        click.echo("-" * 80)
        
        for client in clients:
            click.echo(f"ID: {client.id}")
            click.echo(f"Name: {client.name}")
            click.echo(f"Email: {client.email}")
            click.echo(f"Phone: {client.phone}")
            click.echo(f"Family Type: {client.family_type}")
            if client.due_date:
                days_until = client.get_days_until_due()
                if days_until:
                    click.echo(f"Due Date: {client.due_date.strftime('%Y-%m-%d')} ({days_until} days)")
                else:
                    click.echo(f"Due Date: {client.due_date.strftime('%Y-%m-%d')} (Overdue)")
            click.echo(f"Total Appointments: {client.total_appointments}")
            click.echo(f"Total Spent: ${client.total_spent:.2f}")
            if client.tags:
                click.echo(f"Tags: {', '.join(client.tags)}")
            click.echo("-" * 40)
        
    except Exception as e:
        click.echo(f"Search failed: {e}", err=True)
        sys.exit(1)


@crm.command()
@click.argument('client_id')
@click.pass_context
def client(ctx, client_id):
    """Get detailed client information"""
    try:
        config_manager = ctx.obj['config_manager']
        scheduler = AppointmentScheduler(config_manager)
        
        click.echo(f"Getting details for client {client_id}...")
        client = scheduler.get_client_details(client_id)
        
        if not client:
            click.echo("Client not found.")
            return
        
        click.echo("Client Details:")
        click.echo("=" * 50)
        click.echo(f"ID: {client.id}")
        click.echo(f"Name: {client.name}")
        click.echo(f"Email: {client.email}")
        click.echo(f"Phone: {client.phone}")
        click.echo(f"Address: {client.address}")
        click.echo(f"Company: {client.company}")
        click.echo(f"Website: {client.website}")
        click.echo(f"Family Type: {client.family_type}")
        if client.due_date:
            days_until = client.get_days_until_due()
            if days_until:
                click.echo(f"Due Date: {client.due_date.strftime('%Y-%m-%d')} ({days_until} days)")
            else:
                click.echo(f"Due Date: {client.due_date.strftime('%Y-%m-%d')} (Overdue)")
        click.echo(f"Family Size: {client.family_size}")
        if client.children_info:
            click.echo(f"Children: {', '.join(client.get_children_names())}")
        click.echo(f"Previous Photographer: {client.previous_photographer}")
        click.echo(f"Photography Experience: {client.photography_experience}")
        click.echo(f"Referral Source: {client.referral_source}")
        click.echo(f"Tags: {', '.join(client.tags) if client.tags else 'None'}")
        click.echo(f"Total Appointments: {client.total_appointments}")
        click.echo(f"Total Spent: ${client.total_spent:.2f}")
        click.echo(f"Average Session Value: ${client.average_session_value:.2f}")
        click.echo(f"Customer Lifetime Value: ${client.customer_lifetime_value:.2f}")
        click.echo(f"Created: {client.created_at.strftime('%Y-%m-%d')}")
        click.echo(f"Last Contact: {client.last_contact.strftime('%Y-%m-%d') if client.last_contact else 'Never'}")
        click.echo(f"Last Appointment: {client.last_appointment.strftime('%Y-%m-%d') if client.last_appointment else 'Never'}")
        
        if client.notes:
            click.echo(f"\nNotes: {client.notes}")
        
    except Exception as e:
        click.echo(f"Failed to get client details: {e}", err=True)
        sys.exit(1)


@crm.command()
@click.argument('client_id')
@click.argument('note_content')
@click.option('--title', '-t', help='Note title')
@click.option('--type', '--note-type', default='general', help='Note type (general, follow_up, marketing, internal)')
@click.option('--author', '-a', default='System', help='Note author')
@click.option('--internal', '-i', is_flag=True, help='Mark as internal note')
@click.pass_context
def add_note(ctx, client_id, note_content, title, type, author, internal):
    """Add a note to a client"""
    try:
        config_manager = ctx.obj['config_manager']
        scheduler = AppointmentScheduler(config_manager)
        
        click.echo(f"Adding note to client {client_id}...")
        
        success = scheduler.add_client_note(
            client_id=client_id,
            note_content=note_content,
            note_type=type,
            title=title or "",
            author=author,
            internal=internal
        )
        
        if success:
            click.echo("Note added successfully!")
        else:
            click.echo("Failed to add note.")
            sys.exit(1)
        
    except Exception as e:
        click.echo(f"Failed to add note: {e}", err=True)
        sys.exit(1)


@crm.command()
@click.pass_context
def analytics(ctx):
    """Get CRM analytics and insights"""
    try:
        config_manager = ctx.obj['config_manager']
        scheduler = AppointmentScheduler(config_manager)
        
        click.echo("Getting CRM analytics...")
        analytics = scheduler.get_crm_analytics()
        
        if not analytics:
            click.echo("No analytics data available.")
            return
        
        click.echo("CRM Analytics:")
        click.echo("=" * 50)
        click.echo(f"Total Clients: {analytics.get('total_clients', 0)}")
        click.echo(f"New Clients This Month: {analytics.get('new_clients_month', 0)}")
        click.echo(f"Total Appointments: {analytics.get('total_appointments', 0)}")
        click.echo(f"Appointments This Month: {analytics.get('appointments_month', 0)}")
        click.echo(f"Total Revenue: ${analytics.get('total_revenue', 0):.2f}")
        click.echo(f"Monthly Revenue: ${analytics.get('monthly_revenue', 0):.2f}")
        click.echo(f"Average Session Value: ${analytics.get('average_session_value', 0):.2f}")
        
        if analytics.get('top_referral_sources'):
            click.echo(f"\nTop Referral Sources:")
            for source, count in analytics['top_referral_sources'].items():
                click.echo(f"  {source}: {count}")
        
        if analytics.get('tag_distribution'):
            click.echo(f"\nClient Tag Distribution:")
            for tag, count in analytics['tag_distribution'].items():
                click.echo(f"  {tag}: {count}")
        
        if analytics.get('payment_status_distribution'):
            click.echo(f"\nPayment Status Distribution:")
            for status, count in analytics['payment_status_distribution'].items():
                click.echo(f"  {status}: {count}")
        
    except Exception as e:
        click.echo(f"Failed to get analytics: {e}", err=True)
        sys.exit(1)


@crm.command()
@click.pass_context
def follow_ups(ctx):
    """List follow-up tasks that need attention"""
    try:
        config_manager = ctx.obj['config_manager']
        scheduler = AppointmentScheduler(config_manager)
        
        click.echo("Getting follow-up tasks...")
        follow_ups = scheduler.get_follow_up_tasks()
        
        if not follow_ups:
            click.echo("No follow-up tasks found.")
            return
        
        click.echo(f"Found {len(follow_ups)} follow-up tasks:")
        click.echo("-" * 80)
        
        for task in follow_ups:
            click.echo(f"Appointment ID: {task['appointment_id']}")
            click.echo(f"Client: {task['client_name']}")
            click.echo(f"Notes: {task['follow_up_notes']}")
            click.echo(f"Appointment Date: {task['appointment_date']}")
            click.echo(f"Contact: {task['client_email']} / {task['client_phone']}")
            click.echo("-" * 40)
        
    except Exception as e:
        click.echo(f"Failed to get follow-up tasks: {e}", err=True)
        sys.exit(1)


# Baby Photography Specific Commands
@cli.group()
def baby():
    """Baby photography specific commands"""
    pass


@baby.command()
@click.argument('client_id')
@click.argument('baby_name')
@click.argument('birth_date')
@click.option('--notes', '-n', help='Additional notes about the baby')
@click.pass_context
def add_baby(ctx, client_id, baby_name, birth_date, notes):
    """Add baby information to a client"""
    try:
        config_manager = ctx.obj['config_manager']
        scheduler = AppointmentScheduler(config_manager)
        
        # Parse birth date
        from datetime import datetime
        try:
            parsed_birth_date = datetime.strptime(birth_date, '%Y-%m-%d')
        except ValueError:
            click.echo("Invalid date format. Use YYYY-MM-DD")
            sys.exit(1)
        
        click.echo(f"Adding baby {baby_name} to client {client_id}...")
        
        # Get client details
        client = scheduler.get_client_details(client_id)
        if not client:
            click.echo("Client not found.")
            sys.exit(1)
        
        # Add baby to client
        baby_info = {
            'name': baby_name,
            'birth_date': parsed_birth_date.isoformat(),
            'notes': notes or "",
            'added_at': datetime.now().isoformat()
        }
        
        client.add_child(baby_info)
        success = scheduler.crm_manager.update_client(client)
        
        if success:
            click.echo(f"Baby {baby_name} added successfully!")
            click.echo(f"Birth Date: {parsed_birth_date.strftime('%Y-%m-%d')}")
            click.echo(f"Family Size: {client.family_size}")
        else:
            click.echo("Failed to add baby.")
            sys.exit(1)
        
    except Exception as e:
        click.echo(f"Failed to add baby: {e}", err=True)
        sys.exit(1)


@baby.command()
@click.argument('client_id')
@click.pass_context
def milestones(ctx, client_id):
    """List upcoming milestones for a client's babies"""
    try:
        config_manager = ctx.obj['config_manager']
        scheduler = AppointmentScheduler(config_manager)
        
        click.echo(f"Getting milestones for client {client_id}...")
        
        # Get client details
        client = scheduler.get_client_details(client_id)
        if not client:
            click.echo("Client not found.")
            sys.exit(1)
        
        if not client.children_info:
            click.echo("No children found for this client.")
            return
        
        click.echo(f"Milestones for {client.name}:")
        click.echo("=" * 50)
        
        for child in client.children_info:
            if 'birth_date' in child and child['birth_date']:
                from datetime import datetime
                birth_date = datetime.fromisoformat(child['birth_date'])
                now = datetime.now()
                age_days = (now - birth_date).days
                
                click.echo(f"\nChild: {child.get('name', 'Unknown')}")
                click.echo(f"Birth Date: {birth_date.strftime('%Y-%m-%d')}")
                click.echo(f"Current Age: {age_days} days ({age_days // 7} weeks, {age_days // 30} months)")
                
                # Calculate next milestone
                if age_days < 14:
                    next_milestone = "Newborn (0-14 days)"
                    days_until = 14 - age_days
                elif age_days < 90:
                    next_milestone = "3 Month (90 days)"
                    days_until = 90 - age_days
                elif age_days < 180:
                    next_milestone = "6 Month (180 days)"
                    days_until = 180 - age_days
                elif age_days < 270:
                    next_milestone = "9 Month (270 days)"
                    days_until = 270 - age_days
                elif age_days < 365:
                    next_milestone = "1 Year (365 days)"
                    days_until = 365 - age_days
                else:
                    next_milestone = "Older than 1 year"
                    days_until = 0
                
                if days_until > 0:
                    click.echo(f"Next Milestone: {next_milestone} (in {days_until} days)")
                else:
                    click.echo(f"Next Milestone: {next_milestone}")
        
    except Exception as e:
        click.echo(f"Failed to get milestones: {e}", err=True)
        sys.exit(1)


@baby.command()
@click.argument('client_id')
@click.option('--due-date', help='Due date (YYYY-MM-DD)')
@click.option('--family-type', help='Family type (expecting, newborn, baby, toddler)')
@click.option('--photography-experience', help='Photography experience level')
@click.pass_context
def update_family(ctx, client_id, due_date, family_type, photography_experience):
    """Update family information for a client"""
    try:
        config_manager = ctx.obj['config_manager']
        scheduler = AppointmentScheduler(config_manager)
        
        click.echo(f"Updating family information for client {client_id}...")
        
        # Get client details
        client = scheduler.get_client_details(client_id)
        if not client:
            click.echo("Client not found.")
            sys.exit(1)
        
        # Update fields
        if due_date:
            from datetime import datetime
            try:
                parsed_due_date = datetime.strptime(due_date, '%Y-%m-%d')
                client.due_date = parsed_due_date
                click.echo(f"Due date updated to: {parsed_due_date.strftime('%Y-%m-%d')}")
            except ValueError:
                click.echo("Invalid date format. Use YYYY-MM-DD")
                sys.exit(1)
        
        if family_type:
            client.family_type = family_type
            click.echo(f"Family type updated to: {family_type}")
        
        if photography_experience:
            client.photography_experience = photography_experience
            click.echo(f"Photography experience updated to: {photography_experience}")
        
        # Save changes
        success = scheduler.crm_manager.update_client(client)
        
        if success:
            click.echo("Family information updated successfully!")
        else:
            click.echo("Failed to update family information.")
            sys.exit(1)
        
    except Exception as e:
        click.echo(f"Failed to update family information: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('appointment_id')
@click.argument('reason')
@click.pass_context
def cancel(ctx, appointment_id, reason):
    """Cancel an appointment"""
    try:
        config_manager = ctx.obj['config_manager']
        scheduler = AppointmentScheduler(config_manager)
        
        click.echo(f"Cancelling appointment {appointment_id}...")
        
        success = scheduler.cancel_appointment(appointment_id, reason)
        
        if success:
            click.echo("Appointment cancelled successfully!")
        else:
            click.echo("Failed to cancel appointment.")
            sys.exit(1)
        
    except Exception as e:
        click.echo(f"Failed to cancel appointment: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    cli()
