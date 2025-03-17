from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId

class UserConsentModel(BaseModel):
    id: Optional[ObjectId] = Field(default=None, alias="_id")
    user_id: Optional[ObjectId] = None
    consents: list[dict]  
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def update_consent(self, term_id: ObjectId, status: bool, version: int):
        """Atualiza o consentimento do usuário, garantindo que esteja na versão mais recente ativa."""
        for consent in self.consents:
            if consent["term_id"] == str(term_id):
                consent["status"] = status
                consent["version"] = version
                consent["timestamp"] = datetime.utcnow()
                consent["active"] = status 
                break
        else:
            self.consents.append({
                "term_id": str(term_id),
                "status": status,
                "version": version,
                "timestamp": datetime.utcnow(),
                "active": status
            })

    def to_dict(self):
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "consents": [
                {
                    "term_id": str(consent["term_id"]),
                    "status": consent["status"],
                    "version": consent["version"],
                    "timestamp": consent["timestamp"].isoformat(),
                    "active": consent["active"]
                }
                for consent in self.consents
            ],
            "updated_at": self.updated_at.isoformat()
        }

    class Config:
        arbitrary_types_allowed = True