from pymongo import MongoClient
import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.UserModel import UserModel

# Conexão com o MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["PredictiveHealth"]

def insert_users():
    """Lê os usuários do arquivo JSON e insere no MongoDB."""

    try:
        # Ler os dados do arquivo JSON
        with open("users_data.json", "r", encoding="utf-8") as file:
            users_data = json.load(file)

        # Converter os dados para o formato do modelo
        user_objects = [UserModel(**user).to_dict() for user in users_data]

        # Inserir no MongoDB
        db.users.insert_many(user_objects)
        print(f"✅ {len(user_objects)} usuários inseridos com sucesso!")

    except Exception as e:
        print(f"❌ Erro ao inserir usuários: {str(e)}")


if __name__ == "__main__":
    insert_users()