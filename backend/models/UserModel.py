from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from bson import ObjectId

class UserModel(BaseModel):
    id: Optional[ObjectId] = Field(default=None, alias="_id")
    name: str
    email: EmailStr
    password: str
    role: str  # "admin", "medico", "paciente", "deleted"
    reset_token: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    cpf_encrypted: str

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "role": self.role,
            "reset_token": self.reset_token,
            "created_at": self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            "cpf_encrypted": self.cpf_encrypted,
        }
    
    class Config:
        arbitrary_types_allowed = True