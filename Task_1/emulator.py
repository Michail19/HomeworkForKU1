import os
import zipfile
from datetime import datetime


# Простая виртуальная файловая система
class VirtualFileSystem:
    def __init__(self, zip_file_path):
        self.zip_file_path = zip_file_path
        self.current_dir = "/"
        self.fs = {}  # Виртуальная файловая система в памяти
        self.files_content = {}  # Содержимое файлов
        self.load_zip()

    def load_zip(self):
        """Загружает файловую систему из zip-архива."""
        with zipfile.ZipFile(self.zip_file_path, 'r') as z:
            for file in z.namelist():
                parts = file.split('/')
                d = self.fs
                for part in parts[:-1]:
                    d = d.setdefault(part, {})
                if parts[-1]:
                    d[parts[-1]] = None  # Файлы как None
                    # Загрузим содержимое файла
                    self.files_content[file] = z.read(file).decode('utf-8')

    def list_dir(self):
        """Возвращает содержимое текущего каталога."""
        dirs = self.fs
        for part in self.current_dir.strip("/").split("/"):
            if part:
                dirs = dirs[part]
        return list(dirs.keys())

    def change_dir(self, path):
        """Сменить каталог."""
        if path == "..":
            self.current_dir = "/".join(self.current_dir.split("/")[:-1])
            if not self.current_dir:
                self.current_dir = "/"
        elif path in self.list_dir():
            self.current_dir += f"/{path}".strip("/")
        else:
            raise FileNotFoundError(f"No such directory: {path}")

    def current_path(self):
        """Возвращает текущий путь."""
        return self.current_dir

    def read_file(self, file_path):
        """Читает содержимое файла."""
        full_path = f"{self.current_dir.strip('/')}/{file_path}".strip("/")
        if full_path in self.files_content:
            return self.files_content[full_path].splitlines()
        raise FileNotFoundError(f"No such file: {file_path}")


# Командная оболочка
class VirtualShell:
    def __init__(self, vfs):
        self.vfs = vfs

    def start(self):
        while True:
            command = input(f"{self.vfs.current_path()} # ")
            if command.strip() == "exit":
                break
            self.process_command(command)

    def process_command(self, command):
        parts = command.split()
        if not parts:
            return
        cmd = parts[0]

        try:
            if cmd == "ls":
                print("\n".join(self.vfs.list_dir()))
            elif cmd == "pwd":
                print(self.vfs.current_path())
            elif cmd == "cd":
                if len(parts) > 1:
                    self.vfs.change_dir(parts[1])
                else:
                    print("Usage: cd <directory>")
            elif cmd == "tail":
                self.handle_tail(parts)
            elif cmd == "date":
                self.handle_date()
            else:
                print(f"Command not found: {cmd}")
        except Exception as e:
            print(f"Error: {e}")

    def handle_tail(self, parts):
        """Обрабатывает команду tail."""
        if len(parts) < 2:
            print("Usage: tail <file> [lines]")
            return

        file_name = parts[1]
        lines = int(parts[2]) if len(parts) > 2 else 10

        try:
            file_content = self.vfs.read_file(file_name)
            for line in file_content[-lines:]:
                print(line)
        except FileNotFoundError as e:
            print(e)

    def handle_date(self):
        """Обрабатывает команду date."""
        now = datetime.now()
        print(now.strftime("%a %b %d %H:%M:%S %Y"))


if __name__ == "__main__":
    vfs = VirtualFileSystem("VirtualDevice.zip")
    shell = VirtualShell(vfs)
    shell.start()
