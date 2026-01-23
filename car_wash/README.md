# Immutable "Car Wash" Container

This directory contains a **hardened, lead-lined Docker setup** for file sanitation. It implements a "Digital Clean Room" approach, ensuring that the sanitation process occurs in a strictly isolated, ephemeral, and immutable environment.

## Security Architecture

This setup draws inspiration from high-security projects like *entrusted*, *AzureTRE*, and *dangerzone*.

### 1. The "Air Gap" (Network Isolation)
*   **Implementation**: `network_mode: none`
*   **Effect**: The container has **zero** network access. It cannot download malware, connect to a Command & Control (C2) server, or exfiltrate data. It is a pure function: `Input -> [Sanitization] -> Output`.

### 2. Immutable Infrastructure
*   **Implementation**: `read_only: true` (Docker Compose) and root-owned application code (Dockerfile).
*   **Effect**: The root filesystem cannot be modified. Even if an attacker gains code execution, they cannot install tools, modify the application, or persist malware in the system layers.

### 3. Least Privilege & Containment
*   **Implementation**:
    *   `cap_drop: [ALL]`: All Linux capabilities (like `NET_ADMIN`, `SYS_ADMIN`) are stripped.
    *   `security_opt: [no-new-privileges:true]`: Prevents privilege escalation (e.g., via setuid binaries).
    *   **Resource Limits**: CPU (0.5 cores) and Memory (512MB) are capped to prevent DoS attacks.
    *   **Non-Root User**: Runs as UID 1000.

### 4. The "Airlock" Data Flow
*   **Input**: Mounted as **Read-Only** (`:ro`). The container cannot tamper with the source evidence.
*   **Output**: Mounted as Read-Write. Ideally, a separate process on the host should move files out of `output` to a clean destination, verifying that the container has finished.

## Usage

1.  **Prepare the Host**:
    ```bash
    mkdir -p input output
    # Ensure the output directory is writable by UID 1000
    chown 1000:1000 output
    ```

2.  **Run the Clean Room**:
    ```bash
    docker-compose up -d --build
    ```

3.  **Process**:
    *   Drop files into `./input`.
    *   The sanitized files appear in `./output`.

## VRAM / GPU Support (Advanced)

While the default setup is "lead-lined" (software only), some CDR tools (like *ArielCyber/ICDR*) may require GPU acceleration.

**Warning**: Enabling GPU access punches a hole in the isolation (device access).

To enable GPU support with the NVIDIA Container Toolkit:

1.  **Modify `docker-compose.yml`**:
    *   You must *remove* `cap_drop: [ALL]` or explicitly add back capabilities required by the NVIDIA driver (often `utility`, `compute`).
    *   Add the device reservation:
    ```yaml
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    ```

2.  **Base Image**:
    *   Switch `FROM python:3.11-alpine` to an NVIDIA-supported image (e.g., `nvidia/cuda:11.8.0-runtime-ubuntu22.04`). *Note: Alpine does not officially support the proprietary NVIDIA driver stack well; Ubuntu/Debian is recommended for GPU workloads.*
