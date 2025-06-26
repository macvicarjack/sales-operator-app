"""
Email Client interface for Sales Operator app.
Provides a placeholder interface for email integration with systems like Outlook or Gmail.
"""

import streamlit as st
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailClient(ABC):
    """
    Abstract base class for email integration.
    Provides interface for common email operations.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the email client.
        
        Args:
            config (Optional[Dict[str, Any]]): Configuration dictionary for email connection.
        """
        self.config = config or {}
        self.connected = False
        self.sender_email = self.config.get("sender_email", "")
        self.sender_name = self.config.get("sender_name", "Sales Operator")
    
    @abstractmethod
    def connect(self) -> bool:
        """
        Establish connection to the email service.
        
        Returns:
            bool: True if connection successful, False otherwise.
        """
        raise NotImplementedError("Email connection not implemented")
    
    @abstractmethod
    def disconnect(self) -> None:
        """
        Disconnect from the email service.
        """
        raise NotImplementedError("Email disconnection not implemented")
    
    def send_email(self, to: str, subject: str, body: str) -> bool:
        """
        Send an email to the specified recipient.
        
        Args:
            to (str): Recipient email address.
            subject (str): Email subject line.
            body (str): Email body content.
        
        Returns:
            bool: True if email sent successfully, False otherwise.
            
        Raises:
            NotImplementedError: If email integration is not implemented.
        """
        raise NotImplementedError("Email sending not implemented")
    
    def send_email_with_cc(self, to: str, cc: List[str], subject: str, body: str) -> bool:
        """
        Send an email with CC recipients.
        
        Args:
            to (str): Primary recipient email address.
            cc (List[str]): List of CC recipient email addresses.
            subject (str): Email subject line.
            body (str): Email body content.
        
        Returns:
            bool: True if email sent successfully, False otherwise.
        """
        raise NotImplementedError("Email sending with CC not implemented")
    
    def send_email_with_attachments(self, to: str, subject: str, body: str, attachments: List[str]) -> bool:
        """
        Send an email with file attachments.
        
        Args:
            to (str): Recipient email address.
            subject (str): Email subject line.
            body (str): Email body content.
            attachments (List[str]): List of file paths to attach.
        
        Returns:
            bool: True if email sent successfully, False otherwise.
        """
        raise NotImplementedError("Email sending with attachments not implemented")
    
    def send_template_email(self, to: str, template_name: str, template_data: Dict[str, Any]) -> bool:
        """
        Send an email using a predefined template.
        
        Args:
            to (str): Recipient email address.
            template_name (str): Name of the template to use.
            template_data (Dict[str, Any]): Data to populate the template.
        
        Returns:
            bool: True if email sent successfully, False otherwise.
        """
        raise NotImplementedError("Template email sending not implemented")
    
    def send_follow_up_email(self, contact_name: str, contact_email: str, task_description: str) -> bool:
        """
        Send a follow-up email using the follow-up template.
        
        Args:
            contact_name (str): Name of the contact.
            contact_email (str): Email address of the contact.
            task_description (str): Description of the task being followed up on.
        
        Returns:
            bool: True if email sent successfully, False otherwise.
        """
        try:
            from pathlib import Path
            from jinja2 import Template
            
            # Load the follow-up template
            template_path = Path(__file__).parent.parent / "prompts" / "follow_up_prompt.txt"
            if template_path.exists():
                template_content = template_path.read_text()
                template = Template(template_content)
                
                # Render the template with data
                email_content = template.render(
                    contact_name=contact_name,
                    task_description=task_description,
                    your_name=self.sender_name
                )
                
                # Split content into subject and body
                lines = email_content.strip().split('\n')
                subject = lines[0].replace('Subject: ', '')
                body = '\n'.join(lines[1:])
                
                return self.send_email(contact_email, subject, body)
            else:
                # Fallback if template doesn't exist
                subject = "Following up on our conversation"
                body = f"""Hi {contact_name},

Just checking in about {task_description}. Let me know if there's anything else you need or if I can help move things forward.

Best,
{self.sender_name}"""
                
                return self.send_email(contact_email, subject, body)
                
        except Exception as e:
            print(f"Error sending follow-up email: {e}")
            return False
    
    def get_sent_emails(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get a list of recently sent emails.
        
        Args:
            limit (int): Maximum number of emails to retrieve.
        
        Returns:
            List[Dict[str, Any]]: List of sent email dictionaries.
        """
        raise NotImplementedError("Email retrieval not implemented")
    
    def get_email_templates(self) -> List[Dict[str, Any]]:
        """
        Get available email templates.
        
        Returns:
            List[Dict[str, Any]]: List of available email templates.
        """
        raise NotImplementedError("Email template retrieval not implemented")


class MockEmailClient(EmailClient):
    """
    Mock email client for testing and development.
    Prints email content to console instead of actually sending emails.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.sent_emails = []
        self.connected = True
    
    def connect(self) -> bool:
        """Mock connection - always returns True."""
        self.connected = True
        print("📧 Mock email client connected")
        return True
    
    def disconnect(self) -> None:
        """Mock disconnection."""
        self.connected = False
        print("📧 Mock email client disconnected")
    
    def send_email(self, to: str, subject: str, body: str) -> bool:
        """
        Mock email sending - prints to console and stores in sent_emails list.
        
        Args:
            to (str): Recipient email address.
            subject (str): Email subject line.
            body (str): Email body content.
        
        Returns:
            bool: Always returns True for mock client.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Print email content to console
        print("\n" + "="*60)
        print("📧 MOCK EMAIL SENT")
        print("="*60)
        print(f"From: {self.sender_email} ({self.sender_name})")
        print(f"To: {to}")
        print(f"Subject: {subject}")
        print(f"Date: {timestamp}")
        print("-"*60)
        print(body)
        print("="*60)
        print("(This is a mock email - no actual email was sent)")
        print()
        
        # Store in sent emails list
        self.sent_emails.append({
            "to": to,
            "subject": subject,
            "body": body,
            "timestamp": timestamp,
            "status": "sent"
        })
        
        return True
    
    def send_email_with_cc(self, to: str, cc: List[str], subject: str, body: str) -> bool:
        """Mock email sending with CC."""
        print(f"CC: {', '.join(cc)}")
        return self.send_email(to, subject, body)
    
    def send_email_with_attachments(self, to: str, subject: str, body: str, attachments: List[str]) -> bool:
        """Mock email sending with attachments."""
        print(f"Attachments: {', '.join(attachments)}")
        return self.send_email(to, subject, body)
    
    def send_template_email(self, to: str, template_name: str, template_data: Dict[str, Any]) -> bool:
        """Mock template email sending."""
        print(f"Template: {template_name}")
        print(f"Template data: {template_data}")
        
        # Create a simple template email
        subject = f"Template: {template_name}"
        body = f"Template email using '{template_name}' with data: {template_data}"
        
        return self.send_email(to, subject, body)
    
    def get_sent_emails(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get mock sent emails."""
        return self.sent_emails[-limit:]
    
    def get_email_templates(self) -> List[Dict[str, Any]]:
        """Get mock email templates."""
        return [
            {
                "name": "follow_up",
                "description": "Follow-up email template",
                "subject": "Following up on our conversation"
            },
            {
                "name": "welcome",
                "description": "Welcome email template",
                "subject": "Welcome to our service"
            },
            {
                "name": "meeting_invite",
                "description": "Meeting invitation template",
                "subject": "Meeting invitation"
            }
        ]


class SMTPEmailClient(EmailClient):
    """
    SMTP-based email client for sending emails via SMTP server.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.smtp_server = self.config.get("smtp_server", "smtp.gmail.com")
        self.smtp_port = self.config.get("smtp_port", 587)
        self.username = self.config.get("username", "")
        self.password = self.config.get("password", "")
        self.smtp_connection = None
    
    def connect(self) -> bool:
        """Connect to SMTP server."""
        try:
            self.smtp_connection = smtplib.SMTP(self.smtp_server, self.smtp_port)
            self.smtp_connection.starttls()
            self.smtp_connection.login(self.username, self.password)
            self.connected = True
            return True
        except Exception as e:
            print(f"SMTP connection failed: {e}")
            self.connected = False
            return False
    
    def disconnect(self) -> None:
        """Disconnect from SMTP server."""
        if self.smtp_connection:
            self.smtp_connection.quit()
            self.smtp_connection = None
        self.connected = False
    
    def send_email(self, to: str, subject: str, body: str) -> bool:
        """Send email via SMTP."""
        if not self.connected:
            if not self.connect():
                return False
        
        try:
            msg = MIMEMultipart()
            msg['From'] = f"{self.sender_name} <{self.sender_email}>"
            msg['To'] = to
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            text = msg.as_string()
            self.smtp_connection.sendmail(self.sender_email, to, text)
            
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False 