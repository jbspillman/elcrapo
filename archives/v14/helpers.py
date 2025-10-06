import shutil
import os


def remove_folder_path(the__path):
    if os.path.exists(the__path):
        try:
            shutil.rmtree(the__path)
            return True
        except OSError as e:
            print(f"Error deleting directory {the__path}: {e}")
            return False
    return True


def check_if_folder_empty(the__path):
    if os.path.exists(the__path):
        file_objects = os.listdir(the__path)
        if len(file_objects) == 0:
            remove_result = remove_folder_path(the__path)
            return remove_result
        else:
            return False
    else:
        return True