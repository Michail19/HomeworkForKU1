import os
import zipfile
import argparse


def zip_directory(directory, zip_name):
    """Packs the contents of a directory into a zip file."""
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Walk the directory tree and add files to the zip file
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file == "emulator.py" or file == "__main__.py":
                    file_path = os.path.join(root, file)
                    # Add the file to the zip, maintaining the relative path inside the zip
                    arcname = os.path.relpath(file_path, start=directory)
                    zipf.write(file_path, arcname)
    print(f'Directory {directory} has been packed into {zip_name}')


def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Zip-Packer: Pack a directory into a zip file.")
    parser.add_argument('directory', type=str, help='Directory to pack into a zip file')
    parser.add_argument('zipfile', type=str, help='Name of the output zip file')

    # Parse the command line arguments
    args = parser.parse_args()

    # Check if the provided directory exists
    if not os.path.isdir(args.directory):
        print(f"Error: Directory {args.directory} does not exist.")
        return

    # Call the function to zip the directory
    zip_directory(args.directory, args.zipfile)


if __name__ == "__main__":
    main()


# Example: python packerZIP.py D:\Python\HomeworkForKU1\Task_1 emulator.zip
