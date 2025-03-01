"""
Storage factory for Pranav agent.

This module provides a factory for creating storage instances.
"""

from typing import Dict, Optional, Type

from .base import BaseStorage
from .json_storage import JSONStorage
from .sqlite_storage import SQLiteStorage


class StorageFactory:
    """
    Factory for creating storage instances.
    
    This class provides a centralized way to create storage instances
    of different types based on configuration.
    """
    
    # Registry of available storage types
    _storage_types: Dict[str, Type[BaseStorage]] = {
        "json": JSONStorage,
        "sqlite": SQLiteStorage,
    }
    
    @classmethod
    def register_storage_type(cls, name: str, storage_class: Type[BaseStorage]):
        """
        Register a new storage type.
        
        Args:
            name (str): Name of the storage type
            storage_class (Type[BaseStorage]): Storage class to register
        """
        cls._storage_types[name] = storage_class
    
    @classmethod
    def create_storage(cls, storage_type: str, **kwargs) -> Optional[BaseStorage]:
        """
        Create a storage instance of the specified type.
        
        Args:
            storage_type (str): Type of storage to create
            **kwargs: Additional arguments to pass to the storage constructor
            
        Returns:
            Optional[BaseStorage]: Storage instance, or None if type not found
        """
        if storage_type not in cls._storage_types:
            print(f"Unknown storage type: {storage_type}")
            return None
        
        storage_class = cls._storage_types[storage_type]
        storage = storage_class(**kwargs)
        
        # Initialize the storage
        if not storage.initialize():
            print(f"Failed to initialize {storage_type} storage")
            return None
        
        return storage
    
    @classmethod
    def get_available_storage_types(cls) -> list:
        """
        Get a list of available storage types.
        
        Returns:
            list: List of available storage type names
        """
        return list(cls._storage_types.keys())