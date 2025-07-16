import unittest
import re
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from config import MAX_CHARS
from functions.write_file import write_file
from functions.run_python import run_python_file

class FilesInfoTests(unittest.TestCase):
    ENTRY_RE = re.compile(r"^- (?P<name>[^:]+): file_size=(?P<size>\d+) bytes, is_dir=(?P<is_dir>True|False)$")

    def assertHasEntry(self, output: str, name: str, is_dir: bool):
        """Check that output has a line for `name`, with any integer size, and the given is_dir."""
        found = False
        for line in output.splitlines():
            m = self.ENTRY_RE.match(line.strip())
            if not m:
                continue
            if m.group("name") == name and m.group("is_dir") == str(is_dir):
                # we got the right filename & dir‑flag; size is \d+ so any number is OK
                found = True
                break
        self.assertTrue(found, f"Did not find entry for {name} in:\n{output}")

    def test_current_dir(self):
        out = get_files_info("calculator", ".")
        print('===========Test1============')
        print('Actual:')
        print(out)
        print('Expected:')
        print("Result for current directory:\n- main.py: file_size=576 bytes, is_dir=False\n- tests.py: file_size=1343 bytes, is_dir=False\n- pkg: file_size=92 bytes, is_dir=True\n") 
        print('===========Test1============')
        self.assertIn("Result for current directory:", out)
        self.assertHasEntry(out, "main.py",   is_dir=False)
        self.assertHasEntry(out, "tests.py",  is_dir=False)
        self.assertHasEntry(out, "pkg",       is_dir=True)

    def test_pkg_dir(self):
        out = get_files_info("calculator", "pkg")
        print('===========Test2============')
        print('Actual:')
        print(out)
        print('Expected:')
        print("Result for \'pkg\' directory:\n- calculator.py: file_size=1739 bytes, is_dir=False\n- render.py: file_size=768 bytes, is_dir=False\n- __pycache__: file_size=96 bytes, is_dir=True\n") 
        print('===========Test2============')
        self.assertIn("Result for \'pkg\' directory:", out)
        self.assertHasEntry(out, "calculator.py",   is_dir=False)
        self.assertHasEntry(out, "render.py",  is_dir=False)
        self.assertHasEntry(out, "__pycache__",       is_dir=True)

    def test_out_of_bounds_bin(self):
        print('===========Test3============')
        out = get_files_info("calculator", "/bin")
        print('Actual:')
        print(out)
        print('Expected:')
        print("Result for \'/bin\' directory:\nError: Cannot list \"/bin\" as it is outside the permitted working directory")
        self.assertIn("Result for \'/bin\' directory:", out)
        self.assertIn("Error: Cannot list \"/bin\" as it is outside the permitted working directory", out)
        print('===========Test3============')


    def test_out_of_bounds_parent(self):
        print('===========Test4============')
        out = get_files_info("calculator", "../")
        print('Actual:')
        print(out)
        print('Expected:')
        print("Result for \'../\' directory:\nError: Cannot list \"../\" as it is outside the permitted working directory")
        self.assertIn("Result for \'../\' directory:", out)
        self.assertIn("Error: Cannot list \"../\" as it is outside the permitted working directory", out)
        print('===========Test4============')

class GetFileContentTests(unittest.TestCase):    
#    def test_lorem(self):
#        print('=========Testing File Trunc===========')
#        out = get_file_content('calculator', 'lorem.txt')
#        print(out)
#        self.assertIn(f'"lorem.txt" truncated at {MAX_CHARS} characters', out)
#        print('=========Testing File Trunc===========')

    def test_main_py(self):
        print('====== Test read main =====')
        out = get_file_content('calculator', 'main.py')
        print(out)
        self.assertIn('def main()', out)
        print('====== Test read main =====')
        
    def test_calc_main_py(self):
        print('====== Test read calculator main =====')
        out = get_file_content('calculator', 'main.py')
        print(out)
        self.assertIn('def main()', out)
        print('====== Test read calculator main =====')
    
    def test_pkg_calc_py(self):
        print('====== Test read calculator pkg =====')
        out = get_file_content('calculator', 'pkg/calculator.py')
        print(out)
        self.assertIn('class Calculator', out)
        print('====== Test read calculator pkg =====')
    
    def test_out_of_bounds(self):
        print('====== Test out of bounds =====')
        out = get_file_content('calculator', '/bin/cat')
        print(out)
        self.assertIn('Error:', out)
        print('====== Test out of bounds  =====')
   
   
    def test_not_exists(self):
        print('====== Test not exists =====')
        out = get_file_content('calculator', 'pkg/does_not_exist.py')
        print(out)
        self.assertIn('Error:', out)
        print('====== Test not exists =====')
    
class WriteContentTests(unittest.TestCase):

    def test_lorem(self):
        print('====== Test Lorem   =====')
        out = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
        print(out)
        self.assertIn('28 characters written', out)
        print('====== Test Lorem   =====')

    def test_more_lorem(self):
        print('====== Test More Lorem   =====')
        out = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
        print(out)
        self.assertIn('26 characters written', out)
        print('====== Test More Lorem   =====')

    def test_out_of_bounds(self):
        print('====== Test out of bounds write  =====')
        out = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
        print(out)
        self.assertIn('Error:', out)
        print('====== Test out of bounds write  =====')

class RunPythonTests(unittest.TestCase):

    def test_calc_main(self):
        print('====== Test Run Calc Main  =====')
        out = run_python_file("calculator", "main.py")
        print(out)
        self.assertIn('Usage', out)
        print('======  Test Run Calc Main =====')
    
    def test_calc_add(self):
        print('====== Test Run Calc Add  =====')
        out = run_python_file("calculator", "main.py", ["3 + 5"])
        print(out)
        self.assertIn('3 + 5', out)
        print('======  Test Run Calc Add =====')
    
    def test_run_test(self):
        print('====== Test Run test  =====')
        out = run_python_file("calculator", "tests.py")
        print(out)
        # self.assertIn('3 + 5', out)
        print('======  Test Run Calc Add =====')

    def test_run_self(self):
        print('====== Test Run Self  =====')
        out = run_python_file("calculator", "../main.py")
        print(out)
        self.assertIn('Error:', out)
        print('======  Test Run Self =====')
    
    def test_run_not_exist(self):
        print('====== Test Run Imaginary  =====')
        out = run_python_file("calculator", "nonexistent.py")
        print(out)
        self.assertIn('Error:', out)
        print('======  Test Run Imaginary =====')

if __name__ == "__main__":
    unittest.main(defaultTest="RunPythonTests", verbosity=2)
