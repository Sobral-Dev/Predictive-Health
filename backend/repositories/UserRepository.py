from repositories.base_repository import BaseRepository
from models.UserModel import UserModel
from typing import Optional
from bson import ObjectId

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__("users", UserModel)
    
    def get_by_id(self, user_id: str) -> Optional[UserModel]:
        try:
            return self.find_one({"_id": ObjectId(user_id)})
        except:
            return None