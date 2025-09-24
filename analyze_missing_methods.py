#!/usr/bin/env python3
"""
Analyze missing methods and functions throughout the application
"""

import sys
import os
import inspect
from typing import List, Dict, Any

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def analyze_missing_methods():
    """Analyze what methods are expected vs what exists"""
    
    print("🔍 Analyzing Missing Methods and Functions")
    print("=" * 60)
    
    # Expected methods from web_app.py analysis
    expected_methods = {
        'crm_manager': [
            'get_recent_clients',
            'get_total_clients', 
            'get_all_clients',
            'create_client',
            'get_client',
            'get_baby_milestones',
            'update_client',
            'get_client_acquisition_data'
        ],
        'appointment_scheduler': [
            'get_appointments_by_date',
            'get_upcoming_appointments',
            'get_total_appointments',
            'get_monthly_revenue',
            'get_all_appointments',
            'create_appointment',
            'get_appointment',
            'update_appointment',
            'get_client_appointments',
            'get_appointments_in_range',
            'get_monthly_revenue_data',
            'get_session_type_statistics',
            'get_milestone_package_data'
        ],
        'config_manager': [
            'get_session_types',
            'save_config',
            'update_config'
        ]
    }
    
    try:
        # Import managers
        from config.config_manager import ConfigManager
        from scheduler.crm_manager import CRMManager
        from scheduler.appointment_scheduler import AppointmentScheduler
        
        print("✅ All managers imported successfully")
        
        # Initialize managers
        config_manager = ConfigManager()
        crm_manager = CRMManager(config_manager)
        appointment_scheduler = AppointmentScheduler(config_manager)
        
        print("✅ All managers initialized successfully")
        
        # Analyze each manager
        managers = {
            'crm_manager': crm_manager,
            'appointment_scheduler': appointment_scheduler,
            'config_manager': config_manager
        }
        
        missing_methods = {}
        
        for manager_name, manager in managers.items():
            print(f"\n📋 Analyzing {manager_name}:")
            
            # Get actual methods
            actual_methods = [m for m in dir(manager) if not m.startswith('_')]
            
            # Check expected methods
            expected = expected_methods.get(manager_name, [])
            missing = []
            
            for method in expected:
                if method not in actual_methods:
                    missing.append(method)
                    print(f"   ❌ Missing: {method}")
                else:
                    print(f"   ✅ Found: {method}")
            
            if missing:
                missing_methods[manager_name] = missing
            else:
                print(f"   🎉 All expected methods found!")
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 SUMMARY OF MISSING METHODS")
        print("=" * 60)
        
        total_missing = 0
        for manager_name, missing in missing_methods.items():
            if missing:
                print(f"\n{manager_name.upper()}:")
                for method in missing:
                    print(f"  - {method}")
                    total_missing += 1
        
        if total_missing == 0:
            print("\n🎉 All expected methods are implemented!")
        else:
            print(f"\n❌ Total missing methods: {total_missing}")
        
        # Additional analysis - check for methods that might be called but don't exist
        print("\n" + "=" * 60)
        print("🔍 ADDITIONAL ANALYSIS")
        print("=" * 60)
        
        # Check for methods that might be missing from other parts of the codebase
        print("\nChecking for other potential missing methods...")
        
        # Check if there are any other manager classes that might be missing
        try:
            from gmail.gmail_manager import GmailManager
            from calendar_integration.calendar_manager import CalendarManager
            from utils.template_manager import TemplateManager
            
            print("✅ Gmail, Calendar, and Template managers imported")
            
            # Check if these managers have the methods they're expected to have
            gmail_manager = GmailManager(config_manager)
            calendar_manager = CalendarManager(config_manager)
            template_manager = TemplateManager(config_manager)
            
            print("✅ All additional managers initialized")
            
        except Exception as e:
            print(f"⚠️  Some managers couldn't be imported: {e}")
        
        return missing_methods
        
    except Exception as e:
        print(f"❌ Analysis failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return {}

if __name__ == '__main__':
    missing = analyze_missing_methods()
    
    if missing:
        print(f"\n🚨 CRITICAL: {sum(len(m) for m in missing.values())} methods are missing!")
        print("These need to be implemented for the application to work properly.")
    else:
        print("\n🎉 All methods are implemented!")
