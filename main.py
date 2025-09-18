import datetime as dt
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def showNextEvents(numberOfEvents):
    """Shows basic usage of the Google Calendar API."""
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
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        service = build('calendar', 'v3', credentials=creds)
        now = dt.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        print(f'Getting the upcoming {numberOfEvents} events')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=numberOfEvents, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])
        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
    except HttpError as error:
        print(f'An error occurred: {error}')


def createEvent():
    """Shows basic usage of the Google Calendar API."""
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
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        service = build('calendar', 'v3', credentials=creds)
        event = {
            'summary': 'Yazeed test event ',
            'description': 'This is a test event from python through google calendar api',
            'colorId': '6',
            'location': 'Riyadh',
            'start': {
                'dateTime': f'{dt.datetime.now().isoformat()}',
                'timeZone': 'Asia/Riyadh'
            },
            'end': {
                'dateTime': f'{dt.datetime.now().isoformat()}',
                'timeZone': 'Asia/Riyadh'
            },
            'attendees': [
                {
                    'email': '7bolooo@gmail.com',
                    'email': 'ali.alorainy@gmail.com',
                }
            ]
        }
        event = service.events().insert(calendarId='primary', body=event).execute()
        print(f'Event created: {event.get('htmlLink')}')
    except HttpError as error:
        print(f'An error occurred: {error}')

if __name__ == '__main__':
    while True:
        print('Choose an option: ')
        print('1. Show next events')
        print('2. Create event')
        print('3. Exit')
        choice = int(input())
        if choice == 1:
            print('Enter the number of events to show: ')
            numberOfEvents = int(input())
            showNextEvents(numberOfEvents)
        elif choice == 2:
            createEvent()
        elif choice == 3:
            print('Exiting...')
            break
        else:
            print('Invalid choice')