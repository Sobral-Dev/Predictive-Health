from bson import ObjectId
from datetime import datetime
from flask import jsonify

# Função para converter ObjectId e outros objetos não serializáveis
def serialize_document(doc):
    if isinstance(doc, ObjectId):
        return str(doc)
    elif isinstance(doc, datetime):
        return doc.isoformat()
    elif isinstance(doc, dict):
        return {key: serialize_document(value) for key, value in doc.items()}
    elif isinstance(doc, list):
        return [serialize_document(item) for item in doc]
    return doc  