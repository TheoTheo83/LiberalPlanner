from SetupGoogle import get_calendar_service

def InsertEvent(summary, location, description, sDateTime, eDateTime):
    # Crée et ajoute à la liste d'agenda une nouvelle évènement
    service = get_calendar_service()

    # Informations sur l'événement que vous souhaitez insérer
    event = {
        'summary': summary, # Titre de l'événement
        'location': location, # Lieu de l'événement
        'description': description, # Description de l'événement
        'start': {
            'dateTime': sDateTime, # Heure de début de l'événement
            'timeZone': 'Europe/Paris',  # Fuseau horaire de l'événement
        },
        'end': {
            'dateTime': eDateTime, # Heure de fin de l'événement
            'timeZone': 'Europe/Paris',  # Fuseau horaire de l'événement
        },
    }

    # Insertion de l'événement dans Google Agenda dans l'agenda principal
    event = service.events().insert(calendarId='primary', body=event).execute()
    print(f'Événement créé: {event.get("htmlLink")}')

if __name__ == '__main__':
   InsertEvent('Test', 'Marseille', 'C est un test Marseillais', '2023-07-18T18:00:00', '2023-07-18T19:00:00')