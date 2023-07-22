from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login() :
    return render_template("login.html", boolean = True)

@auth.route('/logout')
def logout () :
    return render_template("home.html")

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash('Email trop court !', category = 'error')
        elif len(firstName) < 2:
            flash('Prénom trop court !', category = 'error')
        elif password1 != password2:
            flash('Les mots de passe ne correspondent pas !', category = 'error')
        elif len(password1) < 7:
            flash('Mot de passe trop court !', category = 'error')
        else:
            #Creation de l'utilisateur
            flash('Compte crée avec succés !', category = 'succes')

    return render_template("sign_up.html")