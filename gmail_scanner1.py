import os
import base64
import json
import requests
import pickle
from email import message_from_bytes
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# === CONFIG ===
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
CREDENTIALS_FILE = 'credentials.json'  # downloaded from Google Cloud console
TOKEN_FILE = 'token.pickle'
FASTAPI_BACKEND_URL = 'http://localhost:8000/api/subscriptions'  # change if needed

# === GMAIL AUTH ===
def authenticate_gmail():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)

# === GMAIL SEARCH & PARSE ===
def find_subscription_emails(service):
    query = 'subject:(receipt OR subscription OR renewal)'
    results = service.users().messages().list(userId='me', q=query, maxResults=10).execute()
    messages = results.get('messages', [])
    subs = []
    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id'], format='raw').execute()
        raw_data = base64.urlsafe_b64decode(msg_data['raw'].encode('ASCII'))
        email_message = message_from_bytes(raw_data)

        subject = email_message['subject'] or ''
        body = email_message.get_payload(decode=True) or b''
        text = body.decode(errors='ignore')

        # Basic parsing - can be improved with regex later
        sub = {
            'service': subject.split()[0],
            'tier': 'Unknown',
            'next_charge': 'Unknown',
            'payment_method': 'Unknown'
        }
        subs.append(sub)
    return subs

# === POST TO BACKEND ===
def post_to_backend(subs):
    for sub in subs:
        res = requests.post(FASTAPI_BACKEND_URL, json=sub)
        print(f"[+] Posted: {res.status_code} {sub['service']}")

if __name__ == '__main__':
    print("[.] Authenticating with Gmail...")
    gmail_service = authenticate_gmail()

    print("[.] Scanning for subscription emails...")
    subscriptions = find_subscription_emails(gmail_service)

    print("[.] Sending subscriptions to backend...")
    post_to_backend(subscriptions)

    print("[✓] Done.")
