"""
Pranav Agent - Core Implementation

This module contains the main Agent class that handles the core functionality
of the Pranav intelligent agent system.
"""

import os
from datetime import datetime
from typing import Any, Dict, List, Optional

# Import storage components
from .storage.factory import StorageFactory
from .storage.base import BaseStorage


class Agent:
    """
    Main Agent class for the Pranav system.
    
    This class implements the core functionality of the intelligent agent,
    including natural language understanding, task execution, and decision making.
    """
    
    def __init__(self, name="Pranav", config=None):
        """
        Initialize a new Agent instance.
        
        Args:
            name (str): The name of the agent instance
            config (dict, optional): Configuration parameters for the agent
        """
        self.name = name
        self.config = config or {}
        self.capabilities = []
        
        # Initialize storage
        self._initialize_storage()
        
        # Load agent state if available
        self._load_state()
        
        print(f"{self.name} agent initialized successfully.")
    
    def _initialize_storage(self):
        """Initialize the storage system based on configuration."""
        storage_config = self.config.get("storage", {})
        storage_type = storage_config.get("type", "json")
        
        # Set default storage paths
        if storage_type == "json":
            storage_dir = storage_config.get("path", "data/storage")
            self.storage = StorageFactory.create_storage("json", storage_dir=storage_dir)
        elif storage_type == "sqlite":
            db_path = storage_config.get("path", "data/storage/pranav.db")
            self.storage = StorageFactory.create_storage("sqlite", db_path=db_path)
        else:
            # Default to JSON storage if type is unknown
            self.storage = StorageFactory.create_storage("json", storage_dir="data/storage")
        
        if not self.storage:
            print("Warning: Failed to initialize storage. Using in-memory storage only.")
            self.memory = {}
        else:
            # Create data directories if they don't exist
            os.makedirs("data/storage", exist_ok=True)
    
    def _load_state(self):
        """Load agent state from storage."""
        if not hasattr(self, 'storage') or not self.storage:
            self.memory = {}
            self.conversation_history = []
            return
        
        # Load memory
        stored_memory = self.storage.retrieve("memory")
        self.memory = stored_memory if stored_memory else {}
        
        # Load conversation history
        history = self.storage.retrieve("conversation_history")
        self.conversation_history = history if history else []
    
    def _save_state(self):
        """Save agent state to storage."""
        if not hasattr(self, 'storage') or not self.storage:
            return
        
        # Save memory
        self.storage.store("memory", self.memory)
        
        # Save conversation history
        self.storage.store("conversation_history", self.conversation_history)
    
    def remember(self, key: str, value: Any) -> bool:
        """
        Store information in the agent's memory.
        
        Args:
            key (str): The key to store the value under
            value (Any): The value to remember
            
        Returns:
            bool: True if storage was successful, False otherwise
        """
        self.memory[key] = value
        
        # Also store in persistent storage if available
        if hasattr(self, 'storage') and self.storage:
            return self.storage.store(key, value, namespace="memory")
        return True
    
    def recall(self, key: str) -> Optional[Any]:
        """
        Retrieve information from the agent's memory.
        
        Args:
            key (str): The key to retrieve
            
        Returns:
            Optional[Any]: The stored value, or None if not found
        """
        # First check in-memory cache
        if key in self.memory:
            return self.memory[key]
        
        # Then check persistent storage
        if hasattr(self, 'storage') and self.storage:
            value = self.storage.retrieve(key, namespace="memory")
            if value is not None:
                # Update in-memory cache
                self.memory[key] = value
            return value
        
        return None
    
    def forget(self, key: str) -> bool:
        """
        Remove information from the agent's memory.
        
        Args:
            key (str): The key to forget
            
        Returns:
            bool: True if deletion was successful, False otherwise
        """
        if key in self.memory:
            del self.memory[key]
        
        # Also remove from persistent storage
        if hasattr(self, 'storage') and self.storage:
            return self.storage.delete(key, namespace="memory")
        return True
    
    def process_input(self, user_input: str) -> str:
        """
        Process user input and determine appropriate response or action.
        
        Args:
            user_input (str): The input text from the user
            
        Returns:
            str: The agent's response
        """
        # Record the interaction in conversation history
        if hasattr(self, 'conversation_history'):
            self.conversation_history.append({
                "role": "user",
                "content": user_input,
                "timestamp": str(datetime.now())
            })
        
        # This is a placeholder for actual NLP processing
        if not user_input:
            response = "I didn't receive any input. How can I help you?"
        # Simple keyword-based response for demonstration
        elif "hello" in user_input.lower():
            response = f"Hello! I'm {self.name}, your intelligent agent. How can I assist you today?"
        elif "remember" in user_input.lower() and "that" in user_input.lower():
            # Simple memory command parsing
            try:
                # Extract what to remember (very basic implementation)
                memory_text = user_input.split("that", 1)[1].strip()
                memory_key = f"user_memory_{len(self.memory)}"
                self.remember(memory_key, memory_text)
                response = f"I'll remember that: {memory_text}"
            except Exception:
                response = "I couldn't understand what to remember. Please try again."
        elif "what do you remember" in user_input.lower():
            # Return all memories
            if not self.memory:
                response = "I don't have any memories stored yet."
            else:
                memories = []
                for k, v in self.memory.items():
                    if k.startswith("user_memory_"):
                        memories.append(f"- {v}")
                response = "Here's what I remember:\n" + "\n".join(memories)
        else:
            response = f"I received your input: '{user_input}'. This agent is still in development."
        
        # Record the response in conversation history
        if hasattr(self, 'conversation_history'):
            self.conversation_history.append({
                "role": "assistant",
                "content": response,
                "timestamp": str(datetime.now())
            })
        
        # Save state after processing
        self._save_state()
        
        return response
    
    def execute_task(self, task_name: str, parameters: Optional[Dict] = None) -> Dict:
        """
        Execute a specific task based on the task name and parameters.
        
        Args:
            task_name (str): The name of the task to execute
            parameters (dict, optional): Parameters required for the task
            
        Returns:
            dict: The result of the task execution
        """
        # Record task execution in history
        if hasattr(self, 'storage') and self.storage:
            task_history = self.storage.retrieve("task_history") or []
            task_history.append({
                "task": task_name,
                "parameters": parameters,
                "timestamp": str(datetime.now())
            })
            self.storage.store("task_history", task_history)
        
        # Placeholder for task execution logic
        return {
            "status": "not_implemented",
            "message": f"Task '{task_name}' is not implemented yet."
        }
    
    def learn(self, data: Dict) -> bool:
        """
        Update the agent's knowledge based on new data.
        
        Args:
            data (dict): New information for the agent to learn
            
        Returns:
            bool: True if learning was successful, False otherwise
        """
        # Store learning data in persistent storage
        if hasattr(self, 'storage') and self.storage:
            learning_data = self.storage.retrieve("learning_data") or []
            learning_data.append({
                "data": data,
                "timestamp": str(datetime.now())
            })
            self.storage.store("learning_data", learning_data)
        
        # Placeholder for actual learning implementation
        return True
    
    def get_conversation_history(self) -> List[Dict]:
        """
        Get the conversation history.
        
        Returns:
            List[Dict]: List of conversation entries
        """
        if hasattr(self, 'conversation_history'):
            return self.conversation_history
        return []


if __name__ == "__main__":
    # Simple demonstration of the agent
    agent = Agent()
    print(agent.process_input("Hello there!"))
    print(agent.process_input("Remember that my favorite color is blue"))
    print(agent.process_input("What do you remember?"))