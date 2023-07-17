from SetupGoogle import get_calendar_service

def SuppEvent(event_id):

    service = get_calendar_service()

    try:
        # Supprimer l'événement
        service.events().delete(calendarId='primary', eventId=event_id).execute()
        print(f"L'événement avec l'ID {event_id} a été supprimé avec succès.")
    except Exception as e:
        print(f"Une erreur s'est produite lors de la suppression de l'événement : {e}")

if __name__ == '__main__':
    
    event_id = 'vs15qvqkpgnkbr624q8tc0ftu4'
    SuppEvent(event_id)