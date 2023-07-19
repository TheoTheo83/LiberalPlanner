from flask import Blueprint, render_template, request,flash, redirect,url_for
from .models import *
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user,current_user

auth = Blueprint('auth',__name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password =request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user :
            if check_password_hash(user.password,password):
                flash('Connection reussi!',category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else :
                flash('mot de passe incorrecte!',category='error')
        else : 
            flash('utilisateur inconnu !',category='error')

    return render_template("login.html",user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():

    if request.method == 'POST' :
        email = request.form.get('email')
        prenom = request.form.get('prenom')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('cet utilisateur existe déjà! veillez choisir un autre email',category='error')

        if len(email) < 4 :
            flash('email doit etre plus grand que 4 caracterers',category='error')
        elif len (prenom) < 2 :
            flash('le prenom doit etre plus grand que 2 caracterers',category='error')
        
        elif password1 != password2 :
            flash('les mdp ne correspondent pas ',category='error')

        elif len(password1) <5:
            flash ('mdp trop court min 6 caracteres', category= "error" )

        else :
            new_user = User(email=email, prenom=prenom,password=generate_password_hash(password1,method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('utilisateur creer ',category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html",user=current_user)