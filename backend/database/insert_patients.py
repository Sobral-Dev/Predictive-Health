from pymongo import MongoClient
import json
from models.PatientModel import PatientModel

# Conexão com o MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["PredictiveHealth"]

def insert_patients():
    """Lê os pacientes do arquivo JSON e insere no MongoDB."""

    try:
        # Ler os dados do arquivo JSON
        with open("patients_data.json", "r", encoding="utf-8") as file:
            patients_data = json.load(file)

        # Converter os dados para o formato do modelo
        patient_objects = [PatientModel(**patient).to_dict() for patient in patients_data]

        # Inserir no MongoDB
        db.patients.insert_many(patient_objects)
        print(f"✅ {len(patient_objects)} pacientes inseridos com sucesso!")

    except Exception as e:
        print(f"❌ Erro ao inserir pacientes: {str(e)}")


if __name__ == "__main__":
    insert_patients()