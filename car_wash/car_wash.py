import os
import time
import sys

def process_files(input_dir, output_dir):
    if not os.path.exists(input_dir):
        print(f"Input directory {input_dir} does not exist. Waiting...")
        return

    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
        except OSError as e:
            print(f"Error creating output directory {output_dir}: {e}")
            return

    print(f"Scanning {input_dir} for files...")
    try:
        with os.scandir(input_dir) as it:
            for entry in it:
                filename = entry.name
                # Skip hidden files or directories
                if filename.startswith('.') or not entry.is_file():
                    continue

                input_path = entry.path
                output_path = os.path.join(output_dir, filename)

                # Only process if output doesn't exist (avoid re-processing loops for this demo)
                if os.path.exists(output_path):
                    continue

                print(f"Processing {filename}...")
                try:
                    # Simulate sanitation
                    with open(input_path, 'r', encoding='utf-8', errors='ignore') as f_in:
                        content = f_in.read()

                    sanitized_content = content + "\n# SANITIZED BY CAR WASH"

                    with open(output_path, 'w', encoding='utf-8') as f_out:
                        f_out.write(sanitized_content)
                    print(f"Saved to {output_path}")
                except Exception as e:
                    print(f"Failed to process {filename}: {e}")

    except OSError as e:
        print(f"Error reading input directory: {e}")
        return

if __name__ == "__main__":
    # Use absolute paths for Docker volume mounting convenience
    INPUT_DIR = os.getenv("INPUT_DIR", "/data/input")
    OUTPUT_DIR = os.getenv("OUTPUT_DIR", "/data/output")

    print(f"Starting Car Wash Service.")
    print(f"Input Directory: {INPUT_DIR}")
    print(f"Output Directory: {OUTPUT_DIR}")

    # Continuous loop to simulate a service
    while True:
        process_files(INPUT_DIR, OUTPUT_DIR)
        sys.stdout.flush() # Ensure logs are printed in Docker
        time.sleep(10)
