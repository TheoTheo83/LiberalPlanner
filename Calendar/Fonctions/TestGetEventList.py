import datetime
from SetupGoogle import get_calendar_service

def GetEventList():
   
   service = get_calendar_service()

   # Call the Calendar API
   now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
   print('Getting List of 10 events')
   events_result = service.events().list(
       calendarId='primary', timeMin=now,
       maxResults=100, singleEvents=True,
       orderBy='startTime').execute()
   events = events_result.get('items', [])

   if not events:
       print('Aucun événements à venir.')
   for event in events:
       start = event['start'].get('dateTime', event['start'].get('date'))
       print("Date et heure de début : " + start, "/ Titre : " + event['summary'], "/ id : " + event['id'])

if __name__ == '__main__':
   GetEventList()