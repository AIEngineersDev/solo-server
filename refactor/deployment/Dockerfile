# Use the official Python image from the Docker Hub as the base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install git to clone the repository
RUN apt-get update && apt-get install -y git && apt-get clean

# Clone the repository
RUN git clone https://github.com/AIEngineersDev/solo-server.git /app/solo-server

# Set the working directory to the cloned repository
WORKDIR /app/solo-server

# Copy the requirements file to the container
COPY requirements.txt /app/solo-server/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that FastAPI will run on
EXPOSE 8000

# Command to run FastAPI server
CMD ["fastapi", "dev", "server.py", "--host", "0.0.0.0", "--port", "8000", "--reload"]
