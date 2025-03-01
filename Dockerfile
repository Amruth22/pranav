# Use Python 3.10 as the base image
FROM python:3.10-slim

# Set working directory in the container
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files into the container
COPY . .

# Create a non-root user and switch to it
RUN useradd -m pranav && \
    chown -R pranav:pranav /app
USER pranav

# Create necessary directories with proper permissions
RUN mkdir -p logs

# Set the entrypoint to run the agent
ENTRYPOINT ["python", "examples/basic_usage.py"]

# Default command (can be overridden)
CMD []