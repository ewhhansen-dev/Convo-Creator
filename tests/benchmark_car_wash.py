import os
import time
import shutil
import tempfile
import sys

# Ensure repo root is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from car_wash.car_wash import car_wash_loop

def benchmark():
    # Create temp directories
    with tempfile.TemporaryDirectory() as tmp_dir:
        input_dir = os.path.join(tmp_dir, "input")
        output_dir = os.path.join(tmp_dir, "output")
        os.makedirs(input_dir)
        os.makedirs(output_dir)

        # Create many files in input and output to simulate a steady state
        # where most files are already processed.
        num_files = 50000
        print(f"Creating {num_files} dummy files...")
        for i in range(num_files):
            filename = f"file_{i}.txt"
            with open(os.path.join(input_dir, filename), 'w') as f:
                f.write("data")
            with open(os.path.join(output_dir, filename), 'w') as f:
                f.write("done")

        print("Starting benchmark...")
        start_time = time.time()

        # Run one pass of the loop
        car_wash_loop(input_dir, output_dir, single_pass=True)

        end_time = time.time()
        duration = end_time - start_time
        print(f"Time taken for {num_files} files: {duration:.4f} seconds")

if __name__ == "__main__":
    benchmark()
