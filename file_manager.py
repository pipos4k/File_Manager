# backup_to_zip.py - Copies an entrire folder and its contents into
import zipfile, os, datetime
from pathlib import Path
import sys

'''
Ask user what needs.
UI:
1. Zip
2. Remove 
3. Sort
4. Check the folder

If 2.:
give path:
Ask: 
1. All files
2. Remove specific files
3. Dont remove specific files
4. Add only files with specific space
5. Modified recently

If 3.
give path: 
Ask:
1. Day
2. Size
3. Name
4. Type

If 4.
give path:
'''
h = Path.home()
destination = h / "Documents/python/Five-Projects"

def backup_to_zip(folder): 
    while True:
        choice = input("Lets back up the files you want:\n" \
        "1. All files.\n" \
        "2. Exclude specific file extensions.\n" \
        "3. Include only specific file extensions.\n" \
        "4. Include only files larger than a specific size.\n" \
        "5. Include files modified within the last day.\n" \
        "Select an option: " \
       ).strip()

        if not choice.isdigit():
            print("\n------------------------")
            print("Invalid input. Please enter a number from the list below.")
            print("------------------------")
            continue

        choice = int(choice)
        if choice < 6:
            choice = str(choice)
            break
        else:
            print("\n------------------------")
            print("Choose one number from the list below.")
            print("------------------------")

    if choice == "2" or choice == "3":
        while True:
            extension = input("Which file extension do you want to exclude? Example: '.txt'\n").strip()

            if extension.isdigit():
                print("Wrong extension.")
                continue

            if extension.startswith(".") and len(extension) > 1 and extension[1:].isalpha():
                break

    if choice == "4":
        while True:
            size =input("Enter the minimun file size in BYTES (e.g. 1MB = 1000000):\n").strip()
            if not size.isdigit():
                print("You entered a non-numeric value. Please enter a number")
                continue
            size = int(size)
            break
        
    # Back up the entire "folder" into a ZIP file.
    # With specific files to add or to not add
    folder = Path(folder) # Make sure folder is a Path object, not string.

    number = 1
    while True:
        # create the zipfile with the name of folder and the right number.
        zip_filename = Path(f"BU_{folder.parts[-1]}_{str(number)}.zip")
        if not zip_filename.exists():
            # print(f"{zip_filename} doesnt exists.")
            break
        number += 1

    # Create the ZIP file.
    # print(f"Creating {zip_filename}...")
    # backup_zip = zipfile.ZipFile(zip_filename, "w")

    # Walk the entire folder tree and compress the files in each folder.
    for folder_name, subfolders, filenames in os.walk(folder):
        folder_name = Path(folder_name)
        # print(f"Adding files from folder: {folder_name} ...")

        for filename in filenames:
            file_path = folder_name / filename
            # print(f"To filepath: {file_path}")
            arcname = file_path.relative_to(folder)

            if choice == "1": # Add all files (include subfolders if exists)
                print(f"Adding file from{file_path} as {arcname}...")
                # backup_zip.write(file_path, arcname)

            if choice == "2": # Remove specific extension files
                if arcname.suffix == extension:
                    print(f"Skip file: {filename}...")
                else:
                    print(f"Adding file from{file_path} as {arcname}...")
                    # backup_zip.write(file_path, arcname)
                
            if choice == "3": # Add specific extension files
                if arcname.suffix == extension:
                    print(f"Adding file from{file_path} as {arcname}...")
                    # backup_zip.write(file_path, arcname)
                else:
                    print(f"Skip file: {filename}...")

            if choice == "4": # Add files with size bigger than {size}
                if file_path.stat().st_size > size:
                    print(f"Adding file from{file_path} as {arcname} with size: {file_path.stat().st_size}bytes...")
                    # backup_zip.write(file_path, arcname)
                else:
                    print(f"Skip file: {filename}...")

            if choice == "5": # Add files checking their modified day (Default 1 day) 
                modified_time = file_path.stat().st_mtime
                readable_time = datetime.datetime.fromtimestamp(modified_time)
                if readable_time > datetime.datetime.now() - datetime.timedelta(days=1):                
                    print(f"Adding file from{file_path} as {arcname}...")
                    # backup_zip.write(file_path, arcname)
                else:
                    print(f"Skip file: {filename}...")
                
    # backup_zip.close()
    print("Your zip is ready. Thanks for the patient.")
        
def choice_of_function():
    choice = "1"
    # choice = input("Welcome to File MASSIVE APP\n" \
    # "-------------------------\n"
    # "1. Backup /ZIP a folder\n" \
    # "2. \n" \
    # "What you want to do:" \
    # )

    if choice == "1":
        backup_to_zip(destination / "Stands/spam")

choice_of_function()