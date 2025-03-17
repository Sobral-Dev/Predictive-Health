from repositories.base_repository import BaseRepository
from models.PatientModel import PatientModel
from models.UserModel import UserModel
from bson import ObjectId
from typing import Optional

class PatientRepository(BaseRepository):
    def __init__(self):
        super().__init__("patients", PatientModel)
    
    def get_by_id(self, patient_id: str) -> Optional[UserModel]:
        try:
            return self.find_one({"_id": ObjectId(patient_id)})
        except:
            return None