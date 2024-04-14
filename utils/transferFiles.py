import os
import shutil
from datetime import datetime

def move_files_to_timestamped_folder(source_dir="inputFiles"):
    # Generate timestamp for folder name
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    # Create new folder with timestamp
    new_folder = os.path.join(os.getcwd(), "Archives", timestamp)
    os.makedirs(new_folder)

    # Get all files in the source directory
    files = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]

    # Move each file to the new folder
    for file in files:
        shutil.move(os.path.join(source_dir, file), new_folder)

    print(f"All files  moved to folder 'Archives/{timestamp}'.")

