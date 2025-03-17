from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId

class JWTKeyModel(BaseModel):
    id: Optional[ObjectId] = Field(default=None, alias="_id")
    key: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    active: bool = False

    def to_dict(self):
        return {
            "key": self.key,
            "created_at": self.created_at.isoformat(),
            "active": self.active
        }
    
    class Config:
        arbitrary_types_allowed = True
