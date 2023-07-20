from flask import Blueprint, render_template, request, flash, jsonify,redirect,url_for
from flask_login import login_required,current_user
from .models import Note, Patient,Pathologie,Remarque
from . import db 
import json 
from datetime import datetime

views = Blueprint('views',__name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('note trop petite', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('note cree', category='success')

    # Récupérer la liste des patients associés à l'utilisateur actuellement connecté
    patients = Patient.query.filter_by(user_id=current_user.id).all()

    return render_template("home.html", user=current_user, patients=patients)

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

@views.route('/add-patient', methods=['POST'])
@login_required
def add_patient():
    nom = request.form.get('nom')
    prenom = request.form.get('prenom')
    date_naissance_str = request.form.get('date_naissance')
    

    if date_naissance_str:
        try:
            date_naissance = datetime.strptime(date_naissance_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Format de date invalide. Utilisez le format AAAA-MM-JJ.', category='error')
            return redirect(url_for('views.home'))
    else:
        date_naissance = None

    age = request.form.get('age')

    if len(nom) < 1 or len(prenom) < 1 or (date_naissance_str and len(date_naissance_str) == 0) or (date_naissance_str and len(age) < 1):
        flash('Veuillez remplir tous les champs du formulaire.', category='error')
    else:
        new_patient = Patient(Nom=nom, Prenom=prenom, DateNaissance=date_naissance, Age=age, user_id=current_user.id)  # Assurez-vous d'inclure user_id ici
        db.session.add(new_patient)
        db.session.commit()
        flash('Patient ajouté avec succès.', category='success')

    return redirect(url_for('views.home'))


@views.route('/patient', methods=['GET', 'POST'])
@login_required
def patient():
    patients = Patient.query.filter_by(user_id=current_user.id).all()
    pathologies = {}
    remarques = {}
    for patient in patients:
        pathologies[patient.ID_Patients] = Pathologie.query.filter_by(patient_id=patient.ID_Patients).all()
        remarques[patient.ID_Patients] = Remarque.query.filter_by(patient_id=patient.ID_Patients).all()

    if request.method == 'POST':
        patient_id = request.form.get('patient_id')
        pathologie_data = request.form.get('pathologie')
        remarque_data = request.form.get('remarque')

        if patient_id and pathologie_data:
            new_pathologie = Pathologie(patient_id=patient_id, Pathologie=pathologie_data)
            db.session.add(new_pathologie)

        if patient_id and remarque_data:
            new_remarque = Remarque(patient_id=patient_id, Remarque=remarque_data)
            db.session.add(new_remarque)

        db.session.commit()
        flash('Pathologie et/ou remarque ajoutée avec succès.', category='success')
        return redirect(url_for('views.patient'))
    patient = patients[0] if patients else None
    return render_template("patient.html", user=current_user, patients=patients, pathologies=pathologies, remarques=remarques, patient=patient)

