from pydantic import BaseModel, Field
from typing import Any, Optional
from datetime import datetime
from bson import ObjectId

class PredictionDataModel(BaseModel):
    id: Optional[ObjectId] = Field(default=None, alias="_id")
    user_id: ObjectId
    patient_id: ObjectId
    prediction_type: str
    input_data: Any
    prediction_result: Any
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    def to_dict(self):
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "patient_id": str(self.patient_id),
            "prediction_type": self.prediction_type,
            "input_data": self.input_data,
            "prediction_result": self.prediction_result,
            "timestamp": self.timestamp.isoformat()
        }
    
    class Config:
        arbitrary_types_allowed = True