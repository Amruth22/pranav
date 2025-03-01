"""
JSON file storage implementation for Pranav agent.

This module provides a simple JSON file-based storage solution.
"""

import json
import os
import threading
from typing import Any, Dict, List, Optional, Union

from .base import BaseStorage


class JSONStorage(BaseStorage):
    """
    JSON file-based storage implementation.
    
    This class provides persistent storage using JSON files on disk.
    Each namespace is stored in a separate JSON file.
    """
    
    def __init__(self, storage_dir: str = "data/storage"):
        """
        Initialize the JSON storage.
        
        Args:
            storage_dir (str): Directory to store JSON files
        """
        self.storage_dir = storage_dir
        self.default_namespace = "default"
        self._data_cache: Dict[str, Dict[str, Any]] = {}
        self._locks: Dict[str, threading.Lock] = {}
        
    def _get_namespace_path(self, namespace: Optional[str] = None) -> str:
        """Get the file path for a namespace."""
        ns = namespace or self.default_namespace
        return os.path.join(self.storage_dir, f"{ns}.json")
    
    def _get_lock(self, namespace: Optional[str] = None) -> threading.Lock:
        """Get a lock for thread-safe operations on a namespace."""
        ns = namespace or self.default_namespace
        if ns not in self._locks:
            self._locks[ns] = threading.Lock()
        return self._locks[ns]
    
    def _load_namespace(self, namespace: Optional[str] = None) -> Dict[str, Any]:
        """Load data from a namespace file."""
        ns = namespace or self.default_namespace
        if ns in self._data_cache:
            return self._data_cache[ns]
        
        file_path = self._get_namespace_path(ns)
        if not os.path.exists(file_path):
            return {}
        
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                self._data_cache[ns] = data
                return data
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading namespace {ns}: {e}")
            return {}
    
    def _save_namespace(self, namespace: Optional[str] = None) -> bool:
        """Save data to a namespace file."""
        ns = namespace or self.default_namespace
        if ns not in self._data_cache:
            return True  # Nothing to save
        
        file_path = self._get_namespace_path(ns)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        try:
            with open(file_path, 'w') as f:
                json.dump(self._data_cache[ns], f, indent=2)
            return True
        except IOError as e:
            print(f"Error saving namespace {ns}: {e}")
            return False
    
    def initialize(self) -> bool:
        """Initialize the storage system."""
        try:
            os.makedirs(self.storage_dir, exist_ok=True)
            return True
        except OSError as e:
            print(f"Error initializing storage: {e}")
            return False
    
    def store(self, key: str, value: Any, namespace: Optional[str] = None) -> bool:
        """Store a value with the given key."""
        ns = namespace or self.default_namespace
        lock = self._get_lock(ns)
        
        with lock:
            if ns not in self._data_cache:
                self._data_cache[ns] = self._load_namespace(ns)
            
            self._data_cache[ns][key] = value
            return self._save_namespace(ns)
    
    def retrieve(self, key: str, namespace: Optional[str] = None) -> Optional[Any]:
        """Retrieve a value by its key."""
        ns = namespace or self.default_namespace
        lock = self._get_lock(ns)
        
        with lock:
            if ns not in self._data_cache:
                self._data_cache[ns] = self._load_namespace(ns)
            
            return self._data_cache[ns].get(key)
    
    def delete(self, key: str, namespace: Optional[str] = None) -> bool:
        """Delete a value by its key."""
        ns = namespace or self.default_namespace
        lock = self._get_lock(ns)
        
        with lock:
            if ns not in self._data_cache:
                self._data_cache[ns] = self._load_namespace(ns)
            
            if key in self._data_cache[ns]:
                del self._data_cache[ns][key]
                return self._save_namespace(ns)
            
            return True  # Key didn't exist, so deletion is technically successful
    
    def list_keys(self, namespace: Optional[str] = None) -> List[str]:
        """List all keys in the storage."""
        ns = namespace or self.default_namespace
        lock = self._get_lock(ns)
        
        with lock:
            if ns not in self._data_cache:
                self._data_cache[ns] = self._load_namespace(ns)
            
            return list(self._data_cache[ns].keys())
    
    def clear(self, namespace: Optional[str] = None) -> bool:
        """Clear all data in the storage."""
        if namespace is None:
            # Clear all namespaces
            try:
                for ns in list(self._data_cache.keys()):
                    lock = self._get_lock(ns)
                    with lock:
                        self._data_cache[ns] = {}
                        self._save_namespace(ns)
                return True
            except Exception as e:
                print(f"Error clearing all namespaces: {e}")
                return False
        else:
            # Clear specific namespace
            lock = self._get_lock(namespace)
            with lock:
                self._data_cache[namespace] = {}
                return self._save_namespace(namespace)