# Use an official Python runtime as a parent image
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install wget, curl, and ffmpeg
RUN apt-get update && \
    apt-get install -y wget curl ffmpeg git && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir accelerate

# Copy all files to the container
COPY . .

# Set the Python file to run
ARG PYTHON_FILE=server.py
ENV PYTHON_FILE=${PYTHON_FILE}

# Run the specified Python file when the container launches
CMD ["sh", "-c", "python ${PYTHON_FILE}"]
