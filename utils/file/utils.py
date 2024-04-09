from utils import temp_path
from os.path import join
from os import remove


OUTPUT = join(temp_path(), "output.txt")

def writer(content, output: str = OUTPUT):
    with open(output, 'w') as file:
        characters_written = file.write(content)
    
    return True if characters_written > 0 else False

def reader(file: str = OUTPUT):
    with open(file, 'r') as content:
        lines = content.readlines()
    
    if not writer('content was deleted'):
        raise Exception('Error to delete content')

    return lines