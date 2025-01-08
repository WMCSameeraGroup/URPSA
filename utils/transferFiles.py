import os

def move_dir_to_archive(source_dir,destination_dir):
    os.rename(source_dir, destination_dir)
    print(f"Moved {source_dir} to {destination_dir}")

