from json import loads, dumps


def writer(content, file_path: str):
    with open(file_path, 'w') as file:
        if '.json' in file_path:
            file.writelines(dumps(content))
        elif isinstance(content, list):
            file.writelines(content)
        else:
            file.write(content)

def reader(file: str, delete_after_read: bool = True) -> (dict | list[str]):
    with open(file, 'r') as content:
        if '.json' in file:
            return loads(content.read())
        
        lines = content.readlines()
    
    if delete_after_read:
        deleter(file)
    
    return lines

def deleter(file: str):
    writer('content was deleted', file_path=file)