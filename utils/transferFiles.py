import os

def move_dir_to_archive(pathway_dir):

    try:
        os.rename(pathway_dir, "Archive/"+pathway_dir)
        print(f"Moved {pathway_dir} to {"Archive/"+pathway_dir}")
    except FileNotFoundError:
        print("The source directory does not exist.")
    except PermissionError:
        print("Permission denied.")
    except Exception as e:
        print(f"Error: {e}")



def delete_dir(source_dir):
    try:
        os.rmdir(source_dir)
        print(f"Removed {source_dir}")

    except FileNotFoundError:
        print("The source directory does not exist.")

    except PermissionError:
        print("Permission denied.")
    except Exception as e:
        print(f"Error: {e}")

