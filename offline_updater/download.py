import json
import os
import subprocess
import sys

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "config.json")

    if not os.path.exists(config_path):
        print(f"Error: Config file not found at {config_path}")
        sys.exit(1)

    try:
        with open(config_path, "r") as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error parsing config file: {e}")
        sys.exit(1)

    apt_packages = config.get("apt_packages", [])
    pip_packages = config.get("pip_packages", [])
    download_dir_name = config.get("download_dir", "updates")

    # Resolve download directory relative to the script location
    download_dir = os.path.join(script_dir, download_dir_name)

    apt_dir = os.path.join(download_dir, "apt")
    pip_dir = os.path.join(download_dir, "pip")

    os.makedirs(apt_dir, exist_ok=True)
    # apt-get often requires a 'partial' directory inside the archives directory
    os.makedirs(os.path.join(apt_dir, "partial"), exist_ok=True)

    os.makedirs(pip_dir, exist_ok=True)

    print(f"Download directory: {download_dir}")

    # APT Update
    print("Updating APT repositories...")
    try:
        subprocess.run(["sudo", "apt-get", "update"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error updating APT: {e}")
        print("Continuing, but downloads might fail if metadata is outdated.")
    except FileNotFoundError:
        print("Error: 'sudo' or 'apt-get' not found. Are you on a Debian/Ubuntu system?")

    # APT Download
    if apt_packages:
        print(f"Downloading APT packages: {', '.join(apt_packages)}")
        # We use --reinstall to ensure we get the package even if installed
        # We use -o Dir::Cache::Archives to specify where to save

        cmd = [
            "sudo", "apt-get", "install", "--download-only", "-y", "--reinstall",
            "-o", f"Dir::Cache::Archives={apt_dir}",
        ] + apt_packages

        try:
            subprocess.run(cmd, check=True)
            print("APT packages downloaded successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error downloading APT packages: {e}")
        except FileNotFoundError:
            print("Error: 'sudo' or 'apt-get' not found. Skipping APT download.")
    else:
        print("No APT packages specified.")

    # PIP Download
    if pip_packages:
        print(f"Downloading PIP packages: {', '.join(pip_packages)}")
        cmd = [
            sys.executable, "-m", "pip", "download", "--dest", pip_dir
        ] + pip_packages

        try:
            subprocess.run(cmd, check=True)
            print("PIP packages downloaded successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error downloading PIP packages: {e}")
    else:
        print("No PIP packages specified.")

    print("Download process complete.")
    print(f"Files are located in: {download_dir}")

if __name__ == "__main__":
    main()
