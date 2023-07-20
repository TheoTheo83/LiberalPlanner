from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required,current_user
from .models import Note, Patient
from . import db 
import json 

views = Blueprint('views',__name__)

@views.route('/',methods=['GET','POST'])
@login_required

def home():
    if request.method== 'POST':
        note= request.form.get('note')

        if len(note)<1 :
            flash('note trop petite ',category='error')
        else :
            new_note = Note(data=note , user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('note cree',category='success')
    return render_template("home.html",user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note=json.loads(request.data)
    noteId= note['noteId']
    note=Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id :
            db.session.delete(note)
            db.session.commit()
    return jsonify({})

@views.route('/', methods=['POST'])
@login_required
def add_patient():
    nom = request.form.get('nom')
    prenom = request.form.get('prenom')
    date_naissance = request.form.get('date_naissance')
    age = request.form.get('age')

    if len(nom) < 1 or len(prenom) < 1 or len(date_naissance) < 1 or len(age) < 1:
        flash('Veuillez remplir tous les champs du formulaire.', category='error')
    else:
        new_patient = Patient(nom=nom, prenom=prenom, DateNaissance=date_naissance, Age=age)
        db.session.add(new_patient)
        db.session.commit()
        flash('Patient ajouté avec succès.', category='success')

    return render_template("home.html",user=current_user)

