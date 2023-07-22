from __future__ import print_function
import base64
import os.path
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from datetime import datetime
import time
import schedule


def authGmail():
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
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Sauvegarde des informations d'identification pour la prochaine exécution
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Création du service Gmail
    service = build('gmail', 'v1', credentials=creds)
    
    return service

def createMessage(sender: str, to: str, subject: str, message_text: str):
    message = MIMEText(message_text)
    # to = le destinataire 
    message['to'] = to
    # l'adresse email qui envoie le mail
    message['from'] = sender
    # le sujet du mail
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}


def sendMessage(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message)
                   .execute())
        print('Message Id: %s' % message['id'])
        
        return message
    except Exception as error:
        print(error)
        

def mail(sender: str, to: str, subject:str , message_text:str ) -> None:
    
    service = authGmail()
    message = createMessage(sender, to, subject, message_text)

    sendMessage(service, 'me', message)