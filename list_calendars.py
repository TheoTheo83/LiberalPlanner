from cal_setup import get_calendar_service

def main():
   service = get_calendar_service()
   # Call the Calendar API
   print('Getting list of calendars')
#    calendar_list_entry = service.calendarList().get(calendarId='hr5aarphet90tvumauu9esupac@group.calendar.google.com').execute()
#    print (calendar_list_entry['summary'])

   calendar_list_entry = {
    "id" : "TestTheo"
    }
   created_calendar_list_entry = service.calendarList().insert(body=calendar_list_entry).execute()
   print (created_calendar_list_entry['summary'])


   calendars_result = service.calendarList().list().execute()

   calendars = calendars_result.get('items', [])

   if not calendars:
       print('No calendars found.')
   for calendar in calendars:
       summary = calendar['summary']
       id = calendar['id']
       primary = "Primary" if calendar.get('primary') else ""
       print("%s\t%s\t%s" % (summary, id, primary))

if __name__ == '__main__':
   main()