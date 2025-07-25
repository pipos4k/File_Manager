# file_manager.py - Copy, delete or sort your files and folders
import zipfile, os, datetime, sys, glob
from pathlib import Path
from send2trash import send2trash

# Remove files function
def remove_files(folder, choice=None, extension=None, size=None):    
    # Walk through the folder and its subfolders
    for folder_name, subfolders, filenames in os.walk(folder):
        folder_name = Path(folder_name)

        for filename in filenames:
            file_path = folder_name / filename # Full file path
            arcname = file_path.relative_to(folder) # Relative filepath for logging 

            # Option 1: Remove all files (include subfolders if exists)
            if choice == "1":
                if os.path.exists(folder_name):
                    send2trash(str(file_path))
                    print(f"Moving to trash: {file_path} (as {arcname})...")
                else:
                    print(f"File not found: {file_path}")

            # Option 2: Exclude files with specific extension
            if choice == "2":
                if arcname.suffix == extension:
                    print(f"Skip file {filename}")
                else:
                    if file_path.exists() and file_path.is_file():
                        send2trash(str(file_path))
                        print(f"Moved to trash: {file_path} (as {arcname})")
                    else:
                        print(f"File not found: {file_path}")
            
            # Option 3: Remove files with specific extension
            if choice == "3":
                if arcname.suffix == extension:
                    print(f"Moved to trash: {file_path} (as {arcname})")
                    send2trash(str(file_path))
                else:
                    print(f"Skip file: {filename}")

            # Option 4: Remove files larger than a specific size
            if choice == "4":
                if file_path.stat().st_size > size:
                    print(f"Move file to trash from {file_path} as {arcname} with size: {file_path.stat().st_size}bytes...")
                    send2trash(str(file_path))
                else:
                    print(f"Skip file: {filename}...")

            # Option 5: Remove files modified in the last day
            if choice == "5":
                modified_time = file_path.stat().st_mtime
                readable_time = datetime.datetime.fromtimestamp(modified_time)
                if readable_time > datetime.datetime.now() - datetime.timedelta(days=1):                
                    print(f"Moved file to trash from {file_path} as {arcname}...")
                    send2trash(str(file_path))
                else:
                    print(f"Skip file: {filename}...")
                pass
        
# Backup to zip function
def backup_to_zip(folder, choice=None, extension=None, size=None): 
    # Generate a unique ZIP file name(e.g. BU_foldername_1.zip)
    number = 1
    while True:
        # Create the zipfile with the name of folder and the right number.
        zip_filename = Path(f"BU_{folder.parts[-1]}_{str(number)}.zip")
        if not zip_filename.exists():
            print(f"{zip_filename} doesnt exists.")
            break
        number += 1

    # Create the ZIP file.
    print(f"Creating {zip_filename}...")
    backup_zip = zipfile.ZipFile(zip_filename, "w")

    # Walk through the folder and its subfolders
    for folder_name, subfolders, filenames in os.walk(folder):
        folder_name = Path(folder_name)
        print(f"Starting folder: {folder_name} ...")

        for filename in filenames:
            file_path = folder_name / filename # Absolute path to file
            arcname = file_path.relative_to(folder) # Pathe to store in ZIP 

            # Option 1: Add all files (include subfolders if exists)
            if choice == "1": 
                print(f"Adding file from {file_path} as {arcname}...")
                backup_zip.write(file_path, arcname)

            # Option 2: Exclude files with specific extension
            if choice == "2": 
                if arcname.suffix == extension:
                    print(f"Skip file: {filename}...")
                else:
                    print(f"Adding file from {file_path} as {arcname}...")
                    backup_zip.write(file_path, arcname)

            # Option 3 : Include only files with specific extension
            if choice == "3": 
                if arcname.suffix == extension:
                    print(f"Adding file from {file_path} as {arcname}...")
                    backup_zip.write(file_path, arcname)
                else:
                    print(f"Skip file: {filename}...")

            # Option 4: Add files larger than a specific size
            if choice == "4": 
                if file_path.stat().st_size > size:
                    print(f"Adding file from {file_path} as {arcname} with size: {file_path.stat().st_size}bytes...")
                    backup_zip.write(file_path, arcname)
                else:
                    print(f"Skip file: {filename}...")

            # Add files modified in the last day
            if choice == "5":  
                modified_time = file_path.stat().st_mtime
                readable_time = datetime.datetime.fromtimestamp(modified_time)
                if readable_time > datetime.datetime.now() - datetime.timedelta(days=1):                
                    print(f"Adding file from {file_path} as {arcname}...")
                    backup_zip.write(file_path, arcname)
                else:
                    print(f"Skip file: {filename}...")
                
    backup_zip.close()
    print("Your ZIP file is ready. Thank you for your patience.")

# Sort files function
def sort_files(folder):
    # Change to the target folder
    os.chdir(folder)
    # Get list of files and ignore directories
    file_list = [f for f in os.listdir(".") if os.path.isfile(f)]

    while True:
        choice = input("\nChoose how you want to sort the files:\n" \
        "1. Based on size\n" \
        "2. Based on date\n").strip()

        # Validate the choice is a digit
        if not choice.isdigit():
            print("\n---------------------------------------------------")
            print("Invalid input. Please enter a number from the list.")
            print("----------------------------------------------------")
            continue

        # Validate the choice is between 1 and 5
        if choice in ("1", "2"):
            break
        else:
            print("\n-------------------------------------")
            print("PLEASE ENTER A NUMBER FROM THE LIST!")
            print("-------------------------------------")

    # Sort files based on choice
    if choice == "1":
        sorted_files = sorted(file_list, key=os.path.getsize)
    else:
        sorted_files = sorted(file_list, key=os.path.getmtime)

    # Print results
    print("\nSorted files:")
    for i, f in enumerate(sorted_files, start=1):
        size = os.path.getsize(f)
        date = os.path.getctime(f)
        date_str = datetime.datetime.fromtimestamp(date).strftime("Date: %d-%m-%Y | Time: %H:%M:%S |")

        if choice == "1":
            print(f"{i}. {f} - {size} bytes")
            pass
        else:
            print(f"{i}. {f} - {date_str}")

# File filtering function.
def choice_extension():
    while True:
        # User choose the filtering method
        choice = input("\n\nChoose the type of files to include in the operation:\n" \
           "1. All files.\n" \
           "2. Exclude specific file extensions.\n" \
           "3. Include only specific file extensions.\n" \
           "4. Include only files larger than a specific size.\n" \
           "5. Include files modified within the last day.\n" \
           "Select an option: " \
          ).strip()
        
        # Validate the choice is a digit
        if not choice.isdigit():
            print("\n---------------------------------------------------")
            print("Invalid input. Please enter a number from the list.")
            print("----------------------------------------------------")
            continue

        choice = int(choice)

        # Validate the choice is between 1 and 5
        if 0 < choice < 6:
            choice = str(choice)
            break
        else:
            print("\n-------------------------------------")
            print("PLEASE ENTER A NUMBER FROM THE LIST!")
            print("-------------------------------------")

    # Just return choice as str
    if choice in ("1", "5"):
        return str(choice), None
    
    # Filtering the exclude/include extension 
    if choice in ("2", "3"):
        while True:
            extension = input("Which file extension do you want to filter? Example: '.txt'\n").strip()
            # Ensure for valid format
            if extension.startswith(".") and len(extension) > 1 and extension[1:].isalpha():
                return str(choice), extension
            else:
                print("Invalid extension format. Try again.")

    # Filtering the size method
    if choice == "4":
        while True:
            size =input("Enter the minimun file size in **bytes** (e.g. 1MB = 1000000):\n").strip()
            if size.isdigit():
                return str(choice), int(size)
            else:
                print("Invalid size. Please enter a numeric value.")

# Choose the operation function
def choice_of_function():
    print("Welcome to File Manager APP!🛠️\n" \
          "---------------------------")
    while True:
        # User choose the operation
        operation = input(
        "1. Backup / ZIP\n" \
        "2. Remove files\n" \
        "3. Sort files\n" \
        "Selece an option: " \
        ).strip()

        # Validate the choice is from list
        if operation not in ("1", "2", "3"):
            print("\n\nInvalid choice, Please select something from the list.\n")
            continue
        break

    # destination = get_valid_folder_path()
    destination = Path.home() / "Documents/python/Five-Projects/Stands/spam/test"

    # For 1 and 2 operations get additional values
    if operation in ("1", "2"):
        choice, value = choice_extension()
        if operation == "1":
            # You’ll need to define 'destination' or pass it into this function
            backup_to_zip(folder=destination, extension=value, size=value, choice=choice)
        else:
            remove_files(folder=destination, extension=value, size=value, choice=choice)

    elif operation == "3":
        sort_files(destination)

# Check if path is valid
def get_valid_folder_path():
    while True:
        # Make sure folder is a Path object, not string.
        user_input = input("Enter the full path to the folder (e.g. /home/user/Documents):\n").strip()
        # Handles ~, resolves symlinks and relatives paths, and returns an absolute Path
        path = Path(user_input).expanduser().resolve()  

        print(f"🔍 Checking path: {path}")
        if path.is_dir():
            print(f"Valid folder: {path}")
            return path
        else:
            print("Invalid folder path. Please try again.")

choice_of_function()
