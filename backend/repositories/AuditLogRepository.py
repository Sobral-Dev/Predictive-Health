from repositories.base_repository import BaseRepository
from models.AuditLogModel import AuditLogModel 

class AuditLogRepository(BaseRepository):
    def __init__(self):
        super().__init__("audit_logs", AuditLogModel)