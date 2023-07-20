#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from SetupGoogle import get_calendar_service


# Mettre à jour un événement existant grace à son ID
def EditEvent(event_title, event_new_location, event_description,event_new_summary, event_new_start, event_new_end):

    # Appel de l'API Google
    service = get_calendar_service()
    
    # Réccupération de l'ID de l'événement grace au titre
    event_id = GetEventId(event_title)

    # Test si le résultat est différent de None donc si l'événement à été trouvé
    if event_id != None:

        # Si il a été trouvé, on modifie l'événement avec les nouvelles informations
        event_result = service.events().update(
                calendarId='primary',
                eventId= event_id ,
                body={
                "summary": event_new_summary,
                "location": event_new_location,
                "description": event_description,
                "start": {"dateTime": event_new_start, "timeZone": 'Europe/Paris'},
                "end": {"dateTime": event_new_end, "timeZone": 'Europe/Paris'},
                },
            ).execute()

        # Affichage de l'événement modifier
        print("Evénement modifier :")
        print("id: ", event_result['id'])
        print("summary: ", event_result['summary'])
        print("location: ", event_result['location'])
        print("description: ", event_result['description'])
        print("starts at: ", event_result['start']['dateTime'])
        print("ends at: ", event_result['end']['dateTime'])

        # On renvoi l'événement modifier
        return event_result
    else:
        print("Aucun événement portant ce nom a été trouvé !")

# Réccupère les détails d'un évémenement grace à son ID
def GetEventDetails(event_title):

    # Appel de l'API Google
    service = get_calendar_service()

    # On cherche l'ID de l'événement avec son nom
    event_id = GetEventId(event_title)

    # On test si event_id est différent de None
    if event_id != None:

        # Si c'est le cas on essaye d'afficher les détails de l'événement
        try:
            # On réccupére les détails de l'événement spécifié par son ID
            event = service.events().get(calendarId='primary', eventId=event_id).execute()

            # Si on a bien un résultat, on affiche les détails de l'événement
            if event:
                print("Détails de l'événement :")
                print(f"Titre : {event['summary']}")
                print(f"Emplacement : {event.get('location', 'N/A')}")
                print(f"Description : {event.get('description', 'N/A')}")
                print(f"Heure de début : {event['start'].get('dateTime', event['start'].get('date'))}")
                print(f"Heure de fin : {event['end'].get('dateTime', event['end'].get('date'))}")
            return event
        # On gére l'exception au cas ou une erreur se produit
        except Exception as e:
            print(f"Une erreur s'est produite lors de la récupération des détails de l'événement : {e}")
            return None
    # Si event_id est égale à None, cela veut dire que l'événement n'a pas été trouvé
    else:
        #  On informe l'utilisateur
        print(f"Aucun événement portant le nom de {event_title} à été trouvé")

# Fonction qui permet de lister tous les noms et IDs des calendriers existants.
def GetCalendarList():
   
   # Appel de l'API Calendar
   service = get_calendar_service()

   print('Liste des Calendrier existant :\n')

   # Requette qui récuppère la liste des calendriers
   calendars_result = service.calendarList().list().execute()

   # Sépare le résultat de la requette en tableau d'éléments ("calendars")
   calendars = calendars_result.get('items', [])

   # On test si le resultat est vide
   if not calendars:
       # Si c'est le cas on affiche un message d'alerte
       print('Aucun calendrier trouvé !')
   # Sinon on fait une boucle qui parcour les différents calendriers
   for calendar in calendars:
       summary = calendar['summary']
       id = calendar['id']
       primary = "Primary" if calendar.get('primary') else ""

       # On affiche le nom, l'id du calendrier. Et si c'est le calendrier par default
       print("%s\t%s\t%s" % (summary, id, primary))

# Fonction qui réccupère l'ID d'un événement grace à son nom
def GetEventId(event_title):

    # Appel de l'API
    service = get_calendar_service()

    try:
        # Obtenir la liste des événements du calendrier par default
        events = service.events().list(calendarId='primary').execute()
        
        # Parcour les événements obtenu
        for event in events['items']:
            # Si le nom recherché correspond au nom de l'événement actuellement parcouru
            if event['summary'] == event_title:
                # Alors on renvoi l'ID de l'événement
                return event['id']
            # Si aucun événement ne porte ce nom
            else:
                # On renvoi None
                return None
            
    # Gère les exeptions
    except Exception as e:
        # Informe l'utilisateur en cas d'erreur
        print(f"Une erreur s'est produite lors de la récupération de l'ID de l'événement : {e}")
        # Et renvoi None
        return None

# Réccupère la liste des 100 prochains événements
def GetEventList(max_results):
   
    # Appel de l'API Google
    service = get_calendar_service()
   
    # On réccupére l'heure et la date actuel
    now = datetime.datetime.utcnow().isoformat() + 'Z'
   
    # On réccupére les prochains événements du calendrier
    events_result = service.events().list(calendarId='primary', timeMin=now, maxResults=max_results, singleEvents=True, orderBy='startTime').execute()

    # On sépare le résultat en tableau d'éléments
    events = events_result.get('items', [])

    # Si le tableau est vide on informe l'utilisateur et on sort de la fonction
    if not events:
        print("Aucun événements trouvé")
        exit
    
    # Sinon on parcours chaque éléments et on affiche ces informations
    for event in events:
        event_summary = event.get('summary', 'N/A')
        start_time = event['start'].get('dateTime', event['start'].get('date', 'N/A'))
        end_time = event['end'].get('dateTime', event['end'].get('date', 'N/A'))
        print(f"Titre : {event_summary}")
        print(f"Date de début : {start_time}")
        print(f"Date de fin : {end_time}")
        print("--------")

    # On renvoi le tableau d'événements
    return events

# Permet d'ajouter un événement au calendrier
def InsertEvent(summary, location, description, sDateTime, eDateTime) :

    # Appel de l'API Google
    service = get_calendar_service()

    # Créé un objet event avec les information de l'événement
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

    # Requette d'insertion de l'événement dans l'agenda 
    event = service.events().insert(calendarId='primary', body=event).execute()

    # On informe l'utilisateur que l'événement à bien été créé et on affiche le lien vers l'événement
    print(f'Événement {summary} créé : {event.get("htmlLink")}')

    # On renvoi l'événement
    return event

# Permet de supprimer un événement
def SuppEvent(event_title):

    # Appel de l'API Google
    service = get_calendar_service()

    # On réccupére l'ID de l'événement grace à son titre
    event_id = GetEventId(event_title)

    if event_id :

        try:
            # Requette de suppression de l'événement
            service.events().delete(calendarId='primary', eventId=event_id).execute()

            # On informe l'utilisateur que l'événement à bien été supprimé
            print(f"L'événement {event_title} a été supprimé avec succès.")

        # On gére si une erreur s'est produite
        except Exception as e:
            print(f"Une erreur s'est produite lors de la suppression de l'événement : {e}")


##### Fonction principale #####
def main():

    #Evenement = input("Tapez le nom de l'événement : ")

    #InsertEvent('Test', 'Marseille', 'C est un test Marseillais', '2023-07-18T18:00:00', '2023-07-18T19:00:00')
    # GetEventDetails('Test')
    # EditEvent('Test', 'Paris', 'Test de description du turfu','TestTheo', '2023-07-20T18:00:00', '2023-07-20T19:00:00')
    # GetEventDetails('TestTheo')
    SuppEvent('Theo')
    # GetEventList(10) # Donne le prochain événements

if __name__ == '__main__':
    main()