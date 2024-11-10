# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv and manage environment
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

RUN uv venv
RUN . .venv/bin/activate && uv pip install -e .

# Expose the port the app runs on
EXPOSE 5010

# Run the application
CMD [".venv/bin/python", "src/predict.py"]