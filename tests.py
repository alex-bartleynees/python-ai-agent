import unittest
import os
from functions import get_files_info


class TestGetFilesInfo(unittest.TestCase):
    def test_calculator_dir(self):
        result = get_files_info.get_files_info("calculator", ".")
        print(result)
        self.assertIn("main.py: file_size:", result)

    def test_calculator_pkg_dir(self):
        result = get_files_info.get_files_info("calculator", "pkg")
        print(result)
        self.assertIn("render.py: file_size:", result)

    def test_outside_working_directory(self):
        result = get_files_info.get_files_info("calculator", "../")
        print(result)
        self.assertEqual(
            result,
            "Error: Cannot list ../ as it is outside the permitted working directory",
        )

    def test_non_existent_directory(self):
        result = get_files_info.get_files_info("calculator", "non_existent_dir")
        print(result)
        self.assertEqual(result, "Error: non_existent_dir is not a directory")


if __name__ == "__main__":
    unittest.main()
