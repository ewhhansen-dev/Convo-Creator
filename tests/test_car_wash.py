import os
import shutil
import tempfile
import unittest
import sys

# Add root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from car_wash.car_wash import process_files

class TestCarWash(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.input_dir = os.path.join(self.test_dir, "input")
        self.output_dir = os.path.join(self.test_dir, "output")
        os.makedirs(self.input_dir)
        os.makedirs(self.output_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_process_files_new_file(self):
        # Create a file in input
        with open(os.path.join(self.input_dir, "test.txt"), "w") as f:
            f.write("hello")

        process_files(self.input_dir, self.output_dir)

        # Check if it exists in output
        output_path = os.path.join(self.output_dir, "test.txt")
        self.assertTrue(os.path.exists(output_path))
        with open(output_path, "r") as f:
            self.assertIn("# SANITIZED BY CAR WASH", f.read())

    def test_process_files_already_exists(self):
        # Create a file in input
        with open(os.path.join(self.input_dir, "test.txt"), "w") as f:
            f.write("hello")

        # Create it in output already with different content
        with open(os.path.join(self.output_dir, "test.txt"), "w") as f:
            f.write("already processed")

        process_files(self.input_dir, self.output_dir)

        # Check it wasn't overwritten
        with open(os.path.join(self.output_dir, "test.txt"), "r") as f:
            self.assertEqual(f.read(), "already processed")

    def test_process_files_skips_hidden(self):
        with open(os.path.join(self.input_dir, ".hidden"), "w") as f:
            f.write("hidden")

        process_files(self.input_dir, self.output_dir)
        self.assertFalse(os.path.exists(os.path.join(self.output_dir, ".hidden")))

if __name__ == "__main__":
    unittest.main()
