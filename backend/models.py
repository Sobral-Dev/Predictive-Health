from config import db
from sqlalchemy import Column, Integer, String, Boolean, Text, TIMESTAMP, ForeignKey, DATE
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class User(db.Model):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    role = Column(String(20), nullable=False)
    consent_status = Column(Boolean, default=None)
    reset_token = Column(String(120))
    created_at = Column(TIMESTAMP, server_default=func.now())
    cpf = Column(String(11), unique=True, nullable=False)
    has_patient_history = Column(Boolean, default=False)

class Patient(db.Model):
    __tablename__ = 'Patient'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    age = Column(Integer)
    medical_conditions = Column(Text)
    consent_status = Column(Boolean, default=None)
    created_at = Column(TIMESTAMP, server_default=func.now())
    cpf = Column(String(11), unique=True, nullable=False)
    birth_date = Column(DATE, nullable=False)

class AuditLog(db.Model):
    __tablename__ = 'AuditLog'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.id', ondelete='CASCADE'), nullable=False)
    action = Column(String(255), nullable=False)
    timestamp = Column(TIMESTAMP, server_default=func.now())
    user = relationship('Users')

class RevokedToken(db.Model):
    __tablename__ = 'RevokedToken'
    id = Column(Integer, primary_key=True)
    jti = Column(String(120), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

class Doctorpatient(db.Model):
    __tablename__ = 'DoctorPatient'
    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer, ForeignKey('Users.id', ondelete='CASCADE'), nullable=False)
    patient_id = Column(Integer, ForeignKey('Patient.id', ondelete='CASCADE'), nullable=False)
    doctor = relationship('Users')
    patient = relationship('Patient')
    created_at = Column(TIMESTAMP, server_default=func.now())
