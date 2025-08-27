#!/usr/bin/env python3
"""
Standalone script to run appointment reminders
Can be used with cron jobs for automated reminder sending
"""

import sys
import logging
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from config.config_manager import ConfigManager
from scheduler.appointment_scheduler import AppointmentScheduler
from utils.logger import setup_logging


def main():
    """Run the reminder service"""
    try:
        # Setup logging
        setup_logging(
            level=logging.INFO,
            log_file='logs/reminders.log'
        )
        
        logger = logging.getLogger(__name__)
        logger.info("Starting reminder service...")
        
        # Load configuration
        config_manager = ConfigManager('config.yaml')
        
        # Initialize scheduler
        scheduler = AppointmentScheduler(config_manager)
        
        # Send reminders
        sent_count = scheduler.send_reminders()
        
        logger.info(f"Reminder service completed. Sent {sent_count} reminders.")
        
        # Exit with success code
        sys.exit(0)
        
    except FileNotFoundError:
        print("Error: config.yaml not found. Please copy config.example.yaml to config.yaml and customize it.")
        sys.exit(1)
    except Exception as e:
        print(f"Error running reminder service: {e}")
        if 'logger' in locals():
            logger.error(f"Reminder service failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
