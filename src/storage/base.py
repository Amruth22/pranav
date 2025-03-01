"""
Base storage interface for Pranav agent.

This module defines the abstract base class for all storage implementations.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union


class BaseStorage(ABC):
    """
    Abstract base class for storage implementations.
    
    All storage providers must implement these methods to provide
    consistent data persistence capabilities.
    """
    
    @abstractmethod
    def initialize(self) -> bool:
        """
        Initialize the storage system.
        
        Returns:
            bool: True if initialization was successful, False otherwise
        """
        pass
    
    @abstractmethod
    def store(self, key: str, value: Any, namespace: Optional[str] = None) -> bool:
        """
        Store a value with the given key.
        
        Args:
            key (str): The key to store the value under
            value (Any): The value to store
            namespace (Optional[str]): Optional namespace to organize data
            
        Returns:
            bool: True if storage was successful, False otherwise
        """
        pass
    
    @abstractmethod
    def retrieve(self, key: str, namespace: Optional[str] = None) -> Optional[Any]:
        """
        Retrieve a value by its key.
        
        Args:
            key (str): The key to retrieve
            namespace (Optional[str]): Optional namespace to retrieve from
            
        Returns:
            Optional[Any]: The stored value, or None if not found
        """
        pass
    
    @abstractmethod
    def delete(self, key: str, namespace: Optional[str] = None) -> bool:
        """
        Delete a value by its key.
        
        Args:
            key (str): The key to delete
            namespace (Optional[str]): Optional namespace to delete from
            
        Returns:
            bool: True if deletion was successful, False otherwise
        """
        pass
    
    @abstractmethod
    def list_keys(self, namespace: Optional[str] = None) -> List[str]:
        """
        List all keys in the storage.
        
        Args:
            namespace (Optional[str]): Optional namespace to list keys from
            
        Returns:
            List[str]: List of keys
        """
        pass
    
    @abstractmethod
    def clear(self, namespace: Optional[str] = None) -> bool:
        """
        Clear all data in the storage.
        
        Args:
            namespace (Optional[str]): Optional namespace to clear
            
        Returns:
            bool: True if clearing was successful, False otherwise
        """
        pass