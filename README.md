# Pranav - Intelligent Agent Project

## Overview
Pranav is an intelligent agent system designed to automate tasks, process information, and provide assistance through natural language understanding and autonomous decision-making capabilities.

## Features (Planned)
- Natural language understanding and processing
- Task automation and scheduling
- Knowledge retrieval and information synthesis
- Decision-making based on predefined rules and learning
- Integration with external APIs and services

## Project Structure
- `/src` - Source code for the agent
- `/docs` - Documentation
- `/tests` - Test cases and testing framework
- `/examples` - Example use cases and demonstrations
- `/config` - Configuration files

## Technologies
- Python for core functionality
- Natural Language Processing libraries
- Machine Learning frameworks
- API integration tools
- Docker for containerization and deployment

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Docker (for containerized deployment)
- Git

### Local Installation
1. Clone the repository:
   ```
   git clone https://github.com/Amruth22/pranav.git
   cd pranav
   ```

2. Create a virtual environment and install dependencies:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Run the example:
   ```
   python examples/basic_usage.py
   ```

### Docker Deployment
The project includes Docker support for easy deployment:

1. Build and start the container:
   ```
   chmod +x docker-run.sh  # Make the script executable (Unix/Linux only)
   ./docker-run.sh start
   ```

2. View logs:
   ```
   ./docker-run.sh logs
   ```

3. Stop the container:
   ```
   ./docker-run.sh stop
   ```

Additional Docker commands are available in the `docker-run.sh` script.

## Configuration
The agent can be configured by modifying the JSON files in the `config` directory. The default configuration is in `config/default_config.json`.

## Contributing
This is a private repository. Please contact the repository owner for contribution guidelines.

## License
All rights reserved. This code is not licensed for use, reproduction, or distribution.