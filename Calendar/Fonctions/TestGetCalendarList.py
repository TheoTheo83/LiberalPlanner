from SetupGoogle import get_calendar_service

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

if __name__ == '__main__':
   GetCalendarList()