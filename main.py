#!/usr/bin/env python3
"""
Gmail Photography Appointment Scheduler
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
from calendar.calendar_manager import CalendarManager
from utils.logger import setup_logging


@click.group()
@click.option('--config', '-c', default='config.yaml', help='Configuration file path')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
@click.pass_context
def cli(ctx, config, verbose):
    """Gmail Photography Appointment Scheduler"""
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
        
        click.echo("Setting up Gmail Photography Appointment Scheduler...")
        
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
        
        click.echo("Setup completed successfully!")
        click.echo("You can now use the scheduler to manage appointments.")
        
    except Exception as e:
        click.echo(f"Setup failed: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('client_name')
@click.argument('datetime')
@click.argument('session_type')
@click.option('--duration', '-d', default=None, help='Duration in minutes')
@click.option('--notes', '-n', help='Additional notes')
@click.pass_context
def schedule(ctx, client_name, datetime, session_type, duration, notes):
    """Schedule a new appointment"""
    try:
        config_manager = ctx.obj['config_manager']
        scheduler = AppointmentScheduler(config_manager)
        
        click.echo(f"Scheduling appointment for {client_name}...")
        
        appointment = scheduler.create_appointment(
            client_name=client_name,
            datetime_str=datetime,
            session_type=session_type,
            duration=duration,
            notes=notes
        )
        
        click.echo(f"Appointment scheduled successfully!")
        click.echo(f"ID: {appointment.id}")
        click.echo(f"Date: {appointment.start_time}")
        click.echo(f"Duration: {appointment.duration} minutes")
        
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
                click.echo(f"Failed to process email {email.id}: {e}")
        
        click.echo(f"Sync completed. Processed {processed} appointments.")
        
    except Exception as e:
        click.echo(f"Sync failed: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    cli()
