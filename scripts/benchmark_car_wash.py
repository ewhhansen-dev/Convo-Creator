import subprocess
import os
import time
import sys
import resource

def benchmark(size_mb=100):
    input_file = "large_input.txt"
    output_file = "large_output.txt"

    # Ensure clean slate
    if os.path.exists(input_file):
        os.remove(input_file)
    if os.path.exists(output_file):
        os.remove(output_file)

    print(f"Generating {size_mb}MB file...")
    # Writing text content since the script uses 'r' (text mode) encoding='utf-8'
    # Random bytes might not be valid utf-8, causing errors='ignore' to work hard or weird behavior.
    # Better to write repetitive text.
    chunk = "This is a line of text that is repeated many times to simulate content.\n"
    target_size = size_mb * 1024 * 1024
    with open(input_file, "w", encoding="utf-8") as f:
        while f.tell() < target_size:
            f.write(chunk)

    print(f"Running car_wash.py on {input_file}...")

    start_time = time.time()

    # We need to fork execution to capture RUSAGE_CHILDREN for this specific call
    # Or just rely on the cumulative usage if we are careful.
    # Since this script is the parent, RUSAGE_CHILDREN accumulates.
    # So we get usage before and after? No, it's cumulative sum.

    usage_before = resource.getrusage(resource.RUSAGE_CHILDREN)

    # Run the script
    proc = subprocess.run([sys.executable, "car_wash/car_wash.py", input_file, output_file])

    usage_after = resource.getrusage(resource.RUSAGE_CHILDREN)
    end_time = time.time()

    if proc.returncode != 0:
        print("Error: car_wash.py failed.")
        return

    # On Linux, ru_maxrss is in Kilobytes.
    # Note: RUSAGE_CHILDREN maxrss is the maximum resident set size of the largest child process,
    # OR the sum of maxrss of all children?
    # The documentation says: "The maximum resident set size used."
    # It's usually the high water mark of the children.

    # However, getrusage(RUSAGE_CHILDREN) might behave differently depending on kernel.
    # Let's verify with a simple print.

    print(f"Execution Time: {end_time - start_time:.4f}s")

    # The usage_after.ru_maxrss should contain the peak memory of the child process.
    # usage_before might be 0 if no children ran yet.

    max_rss = usage_after.ru_maxrss
    print(f"Max RSS (RUSAGE_CHILDREN): {max_rss} KB")
    print(f"Max RSS (MB): {max_rss / 1024:.2f} MB")

    # Cleanup
    if os.path.exists(input_file):
        os.remove(input_file)
    if os.path.exists(output_file):
        os.remove(output_file)

if __name__ == "__main__":
    benchmark(size_mb=100)
