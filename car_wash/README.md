# Immutable Car Wash Container

This directory contains a secure, immutable Docker setup for a file sanitation "car wash" script.

## Structure

*   `car_wash.py`: The application script (simulates file sanitation).
*   `Dockerfile`: Builds the immutable container image.
*   `docker-compose.yml`: Orchestrates the service with read-only root filesystem and volume mounts.

## Running the Car Wash

1.  Create input and output directories on your host:
    ```bash
    mkdir input output
    # Ensure the output directory is writable by the container user (UID 1000)
    # This is important because the container cannot change permissions of mounted volumes
    sudo chown 1000:1000 output
    ```
2.  Add files to `input/`.
3.  Start the container:
    ```bash
    docker-compose up -d --build
    ```
4.  Check `output/` for processed files.
5.  View logs:
    ```bash
    docker-compose logs -f
    ```

## Immutable Design

*   **Read-Only Root Filesystem**: The container runs with `read_only: true`, preventing any modification to system files or application code at runtime.
*   **Non-Root User**: Runs as a dedicated `appuser` (UID 1000).
*   **Ephemeral State**: All writable data is confined to explicit volumes (`/data/output`) or memory-backed tmpfs (`/tmp`), meaning no state persists in the container layer itself.

## GPU / VRAM Usage

You asked about using VRAM (GPU access) in Docker containers. Yes, this is possible and commonly used for tasks like AI/ML (e.g., using Whisper for dictation).

### Prerequisites

1.  **NVIDIA Drivers**: Installed on the host machine.
2.  **NVIDIA Container Toolkit**: Must be installed and configured.
    *   Installation guide: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html

### Enabling GPU in Docker

**Using Docker CLI:**
Add the `--gpus` flag:
```bash
docker run --rm --gpus all nvidia/cuda:11.0.3-base-ubuntu20.04 nvidia-smi
```

**Using Docker Compose:**
You need to modify `docker-compose.yml` to request GPU resources.

Example modification for `car-wash/docker-compose.yml`:

```yaml
services:
  car-wash:
    # ... other config ...
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1 # or 'all'
              capabilities: [gpu]
```

**Important Notes for GPU:**
1.  **Base Image**: You will likely need to switch from `python:3.9-slim` to an NVIDIA CUDA base image (e.g., `nvidia/cuda:11.8.0-base-ubuntu22.04`) or a framework-specific image (e.g., `pytorch/pytorch`) to have the necessary drivers and libraries inside the container.
2.  **Compatibility**: Ensure the CUDA version in the container matches or is compatible with the host driver version.
