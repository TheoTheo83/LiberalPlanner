from jinja2 import Environment, FileSystemLoader
import subprocess


def openTex(templatFile):
    # Créez l'environnement de rendu avec le répertoire du script Python comme chemin pour les modèles
    env = Environment(loader=FileSystemLoader("./"),variable_start_string='**', variable_end_string='**')

    # Chargez le modèle à partir de l'environnement
    template = env.get_template(templateFile)

    return env, template


def changeData(data, template_file):
    env, template = openTex(template_file)

    output = template.render(data=data)  # Passer le dictionnaire 'data' en tant que contexte
    return output




def showTex():
    ...


def saveTex(output, outputFile):
    with open(outputFile, "w") as file:
        file.write(output)


def convertTexToPdf(texFile):

    # Cette ligne lance la commande pdflatex convertis donc le fichier qu'on aura sélectionner
    # A SAVOIR QUE LE FICHIER .tex DOIT ÊTRE PRÉSENT DANS LE DOSSIER OU SE TROUVE LES SCRIPTS
    subprocess.run(["pdflatex", "-output-directory=output", "--jobname=facture", "--interaction=batchmode"], input=texFile.encode())


if __name__ == '__main__':
    #convertTexToPdf(templateFile)
    #openTex(templateFile)

    # template : https://www.overleaf.com/latex/templates?q=invoice https://www.overleaf.com/project/64b7c41474711532d89d6eb5

    templateFile = 'facture.tex'

    data = {
    "My Name": "Benoit LICATESI",
    "My Street": "Marseille",
    "My Zip": "13011",
    "my@mail.com": "benoit.licatesi@gmail.com",
    "Fnord Prefake": "Votre nom",
    "23. May 2009": "01. July 2023",
    "Customer name": "Flash MCQUEEN",
    "Customer street": "Radiator Springs",
    "Customer ZIP": "66",
    "Invoice no. 1": "00001",
    "My greeting": "Bonjour,",
    "Example Project": "Facture",
    "Development": "Changement de pneu",
    "1000.00": "500.00",
    "1": "4",
    "My Closing": "Au revoir"
    }

    # Utilisation de la fonction changeData pour remplacer les données dans le modèle LaTeX
    output = changeData(data,templateFile)

    # Enregistrement du modèle mis à jour dans un fichier .tex
    output_file = "factureBenoit.tex"
    saveTex(output, output_file)
    
    # Conversion du fichier .tex en PDF
    convertTexToPdf(output_file)