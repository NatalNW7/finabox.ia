from os import getcwd, mkdir
from os.path import join, exists


def temp_path():
    temp_path = join(getcwd(), 'temp')
    if not exists(temp_path):
        mkdir(temp_path)
    return temp_path