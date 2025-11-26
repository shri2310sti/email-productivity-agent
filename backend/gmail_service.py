import os
import base64
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 
          'https://www.googleapis.com/auth/gmail.compose']

class GmailService:
    def __init__(self):
        self.service = None
        try:
            self.authenticate()
        except Exception as e:
            print(f"Gmail authentication error: {str(e)}")
            raise
    
    def authenticate(self):
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists('credentials.json'):
                    raise FileNotFoundError("credentials.json not found")
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        
        self.service = build('gmail', 'v1', credentials=creds)
    
    def get_emails(self, max_results=20):
        try:
            results = self.service.users().messages().list(
                userId='me', maxResults=max_results, labelIds=['INBOX']
            ).execute()
            messages = results.get('messages', [])
            emails = []
            for message in messages:
                msg = self.service.users().messages().get(
                    userId='me', id=message['id'], format='full'
                ).execute()
                emails.append(self.parse_email(msg))
            return emails
        except Exception as e:
            print(f"Error fetching emails: {str(e)}")
            return []
    
    def parse_email(self, message):
        headers = message['payload']['headers']
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
        from_email = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
        date = next((h['value'] for h in headers if h['name'] == 'Date'), '')
        
        body = ''
        if 'parts' in message['payload']:
            for part in message['payload']['parts']:
                if part['mimeType'] == 'text/plain' and 'data' in part['body']:
                    body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                    break
        elif 'data' in message['payload']['body']:
            body = base64.urlsafe_b64decode(message['payload']['body']['data']).decode('utf-8')
        
        return {
            'id': message['id'],
            'from': from_email,
            'subject': subject,
            'body': body[:1000],
            'timestamp': date,
            'category': None,
            'actionItems': []
        }
    
    def create_draft(self, to, subject, body):
        try:
            message = MIMEText(body)
            message['to'] = to
            message['subject'] = subject
            raw = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
            draft = self.service.users().drafts().create(
                userId='me', body={'message': {'raw': raw}}
            ).execute()
            return {'success': True, 'draft_id': draft['id']}
        except Exception as e:
            return {'success': False, 'error': str(e)}