import os
import time

def process_file(filepath):
    # Simulate processing
    pass

def car_wash_loop(input_dir, output_dir, single_pass=False):
    """
    Simulates a polling loop that processes files.
    single_pass: If True, runs only one iteration of the loop (for benchmarking).
    """
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"Starting loop for {input_dir} -> {output_dir}")
    while True:
        try:
            files = os.listdir(input_dir)
        except OSError:
            files = []

        # Optimize: Batch check for existing output files to avoid N * stat calls
        try:
            existing_outputs = set(os.listdir(output_dir))
        except OSError:
            existing_outputs = set()

        for filename in files:
            # Only process if output doesn't exist (avoid re-processing loops for this demo)
            if filename in existing_outputs:
                continue

            output_path = os.path.join(output_dir, filename)
            print(f"Processing {filename}...")
            # process
            process_file(os.path.join(input_dir, filename))
            # Create output file to simulate completion
            with open(output_path, 'w') as f:
                f.write("done")

        if single_pass:
            break

        time.sleep(0.1)

if __name__ == "__main__":
    # Ensure dirs exist
    os.makedirs("in", exist_ok=True)
    os.makedirs("out", exist_ok=True)
    car_wash_loop("in", "out")
