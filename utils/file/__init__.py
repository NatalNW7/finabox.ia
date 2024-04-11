from json import loads
from utils import PathConstants


def writer(content, file: str = PathConstants.OUTPUT_TXT):
    with open(file, 'w') as file:
        characters_written = file.write(content)
    
    return True if characters_written > 0 else False

def reader(file: str = PathConstants.OUTPUT_TXT):
    with open(file, 'r') as content:
        if '.json' in file:
            return loads(content.read())
        
        lines = content.readlines()
    
    deleter()
    
    return lines

def deleter(file: str = PathConstants.OUTPUT_TXT):
    if not writer('content was deleted', file=file):
        raise Exception('Error to delete content')
    
    return True