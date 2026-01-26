import json
import os
import subprocess
import sys
import glob

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "config.json")

    # Try to load config to get download_dir, otherwise default
    download_dir_name = "updates"
    pip_packages = []

    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
                download_dir_name = config.get("download_dir", "updates")
                pip_packages = config.get("pip_packages", [])
        except Exception as e:
            print(f"Warning: Could not load config: {e}. Using defaults.")
    else:
        print("Config file not found. Assuming default directory structure.")

    download_dir = os.path.join(script_dir, download_dir_name)
    apt_dir = os.path.join(download_dir, "apt")
    pip_dir = os.path.join(download_dir, "pip")

    if not os.path.exists(download_dir):
        print(f"Error: Updates directory not found at {download_dir}")
        sys.exit(1)

    # APT Install
    deb_files = glob.glob(os.path.join(apt_dir, "*.deb"))
    if deb_files:
        print(f"Found {len(deb_files)} Debian packages to install.")
        print("Installing APT packages...")
        # Passing absolute paths to apt-get install works and treats them as files
        cmd = ["sudo", "apt-get", "install", "-y"] + deb_files

        try:
            subprocess.run(cmd, check=True)
            print("APT packages installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error installing APT packages: {e}")
            print("Trying 'dpkg -i' as fallback...")
            try:
                subprocess.run(["sudo", "dpkg", "-i"] + deb_files, check=True)
            except subprocess.CalledProcessError as e2:
                print(f"Error with dpkg: {e2}")
                print("Try running 'sudo apt-get install -f' manually.")
        except FileNotFoundError:
             print("Error: 'sudo' or 'apt-get' not found. Skipping APT install.")
    else:
        print("No Debian packages found in apt directory.")

    # PIP Install
    if pip_packages:
        print(f"Installing PIP packages: {', '.join(pip_packages)}")
        cmd = [
            sys.executable, "-m", "pip", "install",
            "--no-index",
            "--find-links", pip_dir
        ] + pip_packages

        try:
            subprocess.run(cmd, check=True)
            print("PIP packages installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error installing PIP packages: {e}")
    else:
        # Fallback if no specific packages listed but files exist
        whl_files = glob.glob(os.path.join(pip_dir, "*.whl"))
        tar_files = glob.glob(os.path.join(pip_dir, "*.tar.gz"))
        all_pip_files = whl_files + tar_files

        if all_pip_files:
             print("No PIP packages specified in config, attempting to install all found files...")
             cmd = [
                sys.executable, "-m", "pip", "install",
                "--no-index",
                "--find-links", pip_dir
             ] + all_pip_files
             try:
                subprocess.run(cmd, check=True)
                print("PIP packages installed successfully.")
             except subprocess.CalledProcessError as e:
                print(f"Error installing PIP packages: {e}")
        else:
             print("No PIP packages specified and no files found.")

    print("Installation process complete.")

if __name__ == "__main__":
    main()
