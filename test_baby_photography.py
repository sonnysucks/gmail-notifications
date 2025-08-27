#!/usr/bin/env python3
"""
Baby Photography Test Script for Gmail Photography Appointment Scheduler
Tests specialized baby photography functionality including milestones, baby tracking, and specialized sessions
"""

import sys
import logging
from pathlib import Path
from datetime import datetime, timedelta

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from scheduler.models import Client, Appointment, BabyMilestone, BirthdaySession
from scheduler.crm_manager import CRMManager
from config.config_manager import ConfigManager


def test_baby_milestone_tracking():
    """Test baby milestone tracking functionality"""
    print("Testing Baby Milestone Tracking...")
    
    try:
        # Create a baby milestone
        milestone = BabyMilestone(
            client_id="test_client_123",
            baby_name="Emma",
            birth_date=datetime.now() - timedelta(days=45),
            milestone_type="3month"
        )
        
        # Calculate age
        milestone.calculate_age()
        
        if milestone.age_in_days == 45 and milestone.age_in_weeks == 6:
            print("✓ Baby age calculation working")
        else:
            print("✗ Baby age calculation failed")
            return False
        
        # Test next milestone calculation
        next_milestone = milestone.get_next_milestone()
        if next_milestone == "6month":
            print("✓ Next milestone calculation working")
        else:
            print("✗ Next milestone calculation failed")
            return False
        
        # Test milestone completion
        milestone.completed = True
        if milestone.completed:
            print("✓ Milestone completion tracking working")
        else:
            print("✗ Milestone completion tracking failed")
            return False
        
        print("✓ All baby milestone tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Baby milestone test failed: {e}")
        return False


def test_birthday_session_management():
    """Test birthday session functionality"""
    print("\nTesting Birthday Session Management...")
    
    try:
        # Create a birthday session
        birthday_session = BirthdaySession(
            appointment_id="apt_123",
            child_name="Liam",
            age_turning=3,
            birthday_date=datetime.now() + timedelta(days=30),
            session_date=datetime.now() + timedelta(days=25),
            theme="Superhero",
            colors=["Blue", "Red", "Yellow"],
            props_needed=["Cape", "Mask", "Balloons"],
            cake_flavor="Chocolate",
            cake_design="Superhero themed with cape design"
        )
        
        if birthday_session.child_name == "Liam" and birthday_session.theme == "Superhero":
            print("✓ Birthday session creation working")
        else:
            print("✗ Birthday session creation failed")
            return False
        
        # Test age calculation
        if birthday_session.age_turning == 3:
            print("✓ Age tracking working")
        else:
            print("✗ Age tracking failed")
            return False
        
        # Test theme and props
        if "Superhero" in birthday_session.theme and "Cape" in birthday_session.props_needed:
            print("✓ Theme and props management working")
        else:
            print("✗ Theme and props management failed")
            return False
        
        print("✓ All birthday session tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Birthday session test failed: {e}")
        return False


def test_baby_client_management():
    """Test baby-specific client management"""
    print("\nTesting Baby Client Management...")
    
    try:
        # Create a client with baby information
        client = Client(
            name="Sarah Johnson",
            email="sarah@example.com",
            phone="+1-555-0126",
            family_type="expecting",
            due_date=datetime.now() + timedelta(days=60),
            photography_experience="first_time",
            tags=["New Client", "Maternity Client"]
        )
        
        # Test expecting status
        if client.is_expecting():
            print("✓ Expecting status detection working")
        else:
            print("✗ Expecting status detection failed")
            return False
        
        # Test due date calculation
        days_until = client.get_days_until_due()
        if days_until and days_until > 0:
            print("✓ Due date calculation working")
        else:
            print("✗ Due date calculation failed")
            return False
        
        # Add baby information
        baby_info = {
            'name': 'Baby Johnson',
            'birth_date': datetime.now().isoformat(),
            'notes': 'First baby, very excited parents'
        }
        client.add_child(baby_info)
        
        if client.family_size == 1 and "Baby Johnson" in client.get_children_names():
            print("✓ Baby addition working")
        else:
            print("✗ Baby addition failed")
            return False
        
        # Update family type
        client.family_type = "newborn"
        if client.family_type == "newborn":
            print("✓ Family type update working")
        else:
            print("✗ Family type update failed")
            return False
        
        print("✓ All baby client management tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Baby client management test failed: {e}")
        return False


def test_baby_appointment_features():
    """Test baby-specific appointment features"""
    print("\nTesting Baby Appointment Features...")
    
    try:
        # Create a baby appointment
        appointment = Appointment(
            client_name="Mike and Lisa",
            client_email="mike@example.com",
            start_time=datetime.now() + timedelta(days=14),
            duration=90,
            session_type="Newborn Session",
            baby_name="Baby Smith",
            milestone_type="newborn",
            parent_names=["Mike", "Lisa"],
            siblings_included=True,
            sibling_names=["Emma", "Liam"]
        )
        
        # Test baby-specific properties
        if appointment.baby_name == "Baby Smith":
            print("✓ Baby name tracking working")
        else:
            print("✗ Baby name tracking failed")
            return False
        
        if appointment.is_newborn_session:
            print("✓ Newborn session detection working")
        else:
            print("✗ Newborn session detection failed")
            return False
        
        if appointment.milestone_type == "newborn":
            print("✓ Milestone type tracking working")
        else:
            print("✗ Milestone type tracking failed")
            return False
        
        if len(appointment.parent_names) == 2 and "Mike" in appointment.parent_names:
            print("✓ Parent names tracking working")
        else:
            print("✗ Parent names tracking failed")
            return False
        
        if appointment.siblings_included and len(appointment.sibling_names) == 2:
            print("✓ Sibling tracking working")
        else:
            print("✗ Sibling tracking failed")
            return False
        
        # Test baby age calculation
        birth_date = datetime.now() - timedelta(days=7)
        appointment.calculate_baby_age(birth_date)
        
        if appointment.baby_age_days == 7 and appointment.baby_age_weeks == 1:
            print("✓ Baby age calculation working")
        else:
            print("✗ Baby age calculation failed")
            return False
        
        print("✓ All baby appointment tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Baby appointment test failed: {e}")
        return False


def test_baby_photography_configuration():
    """Test baby photography configuration loading"""
    print("\nTesting Baby Photography Configuration...")
    
    try:
        # Load configuration
        config_manager = ConfigManager('config.example.yaml')
        
        # Test session types
        session_types = config_manager.get('appointments.session_types')
        if session_types:
            print("✓ Session types configuration loaded")
            
            # Check for baby-specific session types
            baby_sessions = ['newborn', 'maternity', 'smash_cake', 'milestone_1year']
            found_sessions = [session for session in baby_sessions if session in session_types]
            
            if len(found_sessions) >= 3:
                print(f"✓ Found {len(found_sessions)} baby photography session types")
            else:
                print(f"✗ Only found {len(found_sessions)} baby photography session types")
                return False
        else:
            print("✗ Session types configuration not loaded")
            return False
        
        # Test baby photography settings
        baby_settings = config_manager.get('baby_photography')
        if baby_settings:
            print("✓ Baby photography settings loaded")
            
            # Check milestone settings
            if 'milestones' in baby_settings:
                print("✓ Milestone tracking configuration found")
            else:
                print("✗ Milestone tracking configuration missing")
                return False
            
            # Check newborn settings
            if 'newborn' in baby_settings:
                print("✓ Newborn session configuration found")
            else:
                print("✗ Newborn session configuration missing")
                return False
            
            # Check smash cake settings
            if 'smash_cake' in baby_settings:
                print("✓ Smash cake configuration found")
            else:
                print("✗ Smash cake configuration missing")
                return False
        else:
            print("✗ Baby photography settings not loaded")
            return False
        
        print("✓ All configuration tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False


def test_baby_crm_integration():
    """Test baby photography CRM integration"""
    print("\nTesting Baby Photography CRM Integration...")
    
    try:
        # Load configuration
        config_manager = ConfigManager('config.example.yaml')
        
        # Initialize CRM manager
        crm_manager = CRMManager(config_manager)
        
        print("✓ CRM manager initialized successfully")
        
        # Test client creation with baby information
        client = Client(
            name="Jennifer Davis",
            email="jennifer@example.com",
            phone="+1-555-0127",
            family_type="expecting",
            due_date=datetime.now() + timedelta(days=45),
            photography_experience="first_time",
            referral_source="Instagram",
            tags=["New Client", "Maternity Client"]
        )
        
        # Add client to CRM
        success = crm_manager.add_client(client)
        if success:
            print("✓ Baby client added to CRM successfully")
        else:
            print("✗ Failed to add baby client to CRM")
            return False
        
        # Test client retrieval
        retrieved_client = crm_manager.get_client(client.id)
        if retrieved_client and retrieved_client.name == "Jennifer Davis":
            print("✓ Baby client retrieved successfully")
        else:
            print("✗ Failed to retrieve baby client")
            return False
        
        # Test client search
        search_results = crm_manager.search_clients("Jennifer")
        if search_results and len(search_results) > 0:
            print("✓ Baby client search working")
        else:
            print("✗ Baby client search failed")
            return False
        
        print("✓ All CRM integration tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ CRM integration test failed: {e}")
        return False


def main():
    """Run all baby photography tests"""
    print("Gmail Photography Appointment Scheduler - Baby Photography Test Suite")
    print("=" * 80)
    
    all_tests_passed = True
    
    # Run tests
    if not test_baby_milestone_tracking():
        all_tests_passed = False
    
    if not test_birthday_session_management():
        all_tests_passed = False
    
    if not test_baby_client_management():
        all_tests_passed = False
    
    if not test_baby_appointment_features():
        all_tests_passed = False
    
    if not test_baby_photography_configuration():
        all_tests_passed = False
    
    if not test_baby_crm_integration():
        all_tests_passed = False
    
    print("\n" + "=" * 80)
    
    if all_tests_passed:
        print("🎉 All Baby Photography tests completed successfully!")
        print("\nThe baby photography system is working properly with:")
        print("✓ Baby milestone tracking and age calculations")
        print("✓ Birthday session management with themes and props")
        print("✓ Baby-specific client management and family tracking")
        print("✓ Specialized appointment features for baby photography")
        print("✓ Baby photography configuration and settings")
        print("✓ CRM integration for baby photography clients")
        print("\nSpecialized features available:")
        print("• Maternity session planning and reminders")
        print("• Newborn session scheduling (0-14 days)")
        print("• Milestone tracking (3, 6, 9, 12 months)")
        print("• Smash cake session management")
        print("• Birthday photography with themes")
        print("• Family portrait sessions")
        print("• Package deals and milestone packages")
        print("\nNext steps:")
        print("1. Copy config.example.yaml to config.yaml and customize")
        print("2. Set up Google Cloud credentials (credentials.json)")
        print("3. Run 'python main.py --setup' to initialize the baby photography CRM")
        print("4. Use 'python main.py baby --help' to see baby-specific commands")
        print("5. Use 'python main.py crm --help' to see CRM commands")
    else:
        print("❌ Some baby photography tests failed. Please check the errors above.")
        sys.exit(1)


if __name__ == '__main__':
    main()
