#!/usr/bin/env python3
"""
Initialize default photography packages
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scheduler.models import Package
from scheduler.crm_manager import CRMManager
from config.config_manager import ConfigManager

def create_default_packages():
    """Create default photography packages"""
    
    # Initialize managers
    config_manager = ConfigManager()
    crm_manager = CRMManager(config_manager)
    
    # Initialize database
    crm_manager._init_database()
    
    # Default packages
    packages = [
        Package(
            name="Newborn Essentials",
            description="Perfect for capturing your baby's first precious moments",
            category="newborn",
            base_price=350.00,
            duration_minutes=180,
            is_customizable=True,
            includes=[
                "3-hour session",
                "25+ edited high-resolution images",
                "Online gallery for sharing",
                "Print release",
                "Props and accessories included",
                "Backup session date if baby is fussy"
            ],
            add_ons=[
                {"name": "Extra hour", "price": 100.00, "description": "Additional hour for extended session"},
                {"name": "Rush editing", "price": 75.00, "description": "48-hour delivery"},
                {"name": "Parent shots", "price": 50.00, "description": "Include parents in 5 images"}
            ],
            requirements=[
                "Baby should be 5-14 days old",
                "Studio temperature kept at 80°F",
                "Plan for 3-4 hours total time",
                "Baby should be fed right before session"
            ],
            recommended_age="5-14 days",
            optimal_timing="Morning sessions work best",
            customizable_fields=["base_price", "duration_minutes", "includes"],
            price_ranges={"min": 300.00, "max": 500.00},
            is_active=True,
            is_featured=True,
            display_order=1
        ),
        
        Package(
            name="Maternity Glow",
            description="Celebrate your pregnancy with beautiful maternity portraits",
            category="maternity",
            base_price=250.00,
            duration_minutes=90,
            is_customizable=True,
            includes=[
                "90-minute session",
                "30+ edited high-resolution images",
                "Online gallery",
                "Print release",
                "Maternity gowns available",
                "Partner and family shots included"
            ],
            add_ons=[
                {"name": "Outdoor location", "price": 50.00, "description": "Session at outdoor location"},
                {"name": "Extra outfit", "price": 25.00, "description": "Additional outfit change"},
                {"name": "Belly casting", "price": 150.00, "description": "Professional belly cast keepsake"}
            ],
            requirements=[
                "Best between 28-36 weeks",
                "Bring comfortable shoes",
                "Avoid lotions on day of shoot"
            ],
            recommended_weeks="28-36 weeks",
            optimal_timing="Golden hour for outdoor shoots",
            customizable_fields=["base_price", "duration_minutes"],
            price_ranges={"min": 200.00, "max": 350.00},
            is_active=True,
            is_featured=False,
            display_order=2
        ),
        
        Package(
            name="Milestone Magic - 6 Month",
            description="Capture your baby's sitting milestone with adorable photos",
            category="milestone",
            base_price=225.00,
            duration_minutes=60,
            is_customizable=True,
            includes=[
                "1-hour session",
                "20+ edited images",
                "Online gallery",
                "Print release",
                "Props and toys included",
                "Sitting poses and tummy time shots"
            ],
            add_ons=[
                {"name": "Cake smash add-on", "price": 75.00, "description": "Mini cake for smashing fun"},
                {"name": "Bath splash", "price": 50.00, "description": "Cute bath time photos"},
                {"name": "Family shots", "price": 40.00, "description": "Include family in 5 images"}
            ],
            requirements=[
                "Baby should be sitting unassisted",
                "Bring favorite toys",
                "Plan session around nap time"
            ],
            recommended_age="6-8 months",
            optimal_timing="Mid-morning after breakfast",
            customizable_fields=["base_price", "add_ons"],
            price_ranges={"min": 175.00, "max": 300.00},
            is_active=True,
            is_featured=False,
            display_order=3
        ),
        
        Package(
            name="Smash Cake Celebration",
            description="Let your little one get messy with their very own cake!",
            category="birthday",
            base_price=300.00,
            duration_minutes=90,
            is_customizable=True,
            includes=[
                "90-minute session",
                "25+ edited images",
                "6-inch smash cake included",
                "Themed decorations",
                "Before, during, and after shots",
                "Bath time cleanup photos",
                "Online gallery and print release"
            ],
            add_ons=[
                {"name": "Custom theme", "price": 50.00, "description": "Custom theme decorations"},
                {"name": "Sibling shots", "price": 60.00, "description": "Include siblings in session"},
                {"name": "Professional cake", "price": 100.00, "description": "Upgrade to professional bakery cake"}
            ],
            requirements=[
                "Best for 11-13 month old babies",
                "Bring backup outfit",
                "Plan for cleanup time"
            ],
            recommended_age="11-13 months",
            optimal_timing="Morning when baby is happiest",
            customizable_fields=["base_price", "duration_minutes", "add_ons"],
            price_ranges={"min": 250.00, "max": 450.00},
            is_active=True,
            is_featured=True,
            display_order=4
        ),
        
        Package(
            name="Growing Family",
            description="Beautiful family portraits to treasure forever",
            category="family",
            base_price=275.00,
            duration_minutes=75,
            is_customizable=True,
            includes=[
                "75-minute session",
                "30+ edited images",
                "Multiple family combinations",
                "Individual child portraits",
                "Online gallery",
                "Print release"
            ],
            add_ons=[
                {"name": "Extended family", "price": 25.00, "description": "Per additional family member"},
                {"name": "Pet inclusion", "price": 40.00, "description": "Include family pets"},
                {"name": "Location change", "price": 75.00, "description": "Second location during session"}
            ],
            requirements=[
                "Coordinate outfits in advance",
                "Plan around children's schedules",
                "Bring snacks for little ones"
            ],
            recommended_age="All ages",
            optimal_timing="Golden hour for best lighting",
            customizable_fields=["base_price", "duration_minutes", "includes"],
            price_ranges={"min": 225.00, "max": 400.00},
            is_active=True,
            is_featured=False,
            display_order=5
        )
    ]
    
    # Add packages to database
    for package in packages:
        success = crm_manager.add_package(package)
        if success:
            print(f"✅ Created package: {package.name}")
        else:
            print(f"❌ Failed to create package: {package.name}")
    
    print(f"\n🎉 Package initialization complete! Created {len(packages)} packages.")

if __name__ == "__main__":
    create_default_packages()
