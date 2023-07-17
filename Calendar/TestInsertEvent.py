from SetupGoogle import get_calendar_service

def InsertEvent():
    # Crée et ajoute à la liste d'agenda une nouvelle évènement
    service = get_calendar_service()

    # Informations sur l'événement que vous souhaitez insérer
    event = {
        'summary': 'Test2',
        'location': 'Marseille',
        'description': 'C est un test Marseillais',
        'start': {
            'dateTime': '2023-07-17T10:00:00', # Heure de début de l'événement
            'timeZone': 'Europe/Paris',  # Fuseau horaire de l'événement
        },
        'end': {
            'dateTime': '2023-07-17T12:00:00', # Heure de fin de l'événement
            'timeZone': 'Europe/Paris',  # Fuseau horaire de l'événement
        },
    }

    # Insertion de l'événement dans Google Agenda
    event = service.events().insert(calendarId='primary', body=event).execute()
    print(f'Événement créé: {event.get("htmlLink")}')

if __name__ == '__main__':
   InsertEvent()