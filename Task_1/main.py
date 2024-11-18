import unittest
from datetime import datetime
from unittest.mock import patch, MagicMock

from Task_1.emulator import VirtualFileSystem, VirtualShell


class TestVirtualFileSystem(unittest.TestCase):
    @patch('zipfile.ZipFile')
    def test_load_zip(self, MockZipFile):
        mock_zip = MagicMock()
        mock_zip.namelist.return_value = ['file1.txt', 'dir/file2.txt']
        MockZipFile.return_value.__enter__.return_value = mock_zip

        vfs = VirtualFileSystem('VirtualDevice.zip')
        self.assertIn('file1.txt', vfs.fs)
        self.assertIn('dir', vfs.fs)
        self.assertIn('file2.txt', vfs.fs['dir'])

    def test_list_dir_root(self):
        vfs = VirtualFileSystem('VirtualDevice.zip')
        vfs.fs = {'file1.txt': None, 'file2.txt': None}
        vfs.current_dir = "/"
        result = vfs.list_dir()
        self.assertEqual(result, ['file1.txt', 'file2.txt'])

    def test_change_dir(self):
        vfs = VirtualFileSystem('VirtualDevice.zip')
        vfs.fs = {'dir1': {'file1.txt': None}, 'dir2': {'file2.txt': None}}
        vfs.current_dir = "/"
        vfs.change_dir('dir1')
        self.assertEqual(vfs.current_dir, '/dir1')

    def test_change_dir_error(self):
        vfs = VirtualFileSystem('VirtualDevice.zip')
        vfs.fs = {'dir1': {'file1.txt': None}}
        vfs.current_dir = "/"
        with self.assertRaises(FileNotFoundError):
            vfs.change_dir('nonexistent_dir')

    def test_current_path(self):
        vfs = VirtualFileSystem('VirtualDevice.zip')
        vfs.current_dir = '/dir1/subdir'
        self.assertEqual(vfs.current_path(), '/dir1/subdir')

    class TestVirtualShell(unittest.TestCase):
        @patch('builtins.print')
        def test_ls(self, mock_print):
            vfs = VirtualFileSystem('VirtualDevice.zip')
            vfs.fs = {'file1.txt': None, 'file2.txt': None}
            shell = VirtualShell(vfs)
            shell.vfs.current_dir = '/'
            shell.process_command('ls')
            mock_print.assert_called_with('file1.txt\nfile2.txt')

    @patch('builtins.print')
    def test_pwd(self, mock_print):
        vfs = VirtualFileSystem('VirtualDevice.zip')
        vfs.current_dir = '/dir1/subdir'
        shell = VirtualShell(vfs)
        shell.process_command('pwd')
        mock_print.assert_called_with('/dir1/subdir')

    def test_cd_valid(self):
        vfs = VirtualFileSystem('VirtualDevice.zip')
        vfs.fs = {'dir1': {'file1.txt': None}}
        vfs.current_dir = '/'
        shell = VirtualShell(vfs)
        shell.process_command('cd dir1')
        self.assertEqual(vfs.current_dir, '/dir1')

    @patch("builtins.print")
    def test_cd_invalid(self, mock_print):
        vfs = MagicMock()
        vfs.list_dir.return_value = []
        vfs.change_dir.side_effect = FileNotFoundError("No such directory: nonexistent_dir")

        shell = VirtualShell(vfs)
        shell.process_command("cd nonexistent_dir")

        mock_print.assert_called_with("No such directory: nonexistent_dir")

    @patch('builtins.input', return_value='exit')  # Мокаем input, чтобы сразу вернулся 'exit'
    @patch('builtins.print')  # Мокаем print, чтобы не выводить лишнее в тестах
    def test_exit(self, mock_print, mock_input):
        vfs = VirtualFileSystem('VirtualDevice.zip')
        shell = VirtualShell(vfs)

        # Проверим, что метод start завершится без ошибок, как только введем 'exit'
        # Метод должен выйти из цикла
        shell.start()

        # Здесь нет необходимости ловить исключение, достаточно проверить, что метод завершился
        mock_input.assert_called_with('/ # ')  # Проверим, что input был вызван с правильным приглашением

    @patch('builtins.print')  # Мокаем print, чтобы не выводить в консоль
    def test_date(self, mock_print):
        vfs = MagicMock()  # Мокаем виртуальную файловую систему
        shell = VirtualShell(vfs)

        # Пытаемся вызвать команду 'date'
        shell.process_command("date")

        # Получаем текущую дату и проверяем, что она выведена в нужном формате
        now = datetime.now().strftime("%a %b %d %H:%M:%S %Y")
        mock_print.assert_called_with(now)  # Проверяем, что вызов print был с этим значением

    @patch('builtins.print')
    def test_tail(self, mock_print):
        # Создаем моки для виртуальной файловой системы
        vfs = MagicMock()
        vfs.read_file.return_value = [
            "Line 1",
            "Line 2",
            "Line 3",
            "Line 4",
            "Line 5",
        ]  # Содержимое файла

        shell = VirtualShell(vfs)

        # Пытаемся вызвать команду 'tail' с аргументом на количество строк
        shell.process_command("tail test_file 3")

        # Проверяем, что выведены последние 3 строки
        mock_print.assert_any_call("Line 3")
        mock_print.assert_any_call("Line 4")
        mock_print.assert_any_call("Line 5")

    @patch("builtins.print")
    def test_tail_invalid_file(self, mock_print):
        vfs = MagicMock()
        vfs.read_file.side_effect = FileNotFoundError("No such file: test_file")

        shell = VirtualShell(vfs)
        shell.process_command("tail test_file 3")

        mock_print.assert_called_with("No such file: test_file")

    @patch('builtins.print')
    def test_tail_invalid_args(self, mock_print):
        # Создаем моки для виртуальной файловой системы
        vfs = MagicMock()
        shell = VirtualShell(vfs)

        # Пытаемся вызвать команду 'tail' с недостаточным количеством аргументов
        shell.process_command("tail")

        # Проверяем, что выводится сообщение об ошибке
        mock_print.assert_called_with("Usage: tail <file> [lines]")

    @patch('builtins.print')
    def test_tail_default_lines(self, mock_print):
        # Создаем моки для виртуальной файловой системы
        vfs = MagicMock()
        vfs.read_file.return_value = [
            "Line 1",
            "Line 2",
            "Line 3",
            "Line 4",
            "Line 5",
        ]

        shell = VirtualShell(vfs)

        # Пытаемся вызвать команду 'tail' без указания количества строк (должно быть 10 по умолчанию)
        shell.process_command("tail test_file")

        # Проверяем, что выведены последние 10 строк (в нашем случае это все 5 строк)
        mock_print.assert_any_call("Line 1")
        mock_print.assert_any_call("Line 2")
        mock_print.assert_any_call("Line 3")
        mock_print.assert_any_call("Line 4")
        mock_print.assert_any_call("Line 5")


if __name__ == "__main__":
    unittest.main()