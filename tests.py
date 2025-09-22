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

    def test_calculator_pkg(self):
        result = get_files_content.get_file_content("calculator", "pkg/calculator.py")
        print(result)
        self.assertIn("class Calculator:", result)

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


class TestWriteFile(unittest.TestCase):
    def test_write_file_success(self):
        from functions.write_file import write_file

        result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
        print(result)
        self.assertIn('Successfully wrote to "lorem.txt"', result)

    def test_write_file_outside_working_directory(self):
        from functions.write_file import write_file

        result = write_file("calculator", "../outside.txt", "This should fail.")
        print(result)
        self.assertEqual(
            result,
            "Error: Cannot read ../outside.txt as it is outside the permitted working directory",
        )

    def test_write_file_invalid_path(self):
        from functions.write_file import write_file

        result = write_file("calculator", "/invalid_path/test.txt", "This should fail.")
        print(result)
        self.assertIn("Error:", result)

    def test_write_file_success_subdir(self):
        from functions.write_file import write_file

        result = write_file(
            "calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"
        )
        print(result)
        self.assertIn('Successfully wrote to "pkg/morelorem.txt"', result)

class TestRunPythonFile(unittest.TestCase):
    def test_run_python_file_success(self):
        from functions.run_python_file import run_python_file
        result = run_python_file("calculator", "main.py", ["2", "+", "2"])
        print(result)
        self.assertIn('STDOUT:', result)    
    def test_run_python_file_success_without_command(self):
        from functions.run_python_file import run_python_file
        result = run_python_file("calculator", "main.py")
        print(result)
        self.assertIn('STDOUT:', result)
    def test_run_python_file_outside_working_directory(self):
        from functions.run_python_file import run_python_file
        result = run_python_file("calculator", "../main.py")
        print(result)
        self.assertEqual(
            result,
            'Error: Cannot execute "../main.py" as it is outside the permitted working directory',
        )
    def test_run_python_file_non_existent(self):
        from functions.run_python_file import run_python_file
        result = run_python_file("calculator", "nonexistent.py")
        print(result)
        self.assertEqual(result, 'Error: File "nonexistent.py" not found')
    def test_run_python_file_not_a_python_file(self):
        from functions.run_python_file import run_python_file
        result = run_python_file("calculator", "lorem.txt")
        print(result)
        self.assertEqual(result, "Error: lorem.txt is not a Python file.")
    def test_runs_tests(self):
        from functions.run_python_file import run_python_file
        result = run_python_file("calculator", "tests.py")
        print(result)
        

if __name__ == "__main__":
    unittest.main()
