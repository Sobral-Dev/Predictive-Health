from models.ConsentTermModel import ConsentTermModel
from pymongo import MongoClient
import json

# Conexão com o MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["PredictiveHealth"]


def insert_consent_terms():
    """Lê os Termos do arquivo JSON e insere no MongoDB."""

    try:
        # Ler os dados do arquivo JSON
        with open("terms_data.json", "r", encoding="utf-8") as file:
            terms_data = json.load(file)

        # Converter os dados para o formato do modelo
        term_objects = [ConsentTermModel(**term).to_dict() for term in terms_data]

        # Inserir no MongoDB
        db.consent_terms.insert_many(term_objects)
        print(f"✅ {len(term_objects)} termos inseridos com sucesso!")

    except Exception as e:
        print(f"❌ Erro ao inserir termos: {str(e)}")


if __name__ == "__main__":
    insert_consent_terms()