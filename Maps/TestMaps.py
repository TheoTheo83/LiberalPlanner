#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime 
from geopy.geocoders import Nominatim
import googlemaps
import geocoder

API_KEY = 'AIzaSyDahWp0ymxC_6E6sFcv5ih-9zB5xvui0OI'
PRIX_ESSENCE = 1.90 # En €
CONSOMMATION_VOITURE = 7/100 # xL/100km


def GetAdresse(latitude, longitude):
    geolocator = Nominatim(user_agent="myGeocoder")
    location = geolocator.reverse(f"{latitude}, {longitude}", exactly_one=True)
    if location:
        print(f"Adresse : {location}")
        return location.address
    else:
        print("Impossible d'obtenir l'adresse.")
        return None

def GetLocalisation():
    pos = geocoder.ip('me')  # Utilise le service de géolocalisation du système d'exploitation
    if pos.latlng is not None:
        latitude, longitude = pos.latlng
        if latitude and longitude:
            print(f"Latitude : {latitude}")
            print(f"Longitude : {longitude}")
            return latitude, longitude
        else:
            print("Impossible de récupérer la position actuelle.")
    else:
        return None

def GetItineraire(Depart, Arrivee) :

    gmaps = googlemaps.Client(key=API_KEY)

    # Convertir l'heure d'arrivée en objet datetime
    if isinstance(arrival_time, str):
        arrival_time = datetime.strptime(arrival_time, '%Y-%m-%d %H:%M:%S')
    
    # Obtenir les directions entre le point A (origin) et le point B (destination)
    directions_result = gmaps.directions(Depart, Arrivee ,mode="driving")
    
    if directions_result:

        # Extraire le temps de trajet et la distance du premier itinéraire trouvé
        route = directions_result[0]
        duration = route['legs'][0]['duration']['text']
        distance = route['legs'][0]['distance']['text']
 
        distance = distance.translate(str.maketrans('', '', 'km'))

        cout = CONSOMMATION_VOITURE * float(distance) * PRIX_ESSENCE

        cout = round(cout, 2)

        # Afficher le temps de trajet et la distance
        if duration and distance:
            print(f"Temps de trajet : {duration}")
            print(f"Distance : {distance}")
            print(f"Cout essence : {cout}€")
        else:
            print("Impossible de trouver un itinéraire.")
        
        return duration, distance, cout
    else:
        return None, None

##### Fonction principale #####
def main():

    #Depart = "11 avenue de luminy, Marseille"
    #Arrivee = "2772 montée du vieux camp, Le Castellet"
    #GetItineraire(Depart, Arrivee)

    latitude, longitude = GetLocalisation()

    GetAdresse(latitude, longitude)


if __name__ == '__main__':
    main()