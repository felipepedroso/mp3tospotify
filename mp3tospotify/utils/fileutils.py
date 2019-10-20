import shutil
from os.path import isfile, join, exists
from os import listdir, mkdir

def ensure_folder_existence(folder_path):
    if not exists(folder_path):
        mkdir(folder_path)

def move_file(file_path, destination_path):
    shutil.move(file_path, destination_path)
    