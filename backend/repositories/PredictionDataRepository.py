from repositories.base_repository import BaseRepository
from models.PredictionDataModel import PredictionDataModel

class PredictionDataRepository(BaseRepository):
    def __init__(self):
        super().__init__("prediction_data", PredictionDataModel)