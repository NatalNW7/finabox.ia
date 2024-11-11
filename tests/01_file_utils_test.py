from os.path import exists

from pytest import mark

from utils import PathConstants
from utils.file import reader, writer


@mark.parametrize(
    'file,content',
    [
        (PathConstants.OUTPUT_TXT, 'test_writer'),
        (
            PathConstants.OUTPUT_CSV,
            ['line 1;line 1\n', 'line 2;line 2\n', 'line 3;line 3\n'],
        ),
        (
            PathConstants.OUTPUT_JSON,
            {'line 1': 'line 1', 'line 2': 'line 2', 'line 3': 'line 3'},
        ),
        (
            PathConstants.OUTPUT_JSON,
            [{'line 1': 'line 1'}, {'line 2': 'line 2'}, {'line 3': 'line 3'}],
        ),
    ],
)
def test_writer(file, content):
    writer(content, file)
    file_content_is_not_empty = reader(file, delete_after_read=False)

    assert file_content_is_not_empty


def test_reader():
    lines = reader(PathConstants.OUTPUT_TXT)
    assert len(lines) > 0


def test_check_if_content_was_deleted_after_reader():
    writer('some content', PathConstants.OUTPUT_TXT)
    reader(PathConstants.OUTPUT_TXT)

    assert reader(PathConstants.OUTPUT_TXT) == ['content was deleted']


def test_check_if_reader_can_read_json():
    json_content = reader(PathConstants.CATEGORIES)

    assert isinstance(json_content, dict)


def test_check_if_temp_folder_exists():
    temp_folder = PathConstants.TEMP

    assert exists(temp_folder)
