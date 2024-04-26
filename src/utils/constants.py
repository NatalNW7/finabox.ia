from os import path, getcwd
from enum import StrEnum


class PathConstants(StrEnum):
    BASE_PATH = getcwd()
    TEMP = path.join(BASE_PATH, 'temp')
    OUTPUT_TXT = path.join(TEMP, 'output.txt')    
    OUTPUT_CSV = path.join(TEMP, 'output.csv')    
    OUTPUT_JSON = path.join(TEMP, 'output.json')    
    RESOURCES = path.join(BASE_PATH, 'resources')
    CATEGORIES = path.join(RESOURCES, 'categories.json')
    ESTABLISHMENTS = path.join(RESOURCES, 'establishments.json')
