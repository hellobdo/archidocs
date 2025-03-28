FROM python:3.12-slim

# Install system dependencies including LibreOffice
RUN apt-get update && apt-get install -y \
    libreoffice \
    libreoffice-writer \
    libreoffice-base \
    libreoffice-calc \
    --no-install-recommends \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Create outputs directory
RUN mkdir -p outputs

# Expose the port that the application will run on
EXPOSE 8501

# Command to run the application
CMD ["streamlit", "run", "frontend/app.py"] 