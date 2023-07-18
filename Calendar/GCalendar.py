#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from SetupGoogle import get_calendar_service


# Mettre à jour un événement existant grace à son ID
def EditEvent(event_title, event_new_location, event_description,event_new_summary, event_new_start, event_new_end):

    service = get_calendar_service()
    
    event_id = GetEventId(event_title)
    if event_id != None:
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

        print("updated event")
        print("id: ", event_result['id'])
        print("summary: ", event_result['summary'])
        print("starts at: ", event_result['start']['dateTime'])
        
        print("ends at: ", event_result['end']['dateTime'])
        return event_result
    else:
        print("Aucun événement portant ce nom a été trouvé !")

# Réccupère les détails d'un évémenement grace à son ID
def GetEventDetails(event_title):

    service = get_calendar_service()

    event_id = GetEventId(event_title)

    if event_id != None:
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

# Fonction qui permet de lister tous les noms et IDs des calendriers existants.
def GetCalendarList():
   
   # Appel de l'API Calendar
   service = get_calendar_service()

   print('Liste des Calendrier existant :\n')

   # Requette qui récuppère la liste des calendriers
   calendars_result = service.calendarList().list().execute()

   # Sépare le résultat de la requette en "items"
   calendars = calendars_result.get('items', [])

   # On test si le resultat est vide
   if not calendars:
       # Si c'est le cas on affiche un message d'alerte
       print('Aucun calendrier trouvé !')
   # Sinon on fait une boucle qui parcour les "items"
   for calendar in calendars:
       summary = calendar['summary']
       id = calendar['id']
       primary = "Primary" if calendar.get('primary') else ""
       print("%s\t%s\t%s" % (summary, id, primary))

# Fonction qui réccupère l'ID d'un événement grace à son nom
def GetEventId(event_title):

    # Appel de l'API
    service = get_calendar_service()

    try:
        # Obtenir la liste des événements du calendrier par default
        events = service.events().list(calendarId='primary').execute()
        
        # Parcour les événements pour trouver l'ID de l'événement recherché
        for event in events['items']:
            if event['summary'] == event_title:
                # print(f"L'ID de l'événement '{event_title}' est : {event['id']}")
                return event['id']
            else:
                # Si l'événement n'a pas été trouvé, renvoie None
                return None
            
    # Gère les exeptions
    except Exception as e:
        print(f"Une erreur s'est produite lors de la récupération de l'ID de l'événement : {e}")
        return None

# Réccupère la liste de tout les événement d'un calendrier
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

# Permet d'ajouter un événement au calendrier
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

# Permet de supprimer un événement
def SuppEvent(event_title):

    service = get_calendar_service()

    event_id = GetEventId(event_title)

    try:
        # Supprimer l'événement
        service.events().delete(calendarId='primary', eventId=event_id).execute()
        print(f"L'événement avec l'ID {event_id} a été supprimé avec succès.")
    except Exception as e:
        print(f"Une erreur s'est produite lors de la suppression de l'événement : {e}")


##### Fonction principale #####
def main():

    #InsertEvent('Test', 'Marseille', 'C est un test Marseillais', '2023-07-18T18:00:00', '2023-07-18T19:00:00')
    #SuppEvent('Test')
    EditEvent('Test', 'Marseille', 'Test de description','TestTheo', '2023-07-18T18:00:00', '2023-07-18T20:00:00')
    GetEventDetails('TestTheo')



if __name__ == '__main__':
    main()