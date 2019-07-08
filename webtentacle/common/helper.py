from os import path

def file_exist(filepath):
    return True if path.exists(filepath) else False