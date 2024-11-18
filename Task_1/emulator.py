import os
import zipfile


# Простая виртуальная файловая система
class VirtualFileSystem:
    def __init__(self, zip_file_path):
        self.zip_file_path = zip_file_path
        self.current_dir = "/"
        self.fs = {}  # Виртуальная файловая система в памяти
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
            else:
                print(f"Command not found: {cmd}")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    vfs = VirtualFileSystem("VirtualDevice.zip")
    shell = VirtualShell(vfs)
    shell.start()
