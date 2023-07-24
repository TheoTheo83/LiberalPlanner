#!/usr/bin/env python
# -*- coding: utf-8 -*-
from geopy.geocoders import Nominatim
import googlemaps
import geocoder

API_KEY = 'AIzaSyDahWp0ymxC_6E6sFcv5ih-9zB5xvui0OI'
PRIX_ESSENCE = 1.90 # En €
CONSOMMATION_VOITURE = 7/100 # xL/100km

# Fonction qui récupére l'adresse correspondant à une longitude et une latitude
def GetAdresse(latitude, longitude):

    # Démarre le service de localisation
    geolocator = Nominatim(user_agent="myGeocoder")

    # Recherche l'adressse avec la latitude et longitude
    location = geolocator.reverse(f"{latitude}, {longitude}", exactly_one=True)

    # Si une adresse à été trouvé
    if location:
        # On affiche l'adresse
        print(f"Adresse : {location}")
        # Et on la renvoi
        return location.address
    
    else:
        print("Impossible d'obtenir l'adresse.")
        return None

# Fonction qui récupére la longitude et la latitude de la position actuelle
def GetLocalisation():

    # Utilise le service de géolocalisation du système d'exploitation
    pos = geocoder.ip('me')

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
        return None

##### Fonction principale #####
def main():

    #Réccupère le temp, la distance et le cout en essence d'un trajet de A à B

    #Depart = "11 avenue de luminy, Marseille"
    #Arrivee = "2772 montée du vieux camp, Le Castellet"
    #GetItineraire(Depart, Arrivee)


    # Réccupère la latitude et longitude actuel, puis la converti en adresse
    latitude, longitude = GetLocalisation()
    GetAdresse(latitude, longitude)


if __name__ == '__main__':
    main()