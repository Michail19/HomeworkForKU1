import unittest
import subprocess
import os


class TestMyProgram(unittest.TestCase):
    test_counts = {}

    @classmethod
    def setUpClass(cls):
        cls.zip_path = 'emulator.zip'

        if not os.path.exists(cls.zip_path):
            subprocess.run(['zip', '-r', cls.zip_path, 'my_program'], check=True)

    def setUp(self):
        test_name = self._testMethodName
        if test_name not in self.test_counts:
            self.test_counts[test_name] = 0

        if self.test_counts[test_name] >= 5:
            self.skipTest(f"{test_name} has already run 5 times")

        self.test_counts[test_name] += 1

    def test_zip_execution(self):
        result = subprocess.run(['python', self.zip_path], capture_output=True, text=True)

        self.assertEqual(result.returncode, 0)

        expected_output = "Expected output here"
        self.assertIn(expected_output, result.stdout)


if __name__ == '__main__':
    unittest.main()
