FROM python:3.11-slim

# Install system dependencies including Ghostscript
RUN apt-get update && apt-get install -y \
    build-essential \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    ghostscript \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create and set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend code
COPY backend/backend /app/backend

# Create necessary directories
RUN mkdir -p outputs templates/html

# Add app directory to Python path
ENV PYTHONPATH=/app

# Set the entrypoint to main.py
ENTRYPOINT ["python", "-m", "backend.main"] 