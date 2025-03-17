import secrets
from models.JWTKeyModel import JWTKeyModel
from repositories.JWTKeyRepository import JWTKeyRepository

JWTKey = JWTKeyRepository()

def load_encryption_key():
    with open("encryption_key.key", "rb") as key_file:
        return key_file.read()

def encrypt_jwt_key(key):
    from app import cipher_suite as cipher
    """Criptografa uma chave JWT"""
    return cipher.encrypt(key.encode('utf-8')).decode('utf-8')

def decrypt_jwt_key(encrypted_key):
    from app import cipher_suite as cipher
    """Descriptografa uma chave JWT"""
    return cipher.decrypt(encrypted_key.encode('utf-8')).decode('utf-8')

def store_jwt_key(new_key):

    active_keys = JWTKey.find_all({"active": True})

    print(f'Active_keys= {len(active_keys)}')

    if active_keys:
        # Desativar todas as chaves ativas
        try:
            JWTKey.update_many({"active": True}, {"active": False}) 
        except Exception as e:
            print(f"Erro ao desativar a chave anterior: {e}")
            pass

    # Salva a chave criptografada no banco
    key_entry = JWTKeyModel(key=new_key, active=True)
    JWTKey.insert_one(key_entry)

    return new_key

# Obter a chave ativa
def get_active_jwt_key():
    key_entry = JWTKey.find_one({"active": True})
    if key_entry:
        return key_entry.key
    return None

# Geração aleatória de uma chave 32 bytes segura
def generate_jwt_key():
    
    return secrets.token_hex(32) 
