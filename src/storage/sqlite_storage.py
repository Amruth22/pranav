"""
SQLite storage implementation for Pranav agent.

This module provides a SQLite-based storage solution for more complex data.
"""

import json
import os
import sqlite3
import threading
from typing import Any, Dict, List, Optional, Union

from .base import BaseStorage


class SQLiteStorage(BaseStorage):
    """
    SQLite-based storage implementation.
    
    This class provides persistent storage using SQLite database.
    Each namespace is stored in a separate table.
    """
    
    def __init__(self, db_path: str = "data/storage/pranav.db"):
        """
        Initialize the SQLite storage.
        
        Args:
            db_path (str): Path to the SQLite database file
        """
        self.db_path = db_path
        self.default_namespace = "default"
        self._connection = None
        self._lock = threading.Lock()
    
    def _get_connection(self):
        """Get a connection to the SQLite database."""
        if self._connection is None:
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            self._connection = sqlite3.connect(self.db_path, check_same_thread=False)
        return self._connection
    
    def _create_table_if_not_exists(self, namespace: str):
        """Create a table for the namespace if it doesn't exist."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS "{namespace}" (
            key TEXT PRIMARY KEY,
            value TEXT
        )
        ''')
        conn.commit()
    
    def initialize(self) -> bool:
        """Initialize the storage system."""
        try:
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            conn = self._get_connection()
            self._create_table_if_not_exists(self.default_namespace)
            return True
        except Exception as e:
            print(f"Error initializing SQLite storage: {e}")
            return False
    
    def store(self, key: str, value: Any, namespace: Optional[str] = None) -> bool:
        """Store a value with the given key."""
        ns = namespace or self.default_namespace
        
        try:
            with self._lock:
                conn = self._get_connection()
                self._create_table_if_not_exists(ns)
                cursor = conn.cursor()
                
                # Convert value to JSON string
                value_json = json.dumps(value)
                
                # Insert or replace
                cursor.execute(f'''
                INSERT OR REPLACE INTO "{ns}" (key, value) VALUES (?, ?)
                ''', (key, value_json))
                
                conn.commit()
                return True
        except Exception as e:
            print(f"Error storing value: {e}")
            return False
    
    def retrieve(self, key: str, namespace: Optional[str] = None) -> Optional[Any]:
        """Retrieve a value by its key."""
        ns = namespace or self.default_namespace
        
        try:
            with self._lock:
                conn = self._get_connection()
                self._create_table_if_not_exists(ns)
                cursor = conn.cursor()
                
                cursor.execute(f'''
                SELECT value FROM "{ns}" WHERE key = ?
                ''', (key,))
                
                result = cursor.fetchone()
                if result is None:
                    return None
                
                # Convert JSON string back to Python object
                return json.loads(result[0])
        except Exception as e:
            print(f"Error retrieving value: {e}")
            return None
    
    def delete(self, key: str, namespace: Optional[str] = None) -> bool:
        """Delete a value by its key."""
        ns = namespace or self.default_namespace
        
        try:
            with self._lock:
                conn = self._get_connection()
                self._create_table_if_not_exists(ns)
                cursor = conn.cursor()
                
                cursor.execute(f'''
                DELETE FROM "{ns}" WHERE key = ?
                ''', (key,))
                
                conn.commit()
                return True
        except Exception as e:
            print(f"Error deleting value: {e}")
            return False
    
    def list_keys(self, namespace: Optional[str] = None) -> List[str]:
        """List all keys in the storage."""
        ns = namespace or self.default_namespace
        
        try:
            with self._lock:
                conn = self._get_connection()
                self._create_table_if_not_exists(ns)
                cursor = conn.cursor()
                
                cursor.execute(f'''
                SELECT key FROM "{ns}"
                ''')
                
                return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error listing keys: {e}")
            return []
    
    def clear(self, namespace: Optional[str] = None) -> bool:
        """Clear all data in the storage."""
        try:
            with self._lock:
                conn = self._get_connection()
                cursor = conn.cursor()
                
                if namespace is None:
                    # Get all table names (namespaces)
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                    tables = [row[0] for row in cursor.fetchall()]
                    
                    # Drop all tables
                    for table in tables:
                        cursor.execute(f'DROP TABLE IF EXISTS "{table}"')
                    
                    # Recreate default namespace
                    self._create_table_if_not_exists(self.default_namespace)
                else:
                    # Clear specific namespace
                    self._create_table_if_not_exists(namespace)
                    cursor.execute(f'DELETE FROM "{namespace}"')
                
                conn.commit()
                return True
        except Exception as e:
            print(f"Error clearing storage: {e}")
            return False