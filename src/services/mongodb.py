from typing import Any, Dict, List, Optional
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database


class MongoDBService:
    def __init__(self, connection_uri: str, database_name: str):
        """Initialize MongoDB connection.
        
        Args:
            connection_uri: MongoDB connection string
            database_name: Name of the database to use
        """
        self.client: MongoClient = MongoClient(connection_uri)
        self.db: Database = self.client[database_name]

    def get_collection(self, collection_name: str) -> Collection:
        """Get a MongoDB collection.
        
        Args:
            collection_name: Name of the collection
        
        Returns:
            MongoDB collection object
        """
        return self.db[collection_name]

    def insert_one(self, collection_name: str, document: Dict[str, Any]) -> str:
        """Insert a single document into a collection.
        
        Args:
            collection_name: Name of the collection
            document: Document to insert
            
        Returns:
            Inserted document ID
        """
        result = self.get_collection(collection_name).insert_one(document)
        return str(result.inserted_id)

    def insert_many(self, collection_name: str, documents: List[Dict[str, Any]]) -> List[str]:
        """Insert multiple documents into a collection.
        
        Args:
            collection_name: Name of the collection
            documents: List of documents to insert
            
        Returns:
            List of inserted document IDs
        """
        result = self.get_collection(collection_name).insert_many(documents)
        return [str(id) for id in result.inserted_ids]

    def find_one(self, collection_name: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find a single document in a collection.
        
        Args:
            collection_name: Name of the collection
            query: Query filter
            
        Returns:
            Found document or None
        """
        return self.get_collection(collection_name).find_one(query)

    def find_many(self, collection_name: str, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find multiple documents in a collection.
        
        Args:
            collection_name: Name of the collection
            query: Query filter
            
        Returns:
            List of found documents
        """
        return list(self.get_collection(collection_name).find(query))

    def update_one(self, collection_name: str, query: Dict[str, Any], update: Dict[str, Any]) -> int:
        """Update a single document in a collection.
        
        Args:
            collection_name: Name of the collection
            query: Query filter
            update: Update operations
            
        Returns:
            Number of modified documents
        """
        result = self.get_collection(collection_name).update_one(query, {"$set": update})
        return result.modified_count

    def update_many(self, collection_name: str, query: Dict[str, Any], update: Dict[str, Any]) -> int:
        """Update multiple documents in a collection.
        
        Args:
            collection_name: Name of the collection
            query: Query filter
            update: Update operations
            
        Returns:
            Number of modified documents
        """
        result = self.get_collection(collection_name).update_many(query, {"$set": update})
        return result.modified_count

    def delete_one(self, collection_name: str, query: Dict[str, Any]) -> int:
        """Delete a single document from a collection.
        
        Args:
            collection_name: Name of the collection
            query: Query filter
            
        Returns:
            Number of deleted documents
        """
        result = self.get_collection(collection_name).delete_one(query)
        return result.deleted_count

    def delete_many(self, collection_name: str, query: Dict[str, Any]) -> int:
        """Delete multiple documents from a collection.
        
        Args:
            collection_name: Name of the collection
            query: Query filter
            
        Returns:
            Number of deleted documents
        """
        result = self.get_collection(collection_name).delete_many(query)
        return result.deleted_count

    def close(self):
        """Close the MongoDB connection."""
        self.client.close()
