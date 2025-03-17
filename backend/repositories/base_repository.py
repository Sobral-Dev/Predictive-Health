from pymongo import MongoClient
from bson import ObjectId
from typing import Type, TypeVar, Optional, List, Dict
from pydantic import BaseModel

mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["PredictiveHealth"]

T = TypeVar("T", bound=BaseModel)

class BaseRepository:
    def __init__(self, collection_name: str, model: Type[T]):
        self.collection = db[collection_name]
        self.model = model

    def find_one(self, query: dict) -> Optional[T]:
        if not isinstance(query, dict): 
            raise ValueError("Query must be a dictionary.")
        data = self.collection.find_one(query)
        return self.model(**data) if data else None

    def find_all(self, query: dict = {}, sort_field: str = None, sort_order: int = 1, projection: dict = None) -> List[T]:
        if not isinstance(query, dict): 
            raise ValueError("Query must be a dictionary.")
        data = self.collection.find(query)

        if sort_field:
            data = data.sort(sort_field, sort_order)  # Ordenação ASC (1) ou DESC (-1)
        
        if projection:
            return list(self.collection.find(query, projection))
            
        return [self.model(**item) for item in data if item]

    def insert_one(self, item: T) -> ObjectId:
        if not isinstance(item, self.model):  
            raise TypeError(f"Item must be an instance of {self.model.__name__}")
        result = self.collection.insert_one(item.dict(by_alias=True, exclude_none=True))
        return result.inserted_id

    def delete_one(self, query: dict) -> bool:
        if not isinstance(query, dict):  
            raise ValueError("Query must be a dictionary.")
        result = self.collection.delete_one(query)
        return result.deleted_count > 0
    
    def update_one(self, query: dict, update_data: Dict) -> bool:
        if not isinstance(query, dict) or not isinstance(update_data, dict):  
            raise ValueError("Query and update_data must be dictionaries.")
        if not update_data:
            raise ValueError("update_data must not be empty.")
        clean_update = {k: v for k, v in update_data.items() if v is not None}
        if not clean_update:
            return False
        result = self.collection.update_one(query, {"$set": clean_update})
        return result.modified_count > 0

    def update_many(self, query: dict, update_data: Dict) -> int:
        if not isinstance(query, dict) or not isinstance(update_data, dict):  
            raise ValueError("Query and update_data must be dictionaries.")
        if not update_data:  
            raise ValueError("update_data must not be empty.")
        clean_update = {k: v for k, v in update_data.items() if v is not None}  
        if not clean_update:
            return 0
        result = self.collection.update_many(query, {"$set": clean_update})
        return result.modified_count
