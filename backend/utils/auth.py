from models.AuditLogModel import AuditLogModel
from models.RevokedTokenModel import RevokedTokenModel
from repositories.UserRepository import UserRepository
from repositories.AuditLogRepository import AuditLogRepository
from repositories.RevokedTokenRepository import RevokedTokenRepository
from functools import wraps
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from flask import jsonify
import json
from bson import ObjectId

AuditLogRepository = AuditLogRepository()
UserRepository = UserRepository()
RevokedTokenRepository = RevokedTokenRepository()

def role_required(roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = UserRepository.find_one({"_id": ObjectId(user_id)})
            if user.role not in roles:
                return jsonify({"error": "Unauthorized"}), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator

def add_audit_log(action, user_id, details=None):
    """
    Registra um evento de auditoria no banco de dados.

    :param action: Ação executada (ex.: "User registration").
    :param user_id: ID do usuário que executou a ação.
    :param details: (Opcional) Detalhes adicionais da ação, em formato de dicionário.
    """
    log = AuditLogModel(
        user_id=user_id,
        action=action,
        details=json.dumps(details) if details else None
    )
    AuditLogRepository.insert_one(log)

def revoke_token(jti):
    # Revoga o token adicionando-o à tabela
    revoked_token = RevokedTokenModel(jti=jti)
    RevokedTokenRepository.insert_one(revoked_token)
