from SetupGoogle import get_calendar_service

def GetEventId(event_title):

    service = get_calendar_service()

    try:
        # Obtenir la liste des événements du calendrier
        events = service.events().list(calendarId='primary').execute()
        
        # Parcourir les événements pour trouver l'ID de l'événement recherché
        for event in events['items']:
            if event['summary'] == event_title:
                return event['id']
        
        # Si l'événement n'a pas été trouvé, renvoyer None
        return None
    except Exception as e:
        print(f"Une erreur s'est produite lors de la récupération de l'ID de l'événement : {e}")
        return None

if __name__ == '__main__':
    # Remplacez 'Titre de l'événement' par le titre de l'événement dont vous souhaitez obtenir l'ID

    event_title = 'Test'
    event_id = GetEventId(event_title)

    if event_id:
        print(f"L'ID de l'événement '{event_title}' est : {event_id}")
    else:
        print(f"L'événement '{event_title}' n'a pas été trouvé.")