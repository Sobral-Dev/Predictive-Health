from pydantic import BaseModel, Field
from typing import Any, Optional
from datetime import datetime
from bson import ObjectId

class AuditLogModel(BaseModel):
    id: Optional[ObjectId] = Field(default=None, alias="_id")
    user_id: Optional[ObjectId] = None
    action: str
    details: Optional[Any] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    retention_period: datetime = Field(default_factory=lambda: datetime.utcnow().replace(year=datetime.utcnow().year + 5))

    def to_dict(self):
        return {
            "id": str(self.id),
            "user_id": self.user_id,
            "action": self.action,
            "details": self.details,
            "timestamp": self.timestamp.isoformat(),
            "retention_period": self.retention_period.isoformat()
        }
    
    class Config:
        arbitrary_types_allowed = True