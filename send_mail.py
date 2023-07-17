from __future__ import print_function
import base64
import os.path
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


def authenticate_gmail():
    SCOPES = ['https://mail.google.com/']
    creds = None
    
    # Vérification de l'existence du fichier token.json
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # Si les informations d'identification ne sont pas valides, l'utilisateur doit se connecter
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('Projet_Python/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Sauvegarde des informations d'identification pour la prochaine exécution
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Création du service Gmail
    service = build('gmail', 'v1', credentials=creds)
    
    return service

def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}


def send_message(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message)
                   .execute())
        print('Message Id: %s' % message['id'])
        return message
    except Exception as error:
        print(error)

def mailGeneric(sender, to, medecin, date, entreprise, nomPrenom):
    subject = "Rappel de rendez-vous"
    message_text = "Cher Dr."+ medecin +",\n\nVoici le récapitulatif des rendez-vous prévus pour demain :\n\n1. Patient: "+ nomPrenom +"\nDate: "+ date +"\nTéléphone: [Numéro de Téléphone du Patient 1]\n\n2. Patient: [Nom du Patient 2]\nDate: [Date du Rendez-vous 2]\nTéléphone: [Numéro de Téléphone du Patient 2]\n\n[Votre Nom/Organisation]"
    service = authenticate_gmail()
    message = create_message(sender, to, subject, message_text)

    send_message(service, 'me', message)
    