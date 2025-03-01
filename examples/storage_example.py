"""
Storage Usage Example for Pranav Agent

This script demonstrates how to use the persistent storage capabilities.
"""

import sys
import os
import json
from datetime import datetime

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.storage.factory import StorageFactory


def demonstrate_json_storage():
    """Demonstrate the JSON storage functionality."""
    print("\n=== JSON Storage Demonstration ===")
    
    # Create a JSON storage instance
    storage = StorageFactory.create_storage("json", storage_dir="data/json_example")
    if not storage:
        print("Failed to create JSON storage")
        return
    
    # Store some values
    print("\nStoring values...")
    storage.store("greeting", "Hello, world!")
    storage.store("timestamp", str(datetime.now()))
    storage.store("counter", 42)
    storage.store("config", {"debug": True, "log_level": "INFO"})
    
    # Store values in a different namespace
    storage.store("user_name", "Alice", namespace="users")
    storage.store("user_email", "alice@example.com", namespace="users")
    
    # Retrieve values
    print("\nRetrieving values:")
    print(f"greeting: {storage.retrieve('greeting')}")
    print(f"timestamp: {storage.retrieve('timestamp')}")
    print(f"counter: {storage.retrieve('counter')}")
    print(f"config: {storage.retrieve('config')}")
    
    # List keys
    print("\nListing keys in default namespace:")
    for key in storage.list_keys():
        print(f"- {key}")
    
    print("\nListing keys in 'users' namespace:")
    for key in storage.list_keys(namespace="users"):
        print(f"- {key}")
    
    # Update a value
    print("\nUpdating counter...")
    current = storage.retrieve("counter")
    storage.store("counter", current + 1)
    print(f"counter (after update): {storage.retrieve('counter')}")
    
    # Delete a value
    print("\nDeleting 'greeting'...")
    storage.delete("greeting")
    print(f"greeting after deletion: {storage.retrieve('greeting')}")
    
    print("\nJSON storage files created in: data/json_example/")


def demonstrate_sqlite_storage():
    """Demonstrate the SQLite storage functionality."""
    print("\n=== SQLite Storage Demonstration ===")
    
    # Create a SQLite storage instance
    storage = StorageFactory.create_storage("sqlite", db_path="data/sqlite_example/pranav.db")
    if not storage:
        print("Failed to create SQLite storage")
        return
    
    # Store some complex data
    print("\nStoring complex data...")
    user_data = {
        "name": "Bob",
        "email": "bob@example.com",
        "preferences": {
            "theme": "dark",
            "notifications": True
        },
        "history": [
            {"action": "login", "timestamp": str(datetime.now())},
            {"action": "view_profile", "timestamp": str(datetime.now())}
        ]
    }
    
    storage.store("user_profile", user_data)
    storage.store("app_state", {"running": True, "pid": 1234})
    
    # Store data in different namespaces
    storage.store("temperature", 22.5, namespace="sensors")
    storage.store("humidity", 45.2, namespace="sensors")
    
    # Retrieve data
    print("\nRetrieving data:")
    retrieved_user = storage.retrieve("user_profile")
    print(f"User name: {retrieved_user['name']}")
    print(f"User preferences: {json.dumps(retrieved_user['preferences'], indent=2)}")
    print(f"User history entries: {len(retrieved_user['history'])}")
    
    # List all keys
    print("\nListing keys in default namespace:")
    for key in storage.list_keys():
        print(f"- {key}")
    
    print("\nListing keys in 'sensors' namespace:")
    for key in storage.list_keys(namespace="sensors"):
        print(f"- {key}")
    
    print("\nSQLite database created at: data/sqlite_example/pranav.db")


def main():
    """Main function to run the storage examples."""
    print("Pranav Agent - Storage Examples")
    print("===============================")
    
    # Create directories if they don't exist
    os.makedirs("data/json_example", exist_ok=True)
    os.makedirs("data/sqlite_example", exist_ok=True)
    
    # Show available storage types
    print(f"\nAvailable storage types: {StorageFactory.get_available_storage_types()}")
    
    # Run demonstrations
    demonstrate_json_storage()
    demonstrate_sqlite_storage()
    
    print("\nStorage examples completed.")


if __name__ == "__main__":
    main()