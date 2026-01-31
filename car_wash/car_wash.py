import sys
import os
import tempfile
import shutil

def sanitize_file(input_path, output_path):
    filename = os.path.basename(input_path)
    print(f"Processing {filename}...")

    # Resolve paths to absolute to correctly check for same file (implicit in logic)
    abs_output = os.path.abspath(output_path)
    output_dir = os.path.dirname(abs_output)

    # Ensure output directory exists (if empty string, it means current dir)
    if output_dir and not os.path.exists(output_dir):
         # If strict, we might fail here, but let's assume valid path provided or let open fail
         pass

    # Use a temporary file for writing to allow in-place modification
    # and to ensure partial writes don't corrupt the output file if logic fails.
    # We create the temp file in the same directory as output to ensure atomic move is possible.
    try:
        temp_fd, temp_path = tempfile.mkstemp(dir=output_dir if output_dir else '.', text=True)
        os.close(temp_fd) # Close the low-level handle immediately
    except OSError as e:
        print(f"Error creating temp file: {e}")
        return

    try:
        # Optimization: Read and write in chunks to avoid loading full file into memory
        chunk_size = 64 * 1024  # 64KB chunks

        with open(input_path, 'r', encoding='utf-8', errors='ignore') as f_in, \
             open(temp_path, 'w', encoding='utf-8') as f_out:

            while True:
                chunk = f_in.read(chunk_size)
                if not chunk:
                    break
                f_out.write(chunk)

            f_out.write("\n# SANITIZED BY CAR WASH")

        # If successful, move temp file to output path
        # shutil.move handles overwrite
        shutil.move(temp_path, output_path)

    except Exception as e:
        print(f"Error: {e}")
        # Clean up temp file on error
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python car_wash.py <input> <output>")
        sys.exit(1)

    sanitize_file(sys.argv[1], sys.argv[2])
