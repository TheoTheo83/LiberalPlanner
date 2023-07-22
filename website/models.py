from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# table pour les notes
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# table pour les utilisateurs
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    prenom = db.Column(db.String(150))
    patients = db.relationship('Patient', backref='user')  # Relation avec les patients
    notes = db.relationship('Note')  # Relation avec les notes

# table pour les parents
class Parent(db.Model):
    ID_Parent = db.Column(db.Integer, primary_key=True)
    ID_Patients = db.Column(db.Integer, db.ForeignKey('patient.ID_Patients'))
    Prenom = db.Column(db.String(255))
    Nom = db.Column(db.String(255))

# table pour les pathologies
class Pathologie(db.Model):
    ID_Pathologie = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.ID_Patients'))
    Pathologie = db.Column(db.String(255))

# table pour les rendez-vous
class Rdv(db.Model):
    id_rdv = db.Column(db.Integer, primary_key=True)
    jourRdv = db.Column(db.Date(), nullable=False)
    ID_Patients = db.Column(db.Integer, db.ForeignKey('patient.ID_Patients'))  # Clé étrangère vers les patients

# table pour les patients
class Patient(db.Model):
    ID_Patients = db.Column(db.Integer, primary_key=True)
    Prenom = db.Column(db.String(255))
    Nom = db.Column(db.String(255))
    DateNaissance = db.Column(db.Date)
    Age = db.Column(db.Integer)
    remarques = db.Column(db.String(1000)) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    pathologies = db.relationship('Pathologie', backref='patient')
    parents = db.relationship('Parent', backref='patient')
    rdvs = db.relationship('Rdv', backref='patient')
