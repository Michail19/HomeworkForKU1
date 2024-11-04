#!/usr/bin/env python
import os


def startConsole():
    while True:
        current_dir = os.getcwd()
        command = input(f'{current_dir} # ')

        if command.strip() == 'exit':
            break

        process_command(command)


def tail(file_path, lines=10):
    with open(file_path, 'rb') as f:
        f.seek(0, 2)
        file_size = f.tell()

        block_size = 1024

        if (file_size - block_size) < 0:
            f.seek(0)
        else:
            f.seek(-1 * block_size, 2)
        data = f.readlines()

        if len(data) < lines:
            lines = len(data)

        return data[-lines:]


def process_command(command):
    command_parts = command.split()

    if len(command_parts) == 0:
        return

    cmd = command_parts[0]

    if cmd == "ls":
        command_parts.append(" ")
        if command_parts[1] == "-1" or command_parts[1] == "-l":
            print("\n".join(os.listdir(".")))
        else:
            print(" ".join(os.listdir(".")))
    elif cmd == "pwd":
        print(os.getcwd())
    elif cmd == "cd":
        if len(command_parts) > 1:
            try:
                os.chdir(command_parts[1])
            except FileNotFoundError:
                print(f"No such directory: {command_parts[1]}")
        else:
            print("Usage: cd <directory>")
    elif cmd == "date":
        system_type = os.name
        if system_type == "posix":
            os.system('date')
        elif system_type == "nt":
            os.system("powershell -Command \"[cultureinfo]::CurrentCulture = 'en-US'; "
                      "Get-Date -Format 'dddd MMMM dd HH:mm:ss K yyyy'\"")
    elif cmd == "tail":
        if len(command_parts) > 1:
            try:
                system_type = os.name
                if system_type == "posix":
                    os.system('tail')
                elif system_type == "nt":
                    command_parts.append("None")
                    if command_parts[2] != "None":
                        last_lines = tail(command_parts[1], int(command_parts[2]))
                    else:
                        last_lines = tail(command_parts[1])

                    for line in last_lines:
                        print(line.decode('utf-8').strip())
            except FileNotFoundError:
                print(f"No such file: {command_parts[1]}")
        else:
            print("Usage: tail <file>")
    else:
        print(f"Command not found: {cmd}")


if __name__ == "__main__":
    startConsole()
