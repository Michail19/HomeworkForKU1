import unittest
import os
import tempfile
import zipfile

from Task_1.emulator import VirtualShell, VirtualFileSystem


class TestVirtualShell(unittest.TestCase):
    def setUp(self):
        # Создаём временный zip-файл с тестовыми данными
        self.test_zip = tempfile.NamedTemporaryFile(delete=False)
        with zipfile.ZipFile(self.test_zip.name, 'w') as z:
            z.writestr('file1.txt', 'Line1\nLine2\nLine3\nLine4\nLine5\n')
            z.writestr('subdir/file2.txt', 'Content of file2')
        self.test_zip.close()

        # Инициализируем виртуальную файловую систему и оболочку
        self.vfs = VirtualFileSystem(self.test_zip.name)
        self.shell = VirtualShell(self.vfs)

    def capture_command_output(self, command):
        output = self.shell.process_command(command)  # Получаем строку из process_command
        return output.splitlines()  # Разделяем на строки

    def tearDown(self):
        os.remove(self.test_zip.name)

    def test_ls_empty_directory(self):
        # Проверяем вывод для пустого каталога
        self.vfs.fs = {"empty_dir": {}}
        self.shell.process_command("cd empty_dir")
        output = self.shell.process_command("ls")
        self.assertEqual(output, "")

    def test_ls_root_directory(self):
        # Проверяем вывод для корневого каталога
        with open("file2.txt", "w") as f2:
            f2.write("Content")
        output = self.shell.process_command("ls")
        self.assertIn("file2.txt", output)

    def test_ls_with_nested_directories(self):
        # Проверяем, что выводится корректный список для вложенных каталогов
        self.vfs.fs["subdir"] = {"nested_file.txt": None}
        self.shell.process_command("cd subdir")
        output = self.capture_command_output("ls")
        self.assertIn("nested_file.txt", output)

    def test_ls_after_cd(self):
        # Проверяем вывод после смены директории
        self.vfs.fs["subdir"] = {"file_in_subdir.txt": None}
        self.shell.process_command("cd subdir")
        output = self.capture_command_output("ls")
        self.assertEqual(output, ["file_in_subdir.txt"])

    def test_ls_invalid_directory(self):
        # Проверяем, что ошибка выбрасывается при попытке `ls` в несуществующей директории
        self.shell.process_command("cd ..")
        with self.assertRaises(KeyError):
            self.shell.process_command("ls nonexistent_directory")

    def test_pwd_initial_directory(self):
        # Проверяем начальный каталог
        output = self.capture_command_output("pwd")
        self.assertEqual(output, ["/"])

    def test_pwd_after_cd(self):
        # Проверяем каталог после перехода в другую директорию
        self.vfs.fs["subdir"] = {}
        self.shell.process_command("cd subdir")
        output = self.capture_command_output("pwd")
        self.assertEqual(output, ["/subdir"])

    def test_pwd_after_nested_cd(self):
        # Проверяем после нескольких переходов в подкаталоги
        self.vfs.fs["dir1"] = {"dir2": {}}
        self.shell.process_command("cd dir1")
        self.shell.process_command("cd dir2")
        output = self.capture_command_output("pwd")
        self.assertEqual(output, ["/dir1/dir2"])

    def test_pwd_after_cd_to_root(self):
        # Проверяем возврат в корень
        self.vfs.fs["subdir"] = {}
        self.shell.process_command("cd subdir")
        self.shell.process_command("cd ..")
        output = self.capture_command_output("pwd")
        self.assertEqual(output, ["/"])

    def test_pwd_after_invalid_cd(self):
        # Проверяем, что каталог не меняется после неудачной попытки `cd`
        with self.assertRaises(FileNotFoundError):
            self.shell.process_command("cd nonexistent_dir")
        output = self.capture_command_output("pwd")
        self.assertEqual(output, ["/"])

    def test_cd_to_existing_directory(self):
        # Проверяем переход в существующую директорию
        self.vfs.fs["subdir"] = {}
        self.shell.process_command("cd subdir")
        output = self.capture_command_output("pwd")
        self.assertEqual(output, ["/subdir"])

    def test_cd_to_root(self):
        # Проверяем возврат в корневую директорию
        self.shell.process_command("cd ..")
        output = self.capture_command_output("pwd")
        self.assertEqual(output, ["/"])

    def test_cd_invalid_directory(self):
        # Проверяем ошибку при переходе в несуществующую директорию
        with self.assertRaises(FileNotFoundError):
            self.shell.process_command("cd nonexistent_dir")

    def test_cd_up_from_root(self):
        # Проверяем, что нельзя выйти за пределы корневого каталога
        self.shell.process_command("cd ..")
        output = self.capture_command_output("pwd")
        self.assertEqual(output, ["/"])

    def test_cd_nested_directories(self):
        # Создание структуры каталогов для теста
        self.vfs.fs = {
            'level1': {
                'level2': {}
            }
        }

        # Переход в каталог /level1/level2
        self.vfs.change_dir('level1')
        self.vfs.change_dir('level2')

        output = self.vfs.current_path()  # Получаем текущий путь
        self.assertEqual(output, '/level1/level2')  # Ожидаем путь /level1/level2

    def test_read_file(self):
        # Читаем содержимое файла
        content = self.vfs.read_file('file1.txt')
        self.assertEqual(content, ['Line1', 'Line2', 'Line3', 'Line4', 'Line5'])

    def test_tail_default_10_lines(self):
        # Проверяем вывод последних 10 строк
        output = self.capture_command_output(f"tail file1.txt")
        self.assertEqual(output, ['Line1', 'Line2', 'Line3', 'Line4', 'Line5'])

    def test_tail_specific_number_of_lines(self):
        # Проверяем вывод конкретного числа строк
        output = self.capture_command_output(f"tail file1.txt 1")
        self.assertEqual(output, ['Line5'])

    def test_tail_more_than_total_lines(self):
        # Проверяем вывод, если запрошено больше строк, чем есть в файле
        output = self.capture_command_output(f"tail file1.txt 20")
        self.assertEqual(output, ['Line1', 'Line2', 'Line3', 'Line4', 'Line5'])

    def test_tail_invalid_file(self):
        # Проверяем, что выдается ошибка для несуществующего файла
        output = self.capture_command_output("tail nonexistent_file.txt")
        self.assertIn("No such file", output[0])

    def test_tail_zero_lines(self):
        # Проверяем, что ничего не выводится при запросе 0 строк
        output = self.capture_command_output(f"tail file1.txt 0")
        self.assertEqual(output, [])

    def test_date_command_output_format(self):
        # Проверяем, что дата выводится в правильном формате
        output = self.capture_command_output("date")
        self.assertTrue(any("202" in line for line in output))

    def test_date_command_is_consistent(self):
        # Проверяем, что вызовы команды возвращают одинаковую дату, если они близки по времени
        first_date = self.capture_command_output("date")[0]
        second_date = self.capture_command_output("date")[0]
        self.assertEqual(first_date, second_date)

    def test_date_command_different_after_delay(self):
        # Проверяем, что дата изменяется с течением времени
        first_date = self.capture_command_output("date")[0]
        import time
        time.sleep(1)  # Задержка в 1 секунду
        second_date = self.capture_command_output("date")[0]
        self.assertNotEqual(first_date, second_date)

    def test_date_command_with_extra_arguments(self):
        # Проверяем, что дополнительные аргументы игнорируются
        output = self.capture_command_output("date extra_argument")
        self.assertTrue(any("202" in line for line in output))

    def test_date_command_no_crash(self):
        # Проверяем, что команда не вызывает исключений
        try:
            self.shell.process_command("date")
        except Exception as e:
            self.fail(f"Date command raised an exception: {e}")

    def test_invalid_command(self):
        output = self.capture_command_output("invalid_command")
        self.assertIn("Command not found", output[0])

