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

    print(f"Generating {num_entries} entries in {input_dir}...")
    start_gen = time.perf_counter()

    # Create mostly directories and hidden files to stress test the filtering logic
    # where the optimization is most effective (avoiding stat calls).
    for i in range(num_entries):
        if i % 2 == 0:
            # Subdirectory
            os.makedirs(os.path.join(input_dir, f"dir_{i}"), exist_ok=True)
        else:
            # Hidden file
            with open(os.path.join(input_dir, f".hidden_{i}"), "w") as f:
                f.write("test")

    end_gen = time.perf_counter()
    print(f"Generation took {end_gen - start_gen:.2f} seconds.")
    return input_dir, output_dir

def run_benchmark():
    with tempfile.TemporaryDirectory() as temp_dir:
        input_dir, output_dir = setup_test_env(temp_dir)

        print("Running benchmark...")
        start_time = time.perf_counter()
        # We run it once. The function returns (void) but processes the list.
        process_files(input_dir, output_dir)
        end_time = time.perf_counter()

        duration = end_time - start_time
        print(f"Traversal processed in {duration:.4f} seconds.")
        return duration

if __name__ == "__main__":
    run_benchmark()
