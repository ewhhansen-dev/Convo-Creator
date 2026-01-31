import os
import shutil
import tempfile
import unittest
import sys

# Ensure repo root is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from car_wash.car_wash import car_wash_loop

class TestCarWash(unittest.TestCase):
    def test_optimization_correctness(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            input_dir = os.path.join(tmp_dir, "input")
            output_dir = os.path.join(tmp_dir, "output")
            os.makedirs(input_dir)
            os.makedirs(output_dir)

            # Create files in input
            files = ["a.txt", "b.txt", "c.txt"]
            for f in files:
                with open(os.path.join(input_dir, f), 'w') as fh:
                    fh.write("content")

            # Create 'a.txt' in output with specific content to verify it's NOT touched
            with open(os.path.join(output_dir, "a.txt"), 'w') as fh:
                fh.write("old_done")

            # Run loop once
            car_wash_loop(input_dir, output_dir, single_pass=True)

            # Check results
            with open(os.path.join(output_dir, "a.txt"), 'r') as fh:
                content = fh.read()

            # Optimization: if it exists, we skip. So content should be "old_done".
            self.assertEqual(content, "old_done", "Should skip existing files")

            # b.txt and c.txt should be created and contain "done"
            for f in ["b.txt", "c.txt"]:
                self.assertTrue(os.path.exists(os.path.join(output_dir, f)))
                with open(os.path.join(output_dir, f), 'r') as fh:
                    self.assertEqual(fh.read(), "done")

if __name__ == "__main__":
    unittest.main()
