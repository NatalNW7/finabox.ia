from os.path import join
from json import loads
from utils import PathConstants


def writer(content, output: str = PathConstants.OUTPUT_TXT):
    with open(output, 'w') as file:
        characters_written = file.write(content)
    
    return True if characters_written > 0 else False

def reader(file: str = PathConstants.OUTPUT_TXT):
    with open(file, 'r') as content:
        if '.json' in file:
            return loads(content.read())
        
        lines = content.readlines()
    
    if not writer('content was deleted'):
        raise Exception('Error to delete content')

    return lines