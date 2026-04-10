from typing import Dict, Any, Optional

class RelationalDB:
    def __init__(self):
        # In-memory storage: { collection_name: { id: { data } } }
        self.store: Dict[str, Dict[str, Any]] = {}

    def get_by_id(self, collection_name: str, item_id: str) -> Optional[Dict[str, Any]]:
        if collection_name not in self.store:
            return None
        return self.store[collection_name].get(item_id)

    def insert_or_update(self, collection_name: str, item_id: str, data: Dict[str, Any]):
        if collection_name not in self.store:
            self.store[collection_name] = {}
        self.store[collection_name][item_id] = data
        
    def list_all(self, collection_name: str) -> list[Dict[str, Any]]:
        if collection_name not in self.store:
            return []
        return list(self.store[collection_name].values())

# Global singleton for in-memory DB
relational_db_instance = RelationalDB()
