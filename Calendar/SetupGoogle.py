import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar']

CREDENTIALS_FILE = 'Calendar/credentials.json'

def get_calendar_service():
   creds = None
   
   # Le fichier token.pickle stocke les token d’accès 
   # de l’utilisateur et est créé automatiquement
   # lorsque la première authentification avec Google API s'est déroulée


   if os.path.exists('token.pickle'):
       with open('token.pickle', 'rb') as token:
           creds = pickle.load(token)

   # Si il n'y a pas de credentials valide, l'utilisateur es invité a se connecté

   if not creds or not creds.valid:
       if creds and creds.expired and creds.refresh_token:
           creds.refresh(Request())
       else:
           flow = InstalledAppFlow.from_client_secrets_file(
               CREDENTIALS_FILE, SCOPES)
           creds = flow.run_local_server(port=0)

       # Sauvegarde du token pour le prochain lancement
       with open('token.pickle', 'wb') as token:
           pickle.dump(creds, token)

   service = build('calendar', 'v3', credentials=creds)
   return service