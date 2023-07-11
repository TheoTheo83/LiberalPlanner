import mysql.connector

# Configuration de la connexion à la base de données
config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_mysql_root_password',
    'database': 'patient_pratique'
}

# Établissement de la connexion
print('ON est là ---------')
connection = mysql.connector.connect(**config)
print('----------------')
# Vérification de la connexion
if connection.is_connected():
    print('Connecté à la base de données')
else:
    print('La connexion à la base de données a échoué')

# Exécution de requêtes
cursor = connection.cursor()

# Récupération de toute les données 
query = 'SELECT * FROM patients'
cursor.execute(query)

# Récupération des résultats
results = cursor.fetchall()

# Affichage des résultats
for row in results:
    print(row)

# Fermeture de la connexion
connection.close()
