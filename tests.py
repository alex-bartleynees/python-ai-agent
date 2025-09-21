import unittest
from functions import get_files_info, get_files_content


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


class TestGetFilesContent(unittest.TestCase):
    def test_calculator_main_py(self):
        result = get_files_content.get_file_content("calculator", "main.py")
        print(result)
        self.assertIn("def main():", result)

    def test_calculator_pkg_render_py(self):
        result = get_files_content.get_file_content("calculator", "pkg/render.py")
        print(result)
        self.assertIn("def format_json_output(", result)

    def test_outside_working_directory(self):
        result = get_files_content.get_file_content("calculator", "../somefile.py")
        print(result)
        self.assertEqual(
            result,
            "Error: Cannot read ../somefile.py as it is outside the permitted working directory",
        )

    def test_non_existent_file(self):
        result = get_files_content.get_file_content(
            "calculator", "non_existent_file.py"
        )
        print(result)
        self.assertEqual(result, "Error: non_existent_file.py does not exist")


if __name__ == "__main__":
    unittest.main()
