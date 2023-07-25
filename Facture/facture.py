from jinja2 import Environment, FileSystemLoader, Template
import subprocess
import os
from typing import Dict, Tuple


def openTex(templatFile) -> Tuple[Environment, Template]:

    # Créez l'environnement de rendu avec le répertoire du script Python comme chemin pour les modèles
    env = Environment(loader=FileSystemLoader("./template"),variable_start_string='**', variable_end_string='**')
    
    # Chargez le modèle à partir de l'environnement, il doit forcément y avoir un dossier "/template" avec les modèles.tex dedans
    template = env.get_template(templateFile)
    
    return (env, template)


def changeData(data: Dict, template_file):
    env, template = openTex(template_file)

    developments = ""

    for elt in data['developments']:
        if developments != "":
            developments +="}\Fee{"
        developments += elt['description'] + "}{" + elt['amount']+ "}{" + elt['quantity']

    data['developments'] = developments
    
    output = template.render(data=data)  # Passer le dictionnaire 'data' en tant que contexte

    return output



# Cette fonction permet de rajouter une ligne sur la facture
def addElement(data:Dict, description: str, amount: int, quantity: int) -> Dict:

    # un dictionnaire identique à ce qu'on peut trouver dans la data.
    new_element = {
        "description": description,
        "amount": amount,
        "quantity": quantity
    }

    # rajout de ce dictionnaire dans la data, rajout à la suite de ce qu'il y a déjà
    data["developments"].append(new_element)

    return data


def saveTex(output, outputFile) -> None:

    # Si le dossier "facture " n'existe pas alors on le créait 
    if not os.path.exists('facture'):
        os.mkdir('facture')

    # Ouvre le fichier en mode écriture et on vient écrire les modifications que l'on aura fait.
    with open(outputFile, "w") as file:
        file.write(output)


def convertTexToPdf(texFile, name: str) -> None:

    # Cette ligne lance la commande pdflatex convertis donc le fichier qu'on aura sélectionner
    # A SAVOIR QUE LE FICHIER .tex DOIT ÊTRE PRÉSENT DANS LE DOSSIER OU SE TROUVE LES SCRIPTS
    subprocess.run(["pdflatex", "-output-directory=facture", "--jobname="+name, "--interaction=batchmode"], input=texFile.encode())


if __name__ == '__main__':
    
    # template : https://www.overleaf.com/latex/templates?q=invoice https://www.overleaf.com/project/64b7c41474711532d89d6eb5

    templateFile = 'facture.tex'

    # La data suivante est les différentes information présent sur la facture, il faut modifier après les deux points pour 
    # ajouter les informations que l'on veut. On ne peut pas modifier ce qu'il y a devant par exemple "My Name".
    data = {
    "My Name": "Benoit LICATESI",
    "My Street": "Marseille",
    "My Zip": "13011",
    "my@mail.com": "benoit.licatesi@gmail.com",
    "Fnord Prefake": " LICATESI Benoit",
    "23. May 2009": "01. July 2023",
    "Customer name": "x",
    "Customer street": "x",
    "Customer ZIP": "66",
    "Invoice no. 1": "00001",
    "Example Project": "FACTURE",
    "developments": [
            {
                "description": "Mise au point équipement informatique",
                "amount": "750.00",
                "quantity": "1"
            },
        ],
    "My Closing": "Cabinet pratique"
    }

    
    # Utilisation de la fonction changeData pour remplacer les données dans le modèle LaTeX

    # Ajout d'une nouvelle ligne dans la description de facture
    data = addElement(data, "Réparation ordinateur", "80.00", "2")

    # Utilisation de la fonction changeData pour remplacer les données dans le modèle LaTeX
    output = changeData(data, templateFile)

    # nom du fichier qui va être utilisé pour créer notre facture et pour la convertir en pdf. 
    # Lors de la création du pdf elle ne gardera pas ce nom, dans la fonction convertTexToPdf(),
    # il faut lui spécifier le nom qu'on veut.
    output_file = "factureBenoit.tex"

    # Enregistrement du modèle mis à jour dans un fichier .tex qu'on choisi dans le second argument
    saveTex(output, output_file)

    # # Conversion du fichier .tex en PDF
    convertTexToPdf(output_file, 'factureBenoit')