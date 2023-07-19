from datetime import datetime, timedelta
from SetupGoogle import get_calendar_service


# Update an existing Google Calendar Event by ID with new summary and time range
def EditEvent(event_id, event_new_summary = None, event_new_start = None, event_new_end = None):
    
    d = datetime.now().date()
    tomorrow = datetime(d.year, d.month, d.day, 9)+timedelta(days=1)
    start = tomorrow.isoformat()
    end = (tomorrow + timedelta(hours=2)).isoformat()

    service = get_calendar_service()

    event_result = service.events().update(
        calendarId='primary',
        eventId= event_id ,
        body={
           "summary": event_new_summary,
           "description": 'This is a tutorial example of automating google calendar with python, updated time.',
           "start": {"dateTime": event_new_start, "timeZone": 'Asia/Kolkata'},
           "end": {"dateTime": event_new_end, "timeZone": 'Asia/Kolkata'},
        },
    ).execute()

    print("updated event")
    print("id: ", event_result['id'])
    print("summary: ", event_result['summary'])
    print("starts at: ", event_result['start']['dateTime'])
    print("ends at: ", event_result['end']['dateTime'])

    return event_result

if __name__ == '__main__':

    event_id ='fcseumpvs6cvcnd7rbup19ev1g'
    event_new_summary = 'TestTheo'
    event_new_start = '2023-07-19T11:00:00'
    durée = 2
    event_new_end = '2023-07-20T11:00:00'

    result = EditEvent(event_id, event_new_summary, event_new_start, event_new_end)
    print (result['id'])