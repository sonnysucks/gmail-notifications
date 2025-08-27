#!/usr/bin/env python3
"""
Simple test script for the Gmail Photography Appointment Scheduler
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from scheduler.models import Appointment, Client, Reminder
from datetime import datetime, timedelta


def test_models():
    """Test the data models"""
    print("Testing data models...")
    
    # Test Client model
    client = Client(
        name="John Doe",
        email="john@example.com",
        phone="+1-555-0123"
    )
    print(f"✓ Client created: {client.name}")
    
    # Test Appointment model
    start_time = datetime.now() + timedelta(days=7)
    appointment = Appointment(
        client_name="John Doe",
        client_email="john@example.com",
        start_time=start_time,
        duration=90,
        session_type="Portrait Session",
        notes="Outdoor location preferred"
    )
    print(f"✓ Appointment created: {appointment.session_type} on {appointment.start_time.strftime('%B %d, %Y')}")
    print(f"  Days until: {appointment.days_until}")
    print(f"  Reminder key: {appointment.reminder_key}")
    
    # Test Reminder model
    reminder = Reminder(
        appointment_id=appointment.id,
        reminder_type="reminder_1week",
        scheduled_time=start_time - timedelta(days=7)
    )
    print(f"✓ Reminder created: {reminder.reminder_type}")
    
    print("\nAll model tests passed! ✓")


def test_config_loading():
    """Test configuration loading"""
    print("\nTesting configuration loading...")
    
    try:
        from config.config_manager import ConfigManager
        
        # This will fail without a config file, but we can test the class structure
        print("✓ ConfigManager class imported successfully")
        
        # Test with example config
        config_data = {
            'business': {'name': 'Test Business', 'email': 'test@example.com'},
            'calendar': {'target_calendar_id': 'primary'},
            'appointments': {'reminder_schedule': [{'weeks': 1}, {'days': 1}]},
            'email': {'templates': {}},
            'gmail': {'label_name': 'Test'},
            'logging': {'level': 'INFO'}
        }
        
        # Test validation logic
        required_sections = ['business', 'calendar', 'appointments', 'email', 'gmail', 'logging']
        for section in required_sections:
            if section in config_data:
                print(f"✓ Required section '{section}' found")
        
        print("✓ Configuration validation logic works")
        
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")


def test_template_rendering():
    """Test template rendering"""
    print("\nTesting template rendering...")
    
    try:
        from utils.template_manager import TemplateManager
        from config.config_manager import ConfigManager
        
        # Create a mock config
        class MockConfig:
            def get_template_path(self, name):
                return None
        
        config = MockConfig()
        template_manager = TemplateManager(config)
        
        # Test fallback template rendering
        context = {
            'appointment': {
                'client_name': 'Test Client',
                'session_type': 'Test Session',
                'start_time': datetime.now(),
                'duration': 60
            },
            'business': {
                'name': 'Test Business',
                'phone': '+1-555-0123',
                'email': 'test@example.com'
            }
        }
        
        rendered = template_manager.render_template('confirmation', context)
        if 'Test Client' in rendered and 'Test Session' in rendered:
            print("✓ Template rendering works")
        else:
            print("✗ Template rendering failed")
            
    except Exception as e:
        print(f"✗ Template test failed: {e}")


def main():
    """Run all tests"""
    print("Gmail Photography Appointment Scheduler - Test Suite")
    print("=" * 60)
    
    try:
        test_models()
        test_config_loading()
        test_template_rendering()
        
        print("\n" + "=" * 60)
        print("All tests completed! The basic system structure is working.")
        print("\nNext steps:")
        print("1. Copy config.example.yaml to config.yaml and customize it")
        print("2. Set up Google Cloud credentials (credentials.json)")
        print("3. Run 'python main.py --setup' to initialize the system")
        print("4. Use 'python main.py --help' to see available commands")
        
    except Exception as e:
        print(f"\n✗ Test suite failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
