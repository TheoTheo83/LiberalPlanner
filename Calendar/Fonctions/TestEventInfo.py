from SetupGoogle import get_calendar_service

def get_event_details(event_id):

    service = get_calendar_service()

    try:
        # Obtenir les détails de l'événement spécifié par son ID
        event = service.events().get(calendarId='primary', eventId=event_id).execute()
        if event:
            print("Détails de l'événement :")
            print(f"Titre : {event['summary']}")
            print(f"Emplacement : {event.get('location', 'N/A')}")
            print(f"Description : {event.get('description', 'N/A')}")
            print(f"Heure de début : {event['start'].get('dateTime', event['start'].get('date'))}")
            print(f"Heure de fin : {event['end'].get('dateTime', event['end'].get('date'))}")
        else:
            print(f"L'événement avec l'ID {event_id} n'a pas été trouvé.")

        return event
    except Exception as e:
        print(f"Une erreur s'est produite lors de la récupération des détails de l'événement : {e}")
        return None

# Remplacez 'eventId' par l'ID de l'événement dont vous souhaitez obtenir les détails
event_id = 'gbvqiffjt5kvvki3mat8a78g10'
get_event_details(event_id)