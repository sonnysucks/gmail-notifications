"""
Gmail API integration and email management
"""

import os
import base64
import logging
from typing import List, Dict, Any, Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from ..config.config_manager import ConfigManager

logger = logging.getLogger(__name__)

# Gmail API scopes
SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.labels'
]


class GmailManager:
    """Manages Gmail operations and API integration"""
    
    def __init__(self, config_manager: ConfigManager):
        """Initialize Gmail manager"""
        self.config = config_manager
        self.service = None
        self.credentials = None
        
    def authenticate(self):
        """Authenticate with Gmail API"""
        try:
            creds = None
            token_path = 'token.json'
            
            # Check if we have valid credentials
            if os.path.exists(token_path):
                creds = Credentials.from_authorized_user_file(token_path, SCOPES)
            
            # If no valid credentials available, let the user log in
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.config.get_credentials_path(), SCOPES)
                    creds = flow.run_local_server(port=0)
                
                # Save the credentials for the next run
                with open(token_path, 'w') as token:
                    token.write(creds.to_json())
            
            self.credentials = creds
            self.service = build('gmail', 'v1', credentials=creds)
            
            logger.info("Successfully authenticated with Gmail API")
            
        except Exception as e:
            logger.error(f"Gmail authentication failed: {e}")
            raise
    
    def setup_labels(self):
        """Create necessary Gmail labels for appointment management"""
        try:
            if not self.service:
                raise RuntimeError("Gmail service not initialized. Call authenticate() first.")
            
            label_name = self.config.get('gmail.label_name', 'Photography Appointments')
            
            # Check if label already exists
            existing_labels = self.service.users().labels().list(userId='me').execute()
            
            label_exists = any(
                label['name'] == label_name 
                for label in existing_labels.get('labels', [])
            )
            
            if not label_exists:
                # Create new label
                label_object = {
                    'name': label_name,
                    'labelListVisibility': 'labelShow',
                    'messageListVisibility': 'show'
                }
                
                created_label = self.service.users().labels().create(
                    userId='me', body=label_object).execute()
                
                logger.info(f"Created Gmail label: {label_name}")
                return created_label['id']
            else:
                logger.info(f"Gmail label already exists: {label_name}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to setup Gmail labels: {e}")
            raise
    
    def send_email(self, to: str, subject: str, body: str, 
                   html_body: Optional[str] = None) -> str:
        """Send an email via Gmail API"""
        try:
            if not self.service:
                raise RuntimeError("Gmail service not initialized. Call authenticate() first.")
            
            # Create message
            message = MIMEMultipart('alternative')
            message['to'] = to
            message['subject'] = subject
            
            # Add text and HTML parts
            text_part = MIMEText(body, 'plain')
            message.attach(text_part)
            
            if html_body:
                html_part = MIMEText(html_body, 'html')
                message.attach(html_part)
            
            # Encode message
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
            
            # Send message
            sent_message = self.service.users().messages().send(
                userId='me', body={'raw': raw_message}).execute()
            
            message_id = sent_message['id']
            logger.info(f"Email sent successfully to {to}, message ID: {message_id}")
            
            return message_id
            
        except Exception as e:
            logger.error(f"Failed to send email to {to}: {e}")
            raise
    
    def scan_for_appointments(self) -> List[Dict[str, Any]]:
        """Scan Gmail for potential appointment emails"""
        try:
            if not self.service:
                raise RuntimeError("Gmail service not initialized. Call authenticate() first.")
            
            search_query = self.config.get('gmail.search_query', 
                'subject:(appointment OR session OR photoshoot) OR body:(appointment OR session OR photoshoot)')
            
            # Search for emails
            results = self.service.users().messages().list(
                userId='me', q=search_query, maxResults=50).execute()
            
            messages = results.get('messages', [])
            appointment_emails = []
            
            for message in messages:
                try:
                    # Get full message details
                    msg = self.service.users().messages().get(
                        userId='me', id=message['id'], format='full').execute()
                    
                    # Extract email data
                    email_data = self._extract_email_data(msg)
                    
                    if email_data:
                        appointment_emails.append(email_data)
                        
                except Exception as e:
                    logger.warning(f"Failed to process message {message['id']}: {e}")
                    continue
            
            logger.info(f"Found {len(appointment_emails)} potential appointment emails")
            return appointment_emails
            
        except Exception as e:
            logger.error(f"Failed to scan Gmail for appointments: {e}")
            raise
    
    def _extract_email_data(self, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extract relevant data from Gmail message"""
        try:
            headers = message['payload'].get('headers', [])
            
            # Extract basic email information
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '')
            from_header = next((h['value'] for h in headers if h['name'] == 'From'), '')
            date_header = next((h['value'] for h in headers if h['name'] == 'Date'), '')
            
            # Extract email body
            body = self._extract_body(message['payload'])
            
            # Check if email is from potential client (not from business email)
            business_email = self.config.get('business.email', '').lower()
            if business_email and business_email in from_header.lower():
                return None  # Skip emails from business
            
            return {
                'id': message['id'],
                'subject': subject,
                'from': from_header,
                'date': date_header,
                'body': body,
                'thread_id': message.get('threadId'),
                'snippet': message.get('snippet', '')
            }
            
        except Exception as e:
            logger.warning(f"Failed to extract email data: {e}")
            return None
    
    def _extract_body(self, payload: Dict[str, Any]) -> str:
        """Extract email body from Gmail message payload"""
        try:
            if 'body' in payload and payload['body'].get('data'):
                # Simple text body
                data = payload['body']['data']
                return base64.urlsafe_b64decode(data).decode('utf-8')
            
            elif 'parts' in payload:
                # Multipart message
                body_parts = []
                for part in payload['parts']:
                    if part.get('mimeType') == 'text/plain':
                        if part['body'].get('data'):
                            data = part['body']['data']
                            body_parts.append(base64.urlsafe_b64decode(data).decode('utf-8'))
                        break
                
                return ' '.join(body_parts)
            
            return ""
            
        except Exception as e:
            logger.warning(f"Failed to extract email body: {e}")
            return ""
    
    def mark_as_processed(self, message_id: str):
        """Mark an email as processed by adding a label"""
        try:
            if not self.service:
                raise RuntimeError("Gmail service not initialized. Call authenticate() first.")
            
            label_name = self.config.get('gmail.label_name', 'Photography Appointments')
            
            # Get label ID
            labels = self.service.users().labels().list(userId='me').execute()
            label_id = None
            
            for label in labels.get('labels', []):
                if label['name'] == label_name:
                    label_id = label['id']
                    break
            
            if label_id:
                # Add label to message
                self.service.users().messages().modify(
                    userId='me', 
                    id=message_id, 
                    body={'addLabelIds': [label_id]}
                ).execute()
                
                logger.info(f"Marked message {message_id} as processed")
            else:
                logger.warning(f"Label '{label_name}' not found")
                
        except Exception as e:
            logger.error(f"Failed to mark message {message_id} as processed: {e}")
    
    def get_email_thread(self, thread_id: str) -> List[Dict[str, Any]]:
        """Get all messages in an email thread"""
        try:
            if not self.service:
                raise RuntimeError("Gmail service not initialized. Call authenticate() first.")
            
            thread = self.service.users().threads().get(
                userId='me', id=thread_id).execute()
            
            messages = thread.get('messages', [])
            email_data_list = []
            
            for message in messages:
                email_data = self._extract_email_data(message)
                if email_data:
                    email_data_list.append(email_data)
            
            return email_data_list
            
        except Exception as e:
            logger.error(f"Failed to get email thread {thread_id}: {e}")
            raise
    
    def search_emails(self, query: str, max_results: int = 100) -> List[Dict[str, Any]]:
        """Search emails with custom query"""
        try:
            if not self.service:
                raise RuntimeError("Gmail service not initialized. Call authenticate() first.")
            
            results = self.service.users().messages().list(
                userId='me', q=query, maxResults=max_results).execute()
            
            messages = results.get('messages', [])
            email_data_list = []
            
            for message in messages:
                try:
                    msg = self.service.users().messages().get(
                        userId='me', id=message['id'], format='full').execute()
                    
                    email_data = self._extract_email_data(msg)
                    if email_data:
                        email_data_list.append(email_data)
                        
                except Exception as e:
                    logger.warning(f"Failed to process message {message['id']}: {e}")
                    continue
            
            return email_data_list
            
        except Exception as e:
            logger.error(f"Failed to search emails: {e}")
            raise
    
    def delete_email(self, message_id: str) -> bool:
        """Delete an email (move to trash)"""
        try:
            if not self.service:
                raise RuntimeError("Gmail service not initialized. Call authenticate() first.")
            
            self.service.users().messages().trash(userId='me', id=message_id).execute()
            logger.info(f"Moved message {message_id} to trash")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete message {message_id}: {e}")
            return False
    
    def get_labels(self) -> List[Dict[str, Any]]:
        """Get all Gmail labels"""
        try:
            if not self.service:
                raise RuntimeError("Gmail service not initialized. Call authenticate() first.")
            
            labels = self.service.users().labels().list(userId='me').execute()
            return labels.get('labels', [])
            
        except Exception as e:
            logger.error(f"Failed to get labels: {e}")
            raise
