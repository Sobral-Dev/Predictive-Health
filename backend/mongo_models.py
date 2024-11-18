from pydantic import BaseModel, Field
from typing import Dict
from datetime import datetime

class PredictionData(BaseModel):
    user_id: int
    patient_id: int
    prediction_type: str
    input_data: Dict
    prediction_result: Dict
    timestamp: datetime = Field(default_factory=datetime.utcnow)