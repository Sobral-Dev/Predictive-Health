from config import db
from sqlalchemy import Column, Integer, String, Boolean, Text, TIMESTAMP, ForeignKey, DATE, Sequence
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

# Sequence para IDs
user_id_seq = Sequence('user_id_seq', start=1, increment=10)
patient_id_seq = Sequence('patient_id_seq', start=1000, increment=15)
auditlog_id_seq = Sequence('auditlog_id_seq', start=5000, increment=20)
doctorpatient_id_seq = Sequence('doctorpatient_id_seq', start=10000, increment=25)

class User(db.Model):
    __tablename__ = 'Users'
    id = Column(Integer, user_id_seq, primary_key=True, server_default=user_id_seq.next_value())
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
    id = Column(Integer, patient_id_seq, primary_key=True, server_default=patient_id_seq.next_value())
    name = Column(String(50), nullable=False)
    age = Column(Integer)
    medical_conditions = Column(Text)
    consent_status = Column(Boolean, default=None)
    created_at = Column(TIMESTAMP, server_default=func.now())
    cpf = Column(String(11), unique=True, nullable=False)
    birth_date = Column(DATE, nullable=False)

class AuditLog(db.Model):
    __tablename__ = 'AuditLog'
    id = Column(Integer, auditlog_id_seq, primary_key=True, server_default=auditlog_id_seq.next_value())
    user_id = Column(Integer, ForeignKey('Users.id', ondelete='CASCADE'), nullable=False)
    action = Column(String(255), nullable=False)
    timestamp = Column(TIMESTAMP, server_default=func.now())
    user = relationship('User')

class RevokedToken(db.Model):
    __tablename__ = 'RevokedToken'
    id = Column(Integer, primary_key=True)
    jti = Column(String(120), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

class DoctorPatient(db.Model):
    __tablename__ = 'DoctorPatient'
    id = Column(Integer, doctorpatient_id_seq, primary_key=True, server_default=doctorpatient_id_seq.next_value())
    doctor_id = Column(Integer, ForeignKey('Users.id', ondelete='CASCADE'), nullable=False)
    patient_id = Column(Integer, ForeignKey('Patient.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    doctor = relationship('User', foreign_keys=[doctor_id])
    patient = relationship('Patient', foreign_keys=[patient_id])
