import mysql.connector

# Connexion à la base de données
conn = mysql.connector.connect(
    host="localhost",  
    user="root",  
    password="",  
    database="liberalplanner" 
)

# Création d'un curseur
cursor = conn.cursor()

# test requette
requete = "SELECT * FROM patients"
cursor.execute(requete)

# Récupération des résultats
results = cursor.fetchall()

# Parcours des résultats
for row in results:
    print(row)

# Fermeture du curseur et de la connexion
cursor.close()
conn.close()
