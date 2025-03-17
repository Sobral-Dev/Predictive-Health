from datetime import datetime
from typing import Optional
from bson import ObjectId
from repositories.base_repository import BaseRepository
from models.UserConsentModel import UserConsentModel
from utils.mongodb_indexes import drop_indexes, create_indexes

class UserConsentRepository(BaseRepository):
    def __init__(self):
        super().__init__("user_consents", UserConsentModel)

    def get_user_consents(self, user_id: str) -> Optional[UserConsentModel]:
        """Retorna o consentimento de um usuário pelo user_id."""
        return self.find_one({"user_id": ObjectId(user_id)})

    def update_or_insert_user_consent(self, user_id: str, term_id: str, status: bool, version: int):
        """
        Atualiza um consentimento existente OU insere um novo caso ainda não exista.
        Mantém o histórico de versões, desativando apenas versões antigas do mesmo termo.
        """
        user_id_obj = ObjectId(user_id)
        term_id_obj = ObjectId(term_id)
        timestamp = datetime.utcnow()

        existing_record = self.find_one({"user_id": user_id_obj})

        if existing_record:
            consents = existing_record.consents

            # Verifica se o usuário já possui um consentimento para este termo e versão específica
            existing_consent = next((c for c in consents if c["term_id"] == str(term_id_obj) and c["version"] == version), None)

            if existing_consent:
                # Atualiza o consentimento já existente na versão correta
                result = self.collection.update_one(
                    {
                        "user_id": user_id_obj
                    },
                    {
                        "$set": {
                            "consents.$[elem].status": status,
                            "consents.$[elem].timestamp": timestamp,
                            "updated_at": timestamp
                        }
                    },
                    array_filters=[{"elem.term_id": str(term_id_obj), "elem.version": version}]
                )

                print(f"🔍 (Atualização do consentimento já existente na versão vigente) Matched Count: {result.matched_count}, Modified Count: {result.modified_count} - {result.raw_result}")

            else:
                # Desativa apenas as versões anteriores do mesmo termo
                result = self.collection.update_many(
                    {"user_id": user_id_obj, "consents.term_id": str(term_id_obj), "consents.version": {"$lt": version}},
                    {"$set": {"consents.$[elem].active": False}},
                    array_filters=[{"elem.term_id": str(term_id_obj)}]  
                )

                print(f"🔍 (Desativar Versões Anteriores) Matched Count: {result.matched_count}, Modified Count: {result.modified_count}")

                # Insere um novo consentimento com a versão mais recente
                result = self.collection.update_one(
                    {"user_id": user_id_obj},
                    {
                        "$push": {
                            "consents": {
                                "term_id": str(term_id_obj),
                                "status": status,
                                "version": version,
                                "timestamp": timestamp,
                                "active": True  
                            }
                        },
                        "$set": {"updated_at": timestamp}
                    }
                )

                print(f"🔍 (Novo consentimento com a versão mais recente) Matched Count: {result.matched_count}, Modified Count: {result.modified_count} - {result.upserted_id}")

        else:
            # Se não existir um registro para o usuário, cria um novo
            new_consent = UserConsentModel(
                user_id=user_id_obj,
                consents=[{
                    "term_id": str(term_id_obj),
                    "status": status,
                    "version": version,
                    "timestamp": timestamp,
                    "active": True  
                }],
                updated_at=timestamp
            )
            self.insert_one(new_consent)

    def deactivate_user_consents(self, term_id: ObjectId):
        """Desativa o consentimento do usuário para um termo específico."""
        self.collection.update_many(
            {"consents.term_id": term_id},
            {"$set": {"consents.$.active": False}}
        )
