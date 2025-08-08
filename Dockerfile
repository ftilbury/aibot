# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Install system dependencies needed for MetaTrader5 (X11 libs) and other
# scientific libraries. These may vary depending on your environment.
RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Create application directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . ./

# Default command to run when starting the container
CMD ["python", "-m", "main"]