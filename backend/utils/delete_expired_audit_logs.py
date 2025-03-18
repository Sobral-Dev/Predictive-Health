from datetime import datetime
from repositories.AuditLogRepository import AuditLogRepository

audit_repo = AuditLogRepository()

def delete_expired_audit_logs():
    """
    Exclui logs de auditoria que já passaram do período de retenção.
    """
    current_time = datetime.utcnow()
    delete_count = audit_repo.delete_many({"retention_period": {"$lt": current_time}})

    if delete_count:
        print(f"🗑️ {delete_count} logs antigos de auditoria foram removidos")
    else:
        print("✅ Nenhum log antigo para remover")