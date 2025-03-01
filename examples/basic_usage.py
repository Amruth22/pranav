"""
Basic Usage Example for Pranav Agent

This script demonstrates how to initialize and interact with the Pranav agent.
"""

import sys
import json
import os

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agent import Agent

def load_config(config_path):
    """Load configuration from a JSON file."""
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading configuration: {e}")
        return None

def main():
    # Load configuration
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'default_config.json')
    config = load_config(config_path)
    
    if not config:
        print("Using default configuration.")
        
    # Initialize the agent
    agent = Agent(config=config)
    
    print(f"\nWelcome to the {agent.name} Agent Demo")
    print("=" * 50)
    print("Type 'exit' or 'quit' to end the session.\n")
    
    # Simple interaction loop
    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ['exit', 'quit']:
            print(f"\n{agent.name}: Goodbye! Have a great day.")
            break
            
        response = agent.process_input(user_input)
        print(f"\n{agent.name}: {response}\n")

if __name__ == "__main__":
    main()