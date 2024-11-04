import os
import tempfile
import unittest
import shutil
from Task_1.emulator import process_command, tail

class TestConsole(unittest.TestCase):
    def setUp(self):
        self.project_root = os.path.abspath(os.path.dirname(__file__))

        self.test_dir = os.path.join(self.project_root, "test_temp_dir")
        os.makedirs(self.test_dir, exist_ok=True)

        self.subdir1 = os.path.join(self.test_dir, "subdir1")
        self.subdir2 = os.path.join(self.test_dir, "subdir2")
        os.makedirs(self.subdir1, exist_ok=True)
        os.makedirs(self.subdir2, exist_ok=True)

    def tearDown(self):
        try:
            self.test_dir.cleanup()
            shutil.rmtree(self.test_dir)
        except Exception as e:
            print(f"Ошибка при очистке: {e}")

# Тесты для команды ls
    def test_ls_command_single_file(self):
        with open("file1.txt", "w") as f:
            f.write("Content")
        output = process_command("ls")
        self.assertIn("file1.txt", output)

    def test_ls_command_multiple_files(self):
        with open("file1.txt", "w") as f1, open("file2.txt", "w") as f2:
            f1.write("Content")
            f2.write("Content")
        output = process_command("ls")
        self.assertIn("file1.txt", output)
        self.assertIn("file2.txt", output)

    def test_ls_command_empty_directory(self):
        output = process_command("ls")
        self.assertEqual(len(output), 0)

    def test_ls_command_hidden_file(self):
        with open(".hiddenfile", "w") as f:
            f.write("Content")
        output = process_command("ls")
        self.assertIn(".hiddenfile", output)

    def test_ls_command_long_format(self):
        with open("file1.txt", "w") as f:
            f.write("Content")
        output = process_command("ls -l")
        self.assertIn("file1.txt", output)

    # Тесты для команды pwd
    def test_pwd_command_initial_directory(self):
        output = process_command("pwd")
        self.assertIn(self.test_dir.name, output[0])

    def test_pwd_command_after_cd(self):
        subdir = os.path.join(self.test_dir.name, "subdir")
        os.mkdir(subdir)
        process_command(f"cd {subdir}")
        output = process_command("pwd")
        self.assertIn(subdir, output[0])

    def test_pwd_command_after_nested_cd(self):
        subdir1 = os.path.join(self.test_dir.name, "subdir1")
        subdir2 = os.path.join(subdir1, "subdir2")
        os.makedirs(subdir2)
        process_command(f"cd {subdir1}")
        process_command(f"cd subdir2")
        output = process_command("pwd")
        self.assertIn(subdir2, output[0])

    def test_pwd_command_root_directory(self):
        process_command("cd /")
        output = process_command("pwd")
        self.assertEqual(output[0], "/")

    def test_pwd_command_after_invalid_cd(self):
        process_command("cd nonexistent_directory")
        output = process_command("pwd")
        self.assertIn(self.test_dir.name, output[0])

    # Тесты для команды cd
    def test_cd_to_existing_directory(self):
        subdir = os.path.join(self.test_dir.name, "subdir")
        os.mkdir(subdir)
        process_command(f"cd {subdir}")
        output = process_command("pwd")
        self.assertIn(subdir, output[0])

    def test_cd_to_nonexistent_directory(self):
        output = process_command("cd nonexistent_directory")
        self.assertIn("No such directory", output[0])

    def test_cd_without_argument(self):
        output = process_command("cd")
        self.assertIn("Usage: cd <directory>", output[0])

    def test_cd_back_to_parent_directory(self):
        subdir = os.path.join(self.test_dir.name, "subdir")
        os.mkdir(subdir)
        process_command(f"cd {subdir}")
        process_command("cd ..")
        output = process_command("pwd")
        self.assertIn(self.test_dir.name, output[0])

    def test_cd_to_root(self):
        process_command("cd /")
        output = process_command("pwd")
        self.assertEqual(output[0], "/")

    # Тесты для команды date
    def test_date_command_output_format(self):
        output = process_command("date")
        self.assertTrue(any("202" in line for line in output))

    def test_date_command_multiple_calls(self):
        first_output = process_command("date")
        first_date = first_output[0]
        second_output = process_command("date")
        second_date = second_output[0]
        self.assertEqual(first_date, second_date)

    def test_date_command_with_timezone(self):
        os.environ["TZ"] = "UTC"
        output = process_command("date")
        self.assertTrue("UTC" in output[0])

    def test_date_command_invalid_timezone(self):
        os.environ["TZ"] = "INVALID"
        output = process_command("date")
        self.assertTrue("INVALID" not in output[0])

    def test_date_command_after_timezone_change(self):
        os.environ["TZ"] = "America/New_York"
        output = process_command("date")
        self.assertTrue("New York" in output[0])

    # Тесты для команды tail
    def test_tail_command_last_5_lines(self):
        output = tail(self.test_file, 5)
        self.assertEqual([line.decode('utf-8').strip() for line in output], ["Line6", "Line7", "Line8", "Line9", "Line10"])

    def test_tail_command_all_lines(self):
        output = tail(self.test_file, 10)
        self.assertEqual([line.decode('utf-8').strip() for line in output],
                         ["Line1", "Line2", "Line3", "Line4", "Line5", "Line6", "Line7", "Line8", "Line9", "Line10"])

    def test_tail_command_more_than_file_lines(self):
        output = tail(self.test_file, 15)
        self.assertEqual(len(output), 10)

    def test_tail_command_invalid_file(self):
        output = process_command("tail nonexistent_file")
        self.assertIn("No such file", output[0])

    def test_tail_command_default_10_lines(self):
        output = tail(self.test_file)
        self.assertEqual(len(output), 10)

    # Тесты для некорректной команды
    def test_invalid_command(self):
        output = process_command("invalid_command")
        self.assertIn("Command not found", output[0])

    def test_empty_command(self):
        output = process_command("")
        self.assertEqual(output, [])

    def test_partial_command(self):
        output = process_command("pw")
        self.assertIn("Command not found", output[0])

    def test_whitespace_command(self):
        output = process_command("   ")
        self.assertEqual(output, [])

    def test_similar_command(self):
        output = process_command("lsd")
        self.assertIn("Command not found", output[0])

if __name__ == "__main__":
    unittest.main()
