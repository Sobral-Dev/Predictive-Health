from bson import ObjectId
from pymongo import ASCENDING, DESCENDING, TEXT, MongoClient

# Conexão com o MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["PredictiveHealth"]

# Listagem de coleções disponíveis
collections = {
    "users": db.users,
    "patients": db.patients,
    "prediction_data": db.prediction_data,
    "user_consents": db.user_consents,
    "consent_terms": db.consent_terms,
    "audit_logs": db.audit_logs,
    "doctor_patient": db.doctor_patient
}

def create_indexes(collection: str = None):
    """Cria os índices necessários em todas as collections."""

    # Índices da coleção Users
    if collection is None or collection == "users":
        db.users.create_index([("email", ASCENDING)], unique=True, collation={"locale": "en", "strength": 2})
        db.users.create_index([("cpf_encrypted", ASCENDING)], unique=True) 

    if collection is None or collection == "patients":
        # Índices da coleção Patients
        db.patients.create_index([("name", ASCENDING)])
        db.patients.create_index([("medical_conditions", ASCENDING)]) 
        db.patients.create_index([("medical_conditions", TEXT)]) 
        db.patients.create_index([("cpf_encrypted", ASCENDING)], unique=True) 

    if collection is None or collection == "prediction_data":
        # Índices da coleção Predictions
        db.prediction_data.create_index([("user_id", ASCENDING)])  
        db.prediction_data.create_index([("user_id", ASCENDING), ("timestamp", DESCENDING)])

    if collection is None or collection == "user_consents":
    # Índices da coleção UserConsents
        db.user_consents.create_index([("user_id", ASCENDING)])  
        db.user_consents.create_index([("consents.term_id", ASCENDING), ("consents.version", ASCENDING)])
        db.user_consents.create_index([
            ("user_id", ASCENDING),
            ("consents.term_id", ASCENDING),
            ("consents.version", ASCENDING),
            ("consents.status", ASCENDING)
        ])

    if collection is None or collection == "consent_terms":
        # Índices da coleção ConsentTerms
        db.consent_terms.create_index([("name", ASCENDING)], unique=True)
        db.consent_terms.create_index([("versions.version", DESCENDING)])
        db.consent_terms.create_index([
            ("name", ASCENDING), 
            ("versions.version", DESCENDING), 
            ("versions.active", ASCENDING)
        ])
 
    if collection is None or collection == "audit_logs":
        # Índices da coleção AuditLog
        db.audit_logs.create_index([("user_id", DESCENDING)])
        db.audit_logs.create_index([("timestamp", DESCENDING)])

    if collection is None or collection == "doctor_patient":
        # Índices da coleção DoctorPatient
        db.doctor_patient.create_index([("doctor_id", ASCENDING), ("patient_id", ASCENDING)], unique=True)
        db.doctor_patient.create_index([("doctor_id", ASCENDING)])

    print("✅ Todos os índices foram criados com sucesso!")

def drop_indexes(all_indexes: bool, collection: str = None):
    """
    Remove índices do MongoDB.

    Parâmetros:
    - `all_indexes` (bool): Se True, remove índices de todas as coleções.
    - `collection` (str): Se informado, remove índices apenas dessa coleção específica.
    """

    if all_indexes:
        
        for col_name, col in collections.items():
            col.drop_indexes()
            print(f"✅ Índices removidos da coleção: {col_name}")

    elif collection:
        if collection not in collections:
            print(f"❌ A coleção '{collection}' não existe.")
            return
        
        collections[collection].drop_indexes()
        print(f"✅ Índices removidos da coleção: {collection}")

    else:
        print("❌ Nenhuma ação foi realizada. Informe `all_indexes=True` ou um nome de `collection` válido.")
