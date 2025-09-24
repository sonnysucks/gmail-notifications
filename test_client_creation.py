#!/usr/bin/env python3
"""
Test script to verify client creation is working
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from config.config_manager import ConfigManager
    from scheduler.crm_manager import CRMManager
    from scheduler.appointment_scheduler import AppointmentScheduler
    
    print("✅ All managers imported successfully")
    
    # Initialize config manager
    config_manager = ConfigManager()
    print("✅ Config manager initialized")
    
    # Initialize CRM manager
    crm_manager = CRMManager(config_manager)
    print("✅ CRM manager initialized")
    
    # Test client creation
    test_client_data = {
        'name': 'Test Family',
        'email': 'test@example.com',
        'phone': '(555) 999-8888',
        'children_count': 1,
        'children_names': 'Baby Test',
        'children_birth_dates': '2025-01-01',
        'family_type': 'New Parents'
    }
    
    print(f"📝 Creating test client: {test_client_data['name']}")
    
    # Create client
    client = crm_manager.add_client(test_client_data)
    print(f"✅ Client created with ID: {client.id}")
    
    # Verify client was saved
    saved_client = crm_manager.get_client(client.id)
    print(f"✅ Client retrieved: {saved_client.name}")
    
    # List all clients
    all_clients = crm_manager.get_all_clients()
    print(f"✅ Total clients in database: {len(all_clients)}")
    
    print("\n🎉 Client creation test completed successfully!")
    
except Exception as e:
    print(f"❌ Test failed: {str(e)}")
    import traceback
    traceback.print_exc()
