# Offline Updater Tools

This set of scripts allows you to download updates and dependencies for APT (Debian/Ubuntu) and PIP (Python) packages on an online machine, and then install them on an offline machine.

## Prerequisites

*   **Online Machine:**
    *   Ubuntu 24 (or compatible)
    *   Python 3
    *   `pip` installed
*   **Offline Machine:**
    *   Ubuntu 24 (or compatible)
    *   Python 3 installed

## Configuration

Edit `config.json` to specify the packages you want to download.

```json
{
    "apt_packages": [
        "curl",
        "git",
        "htop"
    ],
    "pip_packages": [
        "requests",
        "numpy"
    ],
    "download_dir": "updates"
}
```

*   `apt_packages`: List of system packages to download.
*   `pip_packages`: List of Python packages to download.
*   `download_dir`: Name of the directory where files will be saved (relative to the script).

## Usage

### Step 1: Download Updates (Online Machine)

1.  Navigate to the `offline_updater` directory.
2.  Run the downloader script:
    ```bash
    sudo python3 download.py
    ```
    *Note: `sudo` is required for `apt-get` operations.*

    This will create an `updates` directory (or whatever you named it in `config.json`) containing `apt` and `pip` subdirectories with the downloaded files.

### Step 2: Transfer to Offline Machine

1.  Copy the entire `offline_updater` folder (including the scripts and the `updates` directory) to an external drive (USB stick, HDD, etc.).
2.  Connect the drive to the offline machine.
3.  Copy the folder from the drive to the offline machine (optional, but recommended for speed).

### Step 3: Install Updates (Offline Machine)

1.  Navigate to the `offline_updater` directory on the offline machine.
2.  Run the installer script:
    ```bash
    sudo python3 install.py
    ```

    The script will install the APT packages from the local folder and then the PIP packages.

## Troubleshooting & Notes

*   **Missing Dependencies:** If `apt-get` complains about missing dependencies on the offline machine, it might be because the online machine already had them installed, so `apt-get download` didn't fetch them. To fix this, try to ensure the online machine is as clean as possible or use a VM that mirrors the offline machine's state.
*   **Permissions:** Ensure you run the scripts with `sudo` as installing packages requires root privileges.
*   **Ubuntu 24.04 & Python (PEP 668):** Ubuntu 24.04 protects the system Python environment. If `pip install` fails with an "externally-managed-environment" error, consider:
    1.  Installing the package via `apt` instead (add `python3-<package>` to `apt_packages` in `config.json`).
    2.  Creating and activating a virtual environment on the offline machine before running the install script.
