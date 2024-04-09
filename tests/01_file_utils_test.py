from utils.file import writer, reader


def test_writer():
    assert writer('test_writer')

def test_reader():
    lines = reader()
    assert len(lines) > 0

def test_check_if_content_was_deleted_after_reader():
    writer('some content')
    reader()
    
    assert reader() == ['content was deleted']
