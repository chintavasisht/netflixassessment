from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import logging

CLIENT_SECRET_FILE = '/Users/vasishtchinta/netflixassessment/client-secret.json'
SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate():
    try:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
        creds = flow.run_local_server(port=8080, open_browser=True)
        logging.info("Successfully authenticated with Google Drive API")
        return build('drive', 'v3', credentials=creds)
    except Exception as e:
        logging.error(f"Failed to login: {e}")
        return None