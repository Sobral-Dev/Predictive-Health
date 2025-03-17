from repositories.base_repository import BaseRepository
from models.DoctorPatientModel import DoctorPatientModel

class DoctorPatientRepository(BaseRepository):
    def __init__(self):
        super().__init__("doctor_patient", DoctorPatientModel)