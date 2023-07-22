from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    # Crée une instance de l'application Flask
    app = Flask(__name__)
    # Clé secrète utilisée pour la sécurité des sessions
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    # Configuration de la base de données SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # Initialise la base de données SQLAlchemy avec l'application
    db.init_app(app)

    # Importe les vues et l'authentification depuis les fichiers correspondants
    from .views import views
    from .auth import auth

    # Enregistre les blueprints pour les vues et l'authentification
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Importe les modèles User et Note depuis le fichier models.py
    from .models import User, Note
    
    # Crée la base de données si elle n'existe pas déjà
    create_database(app)

    # Initialise le gestionnaire de connexion pour gérer les sessions utilisateur
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Fonction pour charger un utilisateur à partir de son identifiant
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    # Vérifie si la base de données n'existe pas déjà et la crée si nécessaire
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Base de donnee cree!')
