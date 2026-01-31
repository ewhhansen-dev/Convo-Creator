import unittest
import os
import shutil
import sys

# Ensure we can import from the root directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from car_wash.car_wash import sanitize_file

class TestCarWash(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_data"
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        os.makedirs(self.test_dir)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_sanitize_small_file(self):
        input_path = os.path.join(self.test_dir, "input.txt")
        output_path = os.path.join(self.test_dir, "output.txt")

        content = "Hello, this is a test."
        with open(input_path, "w", encoding="utf-8") as f:
            f.write(content)

        sanitize_file(input_path, output_path)

        with open(output_path, "r", encoding="utf-8") as f:
            result = f.read()

        expected = content + "\n# SANITIZED BY CAR WASH"
        self.assertEqual(result, expected)

    def test_sanitize_empty_file(self):
        input_path = os.path.join(self.test_dir, "empty.txt")
        output_path = os.path.join(self.test_dir, "empty_output.txt")

        with open(input_path, "w", encoding="utf-8") as f:
            pass

        sanitize_file(input_path, output_path)

        with open(output_path, "r", encoding="utf-8") as f:
            result = f.read()

        expected = "\n# SANITIZED BY CAR WASH"
        self.assertEqual(result, expected)

    def test_sanitize_inplace(self):
        input_path = os.path.join(self.test_dir, "inplace.txt")

        content = "This content should be preserved and appended to."
        with open(input_path, "w", encoding="utf-8") as f:
            f.write(content)

        sanitize_file(input_path, input_path)

        with open(input_path, "r", encoding="utf-8") as f:
            result = f.read()

        expected = content + "\n# SANITIZED BY CAR WASH"
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
