from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from bson import ObjectId

class PatientModel(BaseModel):
    id: Optional[ObjectId] = Field(default=None, alias="_id")
    name: str
    medical_conditions: Optional[List[str]] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    cpf_encrypted: str
    birth_date: datetime

    def to_dict(self):
        return {
            "name": self.name,
            "medical_conditions": self.medical_conditions,
            "created_at": self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            "cpf_encrypted": self.cpf_encrypted,
            "birth_date": self.birth_date.isoformat() if isinstance(self.birth_date, datetime) else self.birth_date
        }
    
    class Config:
        arbitrary_types_allowed = True