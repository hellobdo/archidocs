# Base stage with common dependencies
FROM python:3.11-slim AS base

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
    bash \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create and set working directory
WORKDIR /app

# Create necessary directories
RUN mkdir -p outputs templates/html test_outputs

# Add app directory to Python path
ENV PYTHONPATH=/app

# Development stage with testing dependencies
FROM base AS dev
# Copy all requirements from docker directory
COPY docker/requirements.txt ./requirements.txt
COPY docker/requirements-dev.txt ./requirements-dev.txt
# Install both sets of dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -r requirements-dev.txt

# Copy all application code including tests
COPY . /app/

# Default command for development (interactive shell)
CMD ["/bin/bash"]

# Production stage
FROM base AS prod
# Only copy production requirements
COPY docker/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy only what's needed for production (explicitly exclude tests)
COPY backend /app/backend
COPY frontend /app/frontend
COPY app.py /app/
# Add any other necessary files here...

# Command to run the application
CMD ["python", "-m", "backend.backend.main"] 