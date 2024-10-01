#!/usr/bin/env python
import os


def startConsole():
    while True:
        current_dir = os.getcwd()
        command = input(f'{current_dir} # ')

        if command.strip() == 'exit':
            break

        process_command(command)


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
    else:
        print(f"Command not found: {cmd}")


if __name__ == "__main__":
    startConsole()
