from SetupGoogle import get_calendar_service

# Fonction qui réccupère l'ID d'un événement grace à son nom
def GetEventId(event_title):

    # Appel de l'API
    service = get_calendar_service()

    try:
        # Obtenir la liste des événements du calendrier par default
        events = service.events().list(calendarId='primary').execute()
        
        cpt = 0
        # Parcour les événements pour trouver l'ID de l'événement recherché
        for event in events['items']:
            if event['summary'] == event_title:
                cpt+=1
                if cpt < 2:
                    print(f"L'ID de l'événement '{event_title}' est : {event['id']}")

                else:
                    print(f"L'ID de l'événement '{event_title}' est : {event['id']}")
                    print(f"L'événement '{event_title}' existe plusieurs fois, présicer la recherche")
                    return None

            else:
                # Si l'événement n'a pas été trouvé, renvoie None
                print(f"L'événement '{event_title}' n'a pas été trouvé.")
                return None
        if cpt < 2 :
            return event['id']
            
    # Gère les exeptions
    except Exception as e:
        print(f"Une erreur s'est produite lors de la récupération de l'ID de l'événement : {e}")
        return None

if __name__ == '__main__':

    # Remplacez 'event_title' par le titre de l'événement dont vous souhaitez obtenir l'ID
    event_title = 'Test'
    event_id = GetEventId(event_title)