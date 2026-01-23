# Use a minimal base image to reduce attack surface
FROM python:3.9-slim

# Set environment variables
# PYTHONDONTWRITEBYTECODE: Prevents Python from writing .pyc files to disk
# PYTHONUNBUFFERED: Ensures Python output is sent straight to terminal (logs)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create a non-root user and group to run the application
# It is a best practice to run containers as non-root
RUN groupadd -r appuser && useradd -r -g appuser -u 1000 appuser

# Set the working directory
WORKDIR /app

# Copy the application code
# By default, COPY creates files owned by root.
# We WANT this for the code itself, so the application cannot modify its own source code
# (immutable application code).
COPY car_wash.py .

# Create directories for data processing
# We change ownership to appuser so the application can read/write data here.
RUN mkdir -p /data/input /data/output && \
    chown -R appuser:appuser /data

# Switch to the non-root user
USER appuser

# Declare volumes for data persistence and external access
# This ensures that data is decoupled from the container's lifecycle.
VOLUME ["/data/input", "/data/output"]

# Command to run the application
CMD ["python", "car_wash.py"]
