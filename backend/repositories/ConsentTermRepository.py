from repositories.base_repository import BaseRepository
from models.ConsentTermModel import ConsentTermModel
from bson import ObjectId
from typing import Optional

class ConsentTermRepository(BaseRepository):
    def __init__(self):
        super().__init__("consent_terms", ConsentTermModel)

    def get_term_by_name(self, name: str) -> Optional[ConsentTermModel]:
        """Retorna um termo pelo nome."""
        return self.find_one({"name": name})

    def get_term_by_id(self, term_id: str) -> Optional[ConsentTermModel]:
        """Retorna um termo pelo ID."""
        return self.find_one({"_id": ObjectId(term_id)})

    def get_all_terms(self):
        """Retorna todos os termos de consentimento."""
        return self.find_all()

    def insert_term(self, term: ConsentTermModel):
        """Insere um novo termo de consentimento."""
        return self.insert_one(term.to_dict())

    def update_term(self, term: ConsentTermModel):
        """Atualiza um termo existente."""
        self.update_one({"_id": term.id}, term.to_dict())

    def deactivate_old_versions(self, term_id: ObjectId):
        """Desativa todas as versões antigas de um termo quando uma nova versão é criada."""
        self.collection.update_many(
            {"_id": term_id, "versions.active": True},
            {"$set": {"versions.$[].active": False}}
        )
