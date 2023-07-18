from flask import Blueprint, render_template, request,flash

auth = Blueprint('auth',__name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    data = request.form
    print(data)
    return render_template("login.html",text="test", user="luis")

@auth.route('/logout')
def logout():
    return "<p>logout<p>"

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():

    if request.method == 'POST' :
        email = request.form.get('email')
        prenom = request.form.get('prenom')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4 :
            flash('email doit etre plus grand que 4 caracterers',category='error')
        elif len (prenom) < 2 :
            flash('le prenom doit etre plus grand que 2 caracterers',category='error')
        
        elif password1 != password2 :
            flash('les mdp ne correspondent pas ',category='error')

        elif len(password1) <5:
            flash ('mdp trop court min 6 caracteres', category= "error" )

        else :
            flash('utilisateur creer ',category='success')


    return render_template("sign_up.html")