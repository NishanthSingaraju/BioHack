import datetime
import logging
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def authenticate():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=3000)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def get_calendar_events():
    creds = authenticate()
    try:
        service = build('calendar', 'v3', credentials=creds)
        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        logging.info('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])
        if not events:
            logging.info('No upcoming events found.')
            return

        # Prints the start and name of the next 10 events
        calendar_items = []
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            calendar_items.append((start, event['summary']))
        return calendar_items

    except HttpError as error:
        logging.info('An error occurred: %s' % error)

def put_calendar_events(jsonFile):
    creds = authenticate()
    try:
        service = build('calendar', 'v3', credentials=creds)
        event = service.events().insert(calendarId='primary', body=jsonFile).execute()
        logging.info('Event created: %s' % (event.get('htmlLink')))
    except HttpError as error:
        logging.info('An error occurred: %s' % error)


if __name__ == '__main__':
     logging.basicConfig(level=logging.INFO)

