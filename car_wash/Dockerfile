# Stage 1: Builder
# We use this stage to prepare dependencies and users, keeping the final image clean.
FROM python:3.11-alpine AS builder

# Prevent python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Install build dependencies if needed (none for the current simple script, but good practice)
# RUN apk add --no-cache build-base

# Create a dedicated non-root user and group
# using a specific UID/GID helps with mapping permissions on the host
RUN addgroup -g 1000 appgroup && \
    adduser -u 1000 -G appgroup -h /home/appuser -D appuser

# Stage 2: Runtime
# This is the final, immutable image.
FROM python:3.11-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Import user and group from builder
COPY --from=builder /etc/passwd /etc/passwd
COPY --from=builder /etc/group /etc/group

# Set the working directory
WORKDIR /app

# Copy the application code
# Owned by root, read-only for the appuser
COPY --chown=root:root car_wash.py .

# Create directory structure for data
# These are mount points. We create them so permissions can be set on the mount points if needed,
# though with read-only root, we rely on the volume mounts being correct.
RUN mkdir -p /data/input /data/output

# Switch to the non-root user
USER appuser

# Define volumes
VOLUME ["/data/input", "/data/output"]

# Healthcheck (Optional, but good for hardening)
# Since we don't have curl/wget installed in a minimal image usually,
# and this is a script loop, we might skip it or use a simple python check.
# For now, we omit to keep the image minimal.

# Command to run the application
CMD ["python", "car_wash.py"]
