from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId

class RevokedTokenModel(BaseModel):
    id: Optional[ObjectId] = Field(default=None, alias="_id")
    jti: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    def to_dict(self):
        return {
            "jti": self.jti,
            "created_at": self.created_at.isoformat()
        }
    
    class Config:
        arbitrary_types_allowed = True
