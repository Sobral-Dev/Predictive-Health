import random
from bson import ObjectId
from datetime import datetime
from pymongo import MongoClient
from models.DoctorPatientModel import DoctorPatientModel
import json

# Conexão com o MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["PredictiveHealth"]

def save_relationships_to_json(relation_objects: list, filename="relations_data.json"):
    """Salva as relações doutor-paciente geradas em um arquivo JSON."""

    for relation in relation_objects:
        relation["_id"] = str(relation["_id"])
        relation['doctor_name'] = db.users.find_one({"_id": ObjectId(relation["doctor_id"])})["name"]
        relation['patient_name'] = db.patients.find_one({"_id": ObjectId(relation["patient_id"])})["name"]
        relation["doctor_id"] = str(relation["doctor_id"])
        relation["patient_id"] = str(relation["patient_id"])

    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(relation_objects, file, indent=4, ensure_ascii=False)
        print(f"✅ Relações salvas em {filename} com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao salvar relações: {e}")

def insert_doctor_patient_relationships():
    """Insere 25 relações médicas aleatórias entre médicos e pacientes, evitando duplicatas."""
    
    # Buscar médicos e pacientes do banco
    doctors = list(db.users.find({"role": "medico"}, {"_id": 1}))
    patients = list(db.patients.find({}, {"_id": 1}))

    if not doctors or not patients:
        print("❌ Não há médicos ou pacientes suficientes no banco de dados.")
        return

    relationships_json = []
    relationships = set()  
    inserted_count = 0  

    while inserted_count < 25:
        doctor = random.choice(doctors)
        patient = random.choice(patients)
        pair = (doctor["_id"], patient["_id"])

        # Verifica se a relação já existe no banco de dados e se não foi sorteada antes
        if pair not in relationships and not db.doctor_patient.find_one({"doctor_id": doctor["_id"], "patient_id": patient["_id"]}):
            consent_status = "accepted" if random.random() < 0.8 else "pending"

            relationship = DoctorPatientModel(
                doctor_id=doctor["_id"],
                patient_id=patient["_id"],
                consent_status=consent_status
            ).to_dict()

            db.doctor_patient.insert_one(relationship)
            relationships.add(pair)  # Adiciona ao conjunto de relações já inseridas
            relationships_json.append(relationship)
            inserted_count += 1  
    
    save_relationships_to_json(relationships_json)

    print(f"✅ {inserted_count} relações médico-paciente inseridas com sucesso!")

if __name__ == "__main__":
    insert_doctor_patient_relationships()