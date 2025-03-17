from pymongo import MongoClient
from insert_users import insert_users
from insert_patients import insert_patients
from insert_doctor_patient import insert_doctor_patient_relationships
from insert_prediction_data import insert_prediction_data
from insert_consent_terms import insert_consent_terms

# Conexão com o MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["PredictiveHealth"]

# Função para limpar os dados antes de inserir novos (evita duplicações)
def clear_database():
    db.users.delete_many({})
    db.patients.delete_many({})
    db.doctor_patient.delete_many({})
    db.consent_terms.delete_many({})
    db.audit_logs.delete_many({})
    db.user_consents.delete_many({})
    db.jwt_keys.delete_many({})
    db.revoked_tokens.delete_many({})
    db.prediction_data.delete_many({})
    print("📢 Banco de dados limpo!")

# Executando o script
if __name__ == "__main__":
    clear_database()
    insert_users()
    insert_patients()
    insert_doctor_patient_relationships()
    insert_consent_terms()
    insert_prediction_data()
    print("🚀 Banco de dados inicializado com sucesso!")
