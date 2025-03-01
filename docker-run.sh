#!/bin/bash
# Script to build and run the Pranav agent Docker container

# Ensure the script exits on any error
set -e

# Create logs directory if it doesn't exist
mkdir -p logs

# Function to display usage information
show_usage() {
  echo "Usage: $0 [OPTION]"
  echo "Options:"
  echo "  build    - Build the Docker image"
  echo "  run      - Run the Docker container"
  echo "  start    - Build and run the Docker container"
  echo "  stop     - Stop the running container"
  echo "  restart  - Restart the container"
  echo "  logs     - Show container logs"
  echo "  shell    - Open a shell in the running container"
  echo "  help     - Show this help message"
}

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
  echo "Error: Docker is not installed or not in PATH"
  exit 1
fi

# Process command line arguments
case "$1" in
  build)
    echo "Building Pranav agent Docker image..."
    docker build -t pranav-agent .
    ;;
  
  run)
    echo "Running Pranav agent container..."
    docker run --name pranav-agent -v "$(pwd)/config:/app/config" -v "$(pwd)/logs:/app/logs" pranav-agent
    ;;
  
  start)
    echo "Starting Pranav agent with docker-compose..."
    docker-compose up -d
    echo "Container started. Use '$0 logs' to see the output."
    ;;
  
  stop)
    echo "Stopping Pranav agent container..."
    docker-compose down
    ;;
  
  restart)
    echo "Restarting Pranav agent container..."
    docker-compose restart
    ;;
  
  logs)
    echo "Showing logs for Pranav agent container..."
    docker-compose logs -f
    ;;
  
  shell)
    echo "Opening shell in Pranav agent container..."
    docker exec -it pranav-agent /bin/bash
    ;;
  
  help|*)
    show_usage
    ;;
esac