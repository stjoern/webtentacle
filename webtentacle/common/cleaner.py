import os
import glob
import logging

logger = logging.getLogger('common')

def delete_files_top_down(directory, *args):
    try:
        extensions = tuple(args)
        dot_extensions = tuple(map(lambda x: '.{}'.format(x), extensions))
        for root, dirs, files in os.walk(directory):
            for currentFile in files:
                print("processing file: {}".format(currentFile))
                if currentFile.lower().endswith(dot_extensions):
                    os.remove(os.path.join(root, currentFile))
    except Exception as exc:
        raise