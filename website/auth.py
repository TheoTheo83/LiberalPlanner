from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import *
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

# Crée un Blueprint pour les routes d'authentification
auth = Blueprint('auth', __name__)

# Route pour la connexion d'un utilisateur
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Récupère les informations de l'utilisateur depuis le formulaire de connexion
        email = request.form.get('email')
        password = request.form.get('password')

        # Vérifie si l'utilisateur existe dans la base de données
        user = User.query.filter_by(email=email).first()
        if user:
            # Vérifie si le mot de passe fourni correspond au mot de passe haché dans la base de données
            if check_password_hash(user.password, password):
                flash('Connexion réussie!', category='success')
                login_user(user, remember=True)  # Connecte l'utilisateur en utilisant Flask-Login
                return redirect(url_for('views.home'))
            else:
                flash('Mot de passe incorrect!', category='error')
        else:
            flash('Utilisateur inconnu!', category='error')

    return render_template("login.html", user=current_user)

# Route pour la déconnexion de l'utilisateur
@auth.route('/logout')
@login_required  # Nécessite une connexion pour accéder à cette route
def logout():
    logout_user()  # Déconnecte l'utilisateur en utilisant Flask-Login
    return redirect(url_for('auth.login'))

# Route pour l'inscription d'un nouvel utilisateur
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        # Récupère les informations de l'utilisateur depuis le formulaire d'inscription
        email = request.form.get('email')
        prenom = request.form.get('prenom')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # Vérifie si l'utilisateur existe déjà dans la base de données
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Cet utilisateur existe déjà! Veuillez choisir un autre email.', category='error')

        # Vérifie la validité des informations fournies
        if len(email) < 4:
            flash('L\'email doit comporter plus de 4 caractères.', category='error')
        elif len(prenom) < 2:
            flash('Le prénom doit comporter plus de 2 caractères.', category='error')
        elif password1 != password2:
            flash('Les mots de passe ne correspondent pas.', category='error')
        elif len(password1) < 5:
            flash('Le mot de passe est trop court (minimum 6 caractères).', category='error')
        else:
            # Crée un nouvel utilisateur et l'ajoute à la base de données
            new_user = User(email=email, prenom=prenom, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)  # Connecte automatiquement le nouvel utilisateur
            flash('Utilisateur créé avec succès.', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
