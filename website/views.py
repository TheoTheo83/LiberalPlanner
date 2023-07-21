from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, Patient, Pathologie
from . import db
import json
from datetime import datetime

views = Blueprint('views', __name__)

# Page d'accueil
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    # Gestion des notes
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Note trop petite', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note créée', category='success')

    # Récupérer la liste des patients associés à l'utilisateur actuellement connecté
    patients = Patient.query.filter_by(user_id=current_user.id).all()

    return render_template("home.html", user=current_user, patients=patients)

# Supprimer une note
@views.route('/delete-note', methods=['POST'])
def delete_note():
    note_data = json.loads(request.data)
    note_id = note_data['noteId']
    note = Note.query.get(note_id)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})

# Supprimer un patient
@views.route('/delete-patient', methods=['POST'])
@login_required
def delete_patient():
    patient_data = json.loads(request.data)
    patient_id = patient_data['patientId']
    patient = Patient.query.get(patient_id)

    if patient:
        if patient.user_id == current_user.id:
            # Supprimer les pathologies liées au patient (s'il y en a)
            Pathologie.query.filter_by(patient_id=patient_id).delete()

            # Supprimer le patient lui-même
            db.session.delete(patient)
            db.session.commit()

    return jsonify({})

# Ajouter un patient
@views.route('/add-patient', methods=['POST'])
@login_required
def add_patient():
    nom = request.form.get('nom')
    prenom = request.form.get('prenom')
    date_naissance_str = request.form.get('date_naissance')
    remarque= request.form.get('remarque')
    
    if date_naissance_str:
        try:
            date_naissance = datetime.strptime(date_naissance_str, '%Y-%m-%d').date()
            # Calculer l'âge à partir de la date de naissance et la date actuelle
            age = (datetime.now().date() - date_naissance).days // 365
        except ValueError:
            flash('Format de date invalide. Utilisez le format AAAA-MM-JJ.', category='error')
            return redirect(url_for('views.home'))
    else:
        date_naissance = None
        age = None
        
    if len(nom) < 1 or len(prenom) < 1 or (date_naissance_str and len(date_naissance_str) == 0) or (date_naissance_str == 0):
        flash('Veuillez remplir tous les champs du formulaire.', category='error')
    else:
        new_patient = Patient(Nom=nom, Prenom=prenom, DateNaissance=date_naissance, Age=age,remarques=remarque, user_id=current_user.id)
        db.session.add(new_patient)
        db.session.commit()
        flash('Patient ajouté avec succès.', category='success')

    return redirect(url_for('views.home'))

# Gérer les patients et leurs informations
@views.route('/patient', methods=['GET', 'POST'])
@login_required
def patient():
    patients = Patient.query.filter_by(user_id=current_user.id).all()
    return render_template("patient.html", user=current_user, patients=patients, patient=patient)

@views.route('/add-pathologie/', methods=['GET'])
@login_required
def add_pathologie():
    return render_template('pathologie.html', user=current_user)

@views.route('/add-pathologie', methods=['POST'])
@login_required
def add_pathologie_post():
    pathologie_data = request.form.get('pathologie')

    if pathologie_data:
        new_pathologie = Pathologie( Pathologie=pathologie_data)
        db.session.add(new_pathologie)
        db.session.commit()
        flash('Pathologie ajoutée avec succès.', category='success')

    return redirect(url_for('views.add_pathologie'))