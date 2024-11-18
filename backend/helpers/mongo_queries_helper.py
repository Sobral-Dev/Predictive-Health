from pymongo import MongoClient

# Conectar ao MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["PredictiveHealth"]
collection = db["PredictionData"]

# Buscar os documentos
documents = collection.find()
for doc in documents:
    print(doc)
