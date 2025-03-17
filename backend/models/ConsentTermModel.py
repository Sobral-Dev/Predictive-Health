from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId
from typing import List

class ConsentTermModel(BaseModel):
    id: Optional[ObjectId] = Field(default=None, alias="_id")
    name: str  
    description: str  
    created_at: datetime = Field(default_factory=datetime.utcnow)
    mandatory: bool = False
    active: bool = True  
    versions: List[dict] = []  

    def add_version(self, description: str):
        """Adiciona uma nova versão ao termo, garantindo que apenas uma esteja ativa."""
        for v in self.versions:
            v["active"] = False  

        new_version = {
            "version": len(self.versions) + 1,
            "description": description,
            "created_at": datetime.utcnow().isoformat(),
            "active": True
        }
        self.versions.append(new_version)

    def deactivate(self):
        """Desativa o termo e todas as versões associadas."""
        self.active = False
        for v in self.versions:
            v["active"] = False

    def to_dict(self):

        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "mandatory": self.mandatory,
            "created_at": self.created_at.isoformat(),
            "active": self.active,
            "versions": [
                {
                    "version": version["version"],
                    "description": version["description"],
                    "created_at": version["created_at"],
                    "active": version["active"]
                }
                for version in self.versions
            ]
        }

    class Config:
        arbitrary_types_allowed = True
