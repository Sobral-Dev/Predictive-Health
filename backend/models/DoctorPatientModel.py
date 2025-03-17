from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId

class DoctorPatientModel(BaseModel):
    id: Optional[ObjectId] = Field(default=None, alias="_id")
    doctor_id: ObjectId
    patient_id: ObjectId
    consent_status: str = "pending"  # "pending", "accepted", "rejected"
    created_at: datetime = Field(default_factory=datetime.utcnow)

    def to_dict(self):
        return {
            "doctor_id": self.doctor_id,
            "patient_id": self.patient_id,
            "consent_status": self.consent_status,
            "created_at": self.created_at.isoformat()
        }
    
    class Config:
        arbitrary_types_allowed = True