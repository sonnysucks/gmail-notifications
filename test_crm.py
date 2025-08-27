#!/usr/bin/env python3
"""
CRM Test Script for Gmail Photography Appointment Scheduler
Tests the CRM functionality and database operations
"""

import sys
import logging
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from scheduler.models import Client, Appointment, ClientNote, MarketingCampaign
from scheduler.crm_manager import CRMManager
from config.config_manager import ConfigManager
from datetime import datetime, timedelta


def test_crm_database():
    """Test CRM database operations"""
    print("Testing CRM Database Operations...")
    
    try:
        # Create config manager
        config_manager = ConfigManager('config.example.yaml')
        
        # Initialize CRM manager
        crm_manager = CRMManager(config_manager)
        
        print("✓ CRM database initialized successfully")
        
        # Test client creation
        test_client = Client(
            name="Jane Smith",
            email="jane.smith@example.com",
            phone="+1-555-0124",
            address="456 Oak Street",
            city="Springfield",
            state="IL",
            zip_code="62701",
            company="Smith Photography",
            website="https://smithphotography.com",
            referral_source="Google Search",
            tags=["New Client", "Portrait Client"],
            industry="Photography",
            budget_range="$500-1000",
            project_type="Personal"
        )
        
        success = crm_manager.add_client(test_client)
        if success:
            print("✓ Client added successfully")
        else:
            print("✗ Failed to add client")
            return False
        
        # Test client retrieval
        retrieved_client = crm_manager.get_client(test_client.id)
        if retrieved_client and retrieved_client.name == "Jane Smith":
            print("✓ Client retrieved successfully")
        else:
            print("✗ Failed to retrieve client")
            return False
        
        # Test client search
        search_results = crm_manager.search_clients("Jane")
        if search_results and len(search_results) > 0:
            print("✓ Client search working")
        else:
            print("✗ Client search failed")
            return False
        
        # Test appointment creation
        test_appointment = Appointment(
            client_id=test_client.id,
            client_name="Jane Smith",
            client_email="jane.smith@example.com",
            start_time=datetime.now() + timedelta(days=7),
            duration=90,
            session_type="Portrait Session",
            session_fee=150.00,
            total_amount=150.00,
            location="Studio",
            priority="normal",
            notes="Outdoor session preferred"
        )
        
        success = crm_manager.add_appointment(test_appointment)
        if success:
            print("✓ Appointment added successfully")
        else:
            print("✗ Failed to add appointment")
            return False
        
        # Test client notes
        test_note = ClientNote(
            client_id=test_client.id,
            note_type="follow_up",
            title="Initial Consultation",
            content="Client interested in portrait session. Prefers outdoor locations.",
            author="Photographer",
            is_internal=False
        )
        
        success = crm_manager.add_client_note(test_note)
        if success:
            print("✓ Client note added successfully")
        else:
            print("✗ Failed to add client note")
            return False
        
        # Test analytics
        analytics = crm_manager.get_crm_analytics()
        if analytics:
            print("✓ CRM analytics working")
            print(f"  Total clients: {analytics.get('total_clients', 0)}")
            print(f"  Total appointments: {analytics.get('total_appointments', 0)}")
        else:
            print("✗ CRM analytics failed")
            return False
        
        # Test follow-up tasks
        follow_ups = crm_manager.get_follow_up_tasks()
        print(f"✓ Follow-up tasks: {len(follow_ups)} found")
        
        print("\nAll CRM database tests passed! ✓")
        return True
        
    except Exception as e:
        print(f"✗ CRM database test failed: {e}")
        return False


def test_client_models():
    """Test client model functionality"""
    print("\nTesting Client Models...")
    
    try:
        # Test Client model
        client = Client(
            name="John Doe",
            email="john.doe@example.com",
            phone="+1-555-0125",
            tags=["VIP", "Returning Client"]
        )
        
        # Test metrics update
        client.update_metrics(200.00)
        if client.total_appointments == 1 and client.total_spent == 200.00:
            print("✓ Client metrics update working")
        else:
            print("✗ Client metrics update failed")
            return False
        
        # Test note addition
        client.add_note("Client prefers natural lighting", internal=False)
        if "natural lighting" in client.notes:
            print("✓ Client note addition working")
        else:
            print("✗ Client note addition failed")
            return False
        
        # Test tag management
        client.add_tag("Portrait Client")
        if "Portrait Client" in client.tags:
            print("✓ Client tag addition working")
        else:
            print("✗ Client tag addition failed")
            return False
        
        client.remove_tag("VIP")
        if "VIP" not in client.tags:
            print("✓ Client tag removal working")
        else:
            print("✗ Client tag removal failed")
            return False
        
        print("✓ All client model tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Client model test failed: {e}")
        return False


def test_appointment_models():
    """Test appointment model functionality"""
    print("\nTesting Appointment Models...")
    
    try:
        # Test Appointment model
        appointment = Appointment(
            client_name="Test Client",
            client_email="test@example.com",
            start_time=datetime.now() + timedelta(days=14),
            duration=60,
            session_type="Portrait Session",
            session_fee=150.00,
            additional_charges=25.00,
            discount=0.00
        )
        
        # Test total amount calculation
        if appointment.total_amount == 175.00:
            print("✓ Appointment total calculation working")
        else:
            print("✗ Appointment total calculation failed")
            return False
        
        # Test payment status
        appointment.update_payment_status(100.00)
        if appointment.payment_status == "partial":
            print("✓ Payment status update working")
        else:
            print("✗ Payment status update failed")
            return False
        
        appointment.update_payment_status(175.00)
        if appointment.payment_status == "paid":
            print("✓ Payment status update working")
        else:
            print("✗ Payment status update failed")
            return False
        
        # Test note addition
        appointment.add_note("Client requested specific background", internal=False)
        if "specific background" in appointment.notes:
            print("✓ Appointment note addition working")
        else:
            print("✗ Appointment note addition failed")
            return False
        
        print("✓ All appointment model tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Appointment model test failed: {e}")
        return False


def test_marketing_campaigns():
    """Test marketing campaign functionality"""
    print("\nTesting Marketing Campaigns...")
    
    try:
        # Test MarketingCampaign model
        campaign = MarketingCampaign(
            name="Summer Portrait Special",
            description="Special pricing for summer portrait sessions",
            campaign_type="email",
            budget=500.00,
            target_audience=["Portrait Client", "New Client"]
        )
        
        if campaign.name == "Summer Portrait Special":
            print("✓ Marketing campaign creation working")
        else:
            print("✗ Marketing campaign creation failed")
            return False
        
        print("✓ All marketing campaign tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Marketing campaign test failed: {e}")
        return False


def main():
    """Run all CRM tests"""
    print("Gmail Photography Appointment Scheduler - CRM Test Suite")
    print("=" * 70)
    
    all_tests_passed = True
    
    # Run tests
    if not test_client_models():
        all_tests_passed = False
    
    if not test_appointment_models():
        all_tests_passed = False
    
    if not test_marketing_campaigns():
        all_tests_passed = False
    
    if not test_crm_database():
        all_tests_passed = False
    
    print("\n" + "=" * 70)
    
    if all_tests_passed:
        print("🎉 All CRM tests completed successfully!")
        print("\nThe CRM system is working properly with:")
        print("✓ Client management and database operations")
        print("✓ Appointment tracking and financial management")
        print("✓ Note management and communication tracking")
        print("✓ Analytics and reporting capabilities")
        print("✓ Marketing campaign management")
        print("\nNext steps:")
        print("1. Copy config.example.yaml to config.yaml and customize")
        print("2. Set up Google Cloud credentials (credentials.json)")
        print("3. Run 'python main.py --setup' to initialize the CRM system")
        print("4. Use 'python main.py crm --help' to see available CRM commands")
    else:
        print("❌ Some CRM tests failed. Please check the errors above.")
        sys.exit(1)


if __name__ == '__main__':
    main()
