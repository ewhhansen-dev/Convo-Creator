import os
import time
import tempfile
import sys
import shutil

# Add the root directory to sys.path so we can import car_wash
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from car_wash.car_wash import process_files

def setup_test_env(base_dir, num_entries=20000):
    input_dir = os.path.join(base_dir, "input")
    output_dir = os.path.join(base_dir, "output")
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    print(f"Generating {num_entries} files in {input_dir} and {output_dir}...")
    start_gen = time.perf_counter()

    for i in range(num_entries):
        filename = f"file_{i}.txt"
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)

        with open(input_path, "w") as f:
            f.write("test")

        # Also create in output dir to trigger the 'continue'
        with open(output_path, "w") as f:
            f.write("test sanitized")

    end_gen = time.perf_counter()
    print(f"Generation took {end_gen - start_gen:.2f} seconds.")
    return input_dir, output_dir

def run_benchmark():
    with tempfile.TemporaryDirectory() as temp_dir:
        input_dir, output_dir = setup_test_env(temp_dir, 20000)

        print("Running benchmark...")

        # Redirect stdout to devnull to avoid cluttering benchmark results with "Scanning..." and "Processing..."
        original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

        try:
            # Warm up
            process_files(input_dir, output_dir)

            start_time = time.perf_counter()
            # Run multiple times to get a better average
            iterations = 10
            for _ in range(iterations):
                process_files(input_dir, output_dir)
            end_time = time.perf_counter()
        finally:
            sys.stdout.close()
            sys.stdout = original_stdout

        duration = (end_time - start_time) / iterations
        print(f"Average traversal processed in {duration:.4f} seconds.")
        return duration

if __name__ == "__main__":
    run_benchmark()
