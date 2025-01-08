import os

def move_dir_to_archive(source_dir,destination_dir):
    try:
        os.rename(source_dir, destination_dir)
        print(f"Moved {source_dir} to {destination_dir}")
    except FileNotFoundError:
        print("The source directory does not exist.")
    except PermissionError:
        print("Permission denied.")
    except Exception as e:
        print(f"Error: {e}")



def delete_dir(source_dir,destination_dir):
    try:
        os.rmdir(source_dir)
        print(f"Removed {source_dir}")

    except FileNotFoundError:
        print("The source directory does not exist.")

    except PermissionError:
        print("Permission denied.")
    except Exception as e:
        print(f"Error: {e}")

