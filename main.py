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

    def tearDown(self):
        os.remove(self.test_zip.name)

    def test_ls_command(self):
        # Проверяем содержимое корневой директории
        output = self.vfs.list_dir()
        self.assertIn('file1.txt', output)
        self.assertIn('subdir', output)

    def test_pwd_command(self):
        # Проверяем начальную директорию
        output = self.vfs.current_path()
        self.assertEqual(output, '/')

    def test_cd_command(self):
        # Переходим в подкаталог и проверяем текущий путь
        self.vfs.change_dir('subdir')
        output = self.vfs.current_path()
        self.assertEqual(output, '/subdir')

    def test_read_file(self):
        # Читаем содержимое файла
        content = self.vfs.read_file('file1.txt')
        self.assertEqual(content, ['Line1', 'Line2', 'Line3', 'Line4', 'Line5'])

    def test_tail_command(self):
        # Используем команду tail и проверяем вывод
        self.shell.process_command('tail file1.txt 3')
        # Здесь нужно перехватить вывод через `unittest.mock` или настроить shell так, чтобы возвращал результат

    def test_date_command(self):
        # Проверяем вывод команды date
        self.shell.process_command('date')
        # Аналогично, для проверки нужно перехватить
