from os import path

def file_exist(filepath):
    return True if path.exists(filepath) else False

def get_nested(data, *args):
    if args and data:
        item = args[0]
        if item:
            value = data.get(item)
            return value if len(args) == 1 else get_nested(value, *args[1:])