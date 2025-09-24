"""
Configuration management for the Gmail Photography Appointment Scheduler
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)


class ConfigManager:
    """Manages application configuration"""
    
    def __init__(self, config_path: str = 'config.yaml'):
        """Initialize configuration manager"""
        self.config_path = Path(config_path)
        self.config = {}
        self.load_config()
    
    def load_config(self):
        """Load configuration from YAML file"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
            
            self.validate_config()
            logger.info(f"Configuration loaded from {self.config_path}")
            
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in configuration file: {e}")
        except Exception as e:
            raise RuntimeError(f"Failed to load configuration: {e}")
    
    def validate_config(self):
        """Validate configuration structure and required fields"""
        required_sections = ['business', 'calendar', 'appointments', 'email', 'gmail', 'logging']
        
        for section in required_sections:
            if section not in self.config:
                raise ValueError(f"Missing required configuration section: {section}")
        
        # Validate business section
        business = self.config['business']
        required_business_fields = ['name', 'email']
        for field in required_business_fields:
            if field not in business:
                raise ValueError(f"Missing required business field: {field}")
        
        # Validate calendar section
        calendar = self.config['calendar']
        if 'target_calendar_id' not in calendar:
            raise ValueError("Missing target_calendar_id in calendar section")
        
        # Validate appointments section
        appointments = self.config['appointments']
        if 'reminder_schedule' not in appointments:
            raise ValueError("Missing reminder_schedule in appointments section")
        
        # Validate email section
        email = self.config['email']
        if 'templates' not in email:
            raise ValueError("Missing templates in email section")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key (supports dot notation)"""
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def get_business_info(self) -> Dict[str, str]:
        """Get business information"""
        return self.config.get('business', {})
    
    def get_calendar_config(self) -> Dict[str, Any]:
        """Get calendar configuration"""
        return self.config.get('calendar', {})
    
    def get_appointment_config(self) -> Dict[str, Any]:
        """Get appointment configuration"""
        return self.config.get('appointments', {})
    
    def get_email_config(self) -> Dict[str, Any]:
        """Get email configuration"""
        return self.config.get('email', {})
    
    def get_gmail_config(self) -> Dict[str, Any]:
        """Get Gmail configuration"""
        return self.config.get('gmail', {})
    
    def get_logging_config(self) -> Dict[str, Any]:
        """Get logging configuration"""
        return self.config.get('logging', {})
    
    def get_reminder_schedule(self) -> list:
        """Get reminder schedule configuration"""
        return self.config.get('appointments', {}).get('reminder_schedule', [])
    
    def get_template_path(self, template_name: str) -> Optional[str]:
        """Get template file path by name"""
        templates = self.config.get('email', {}).get('templates', {})
        return templates.get(template_name)
    
    def reload(self):
        """Reload configuration from file"""
        self.load_config()
    
    def get_credentials_path(self) -> str:
        """Get Google credentials file path"""
        # Check for credentials.json in current directory
        credentials_path = Path('credentials.json')
        if credentials_path.exists():
            return str(credentials_path)
        
        # Check for GOOGLE_APPLICATION_CREDENTIALS environment variable
        env_credentials = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        if env_credentials:
            return env_credentials
        
        # Default fallback
        return 'credentials.json'
    
    def get_session_types(self) -> Dict[str, Dict[str, Any]]:
        """Get session types from configuration as a dictionary with session names as keys"""
        session_types_list = self.config.get('session_types', [])
        session_types_dict = {}
        
        for session in session_types_list:
            session_name = session.get('name', 'Unknown Session')
            session_types_dict[session_name] = session
        
        return session_types_dict
    
    def save_config(self, config_data: Dict[str, Any]) -> bool:
        """Save configuration to file"""
        try:
            self.config.update(config_data)
            
            with open(self.config_path, 'w') as f:
                yaml.dump(self.config, f, default_flow_style=False, indent=2)
            
            logger.info("Configuration saved successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
            return False
    
    def update_config(self, config_data: Dict[str, Any]) -> bool:
        """Update specific configuration sections"""
        try:
            # Update only the provided sections
            for section, values in config_data.items():
                if section in self.config:
                    if isinstance(values, dict):
                        self.config[section].update(values)
                    else:
                        self.config[section] = values
                else:
                    self.config[section] = values
            
            # Save the updated configuration
            return self.save_config(self.config)
            
        except Exception as e:
            logger.error(f"Failed to update configuration: {e}")
            return False
