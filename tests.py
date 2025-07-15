import unittest
import re
from functions.get_files_info import get_files_info

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






if __name__ == "__main__":
    unittest.main()

