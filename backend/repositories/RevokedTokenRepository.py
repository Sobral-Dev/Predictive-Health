from repositories.base_repository import BaseRepository
from models.RevokedTokenModel import RevokedTokenModel

class RevokedTokenRepository(BaseRepository):
    def __init__(self):
        super().__init__("revoked_tokens", RevokedTokenModel)