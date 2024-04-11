from utils.file import writer, reader
from utils import PathConstants
from os.path import exists


def test_writer():
    assert writer('test_writer')

def test_reader():
    lines = reader()
    assert len(lines) > 0

def test_check_if_content_was_deleted_after_reader():
    writer('some content')
    reader()
    
    assert reader() == ['content was deleted']

def test_check_if_reader_can_read_json():
    json_content = reader(PathConstants.CATEGORIES)

    assert isinstance(json_content, dict)

def test_check_if_temp_folder_exists():
    temp_folder = PathConstants.TEMP

    assert exists(temp_folder)
