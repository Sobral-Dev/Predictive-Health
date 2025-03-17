from repositories.base_repository import BaseRepository
from models.JWTKeyModel import JWTKeyModel

class JWTKeyRepository(BaseRepository):
    def __init__(self):
        super().__init__("jwt_keys", JWTKeyModel)