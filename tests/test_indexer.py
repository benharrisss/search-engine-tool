import json

from indexer import build_index, process_text, update_index, save_index, load_index


def test_process_text_basic():
    text = "Hello, World! This is a test."
    expected = ["hello", "world", "this", "is", "a", "test"]
    assert process_text(text) == expected


def test_process_text_punctuation():
    text = "Hello!!! Are you there???"
    expected = ["hello", "are", "you", "there"]
    assert process_text(text) == expected


def test_process_text_no_words():
    text = "!!! ???"
    expected = []
    assert process_text(text) == expected


def test_process_text_empty():
    text = ""
    expected = []
    assert process_text(text) == expected


def test_build_index_single_page():
    pages = [{"page": 1, "text": "Hello world"}]
    expected_index = {
        "hello": {1: {"frequency": 1, "positions": [0]}},
        "world": {1: {"frequency": 1, "positions": [1]}}
    }
    assert build_index(pages) == expected_index


def test_build_index_multiple_pages():
    pages = [
        {"page": 1, "text": "Hello world"},
        {"page": 2, "text": "Hello again"}
    ]
    expected_index = {
        "hello": {
            1: {"frequency": 1, "positions": [0]},
            2: {"frequency": 1, "positions": [0]}
        },
        "world": {1: {"frequency": 1, "positions": [1]}},
        "again": {2: {"frequency": 1, "positions": [1]}}
    }
    assert build_index(pages) == expected_index


def test_build_index_repeated_words():
    pages = [{"page": 1, "text": "Hello hello world"}]
    expected_index = {
        "hello": {1: {"frequency": 2, "positions": [0, 1]}},
        "world": {1: {"frequency": 1, "positions": [2]}}
    }
    assert build_index(pages) == expected_index


def test_build_index_empty_page():
    pages = [{"page": 1, "text": ""}]
    expected_index = {}
    assert build_index(pages) == expected_index


def test_update_index_new_word():
    index = {}
    update_index(index, "hello", 1, 0)
    expected_index = {"hello": {1: {"frequency": 1, "positions": [0]}}}
    assert index == expected_index


def test_update_index_existing_word_new_page():
    index = {"hello": {1: {"frequency": 1, "positions": [0]}}}
    update_index(index, "hello", 2, 0)
    expected_index = {
        "hello": {
            1: {"frequency": 1, "positions": [0]},
            2: {"frequency": 1, "positions": [0]}
        }
    }
    assert index == expected_index


def test_update_index_existing_word_same_page():
    index = {"hello": {1: {"frequency": 1, "positions": [0]}}}
    update_index(index, "hello", 1, 5)
    assert index["hello"][1]["frequency"] == 2
    assert index["hello"][1]["positions"] == [0, 5]


def test_save_index(tmp_path):
    path = tmp_path / "index.json"
    index = {
        "hello": {
            "1": {"frequency": 1, "positions": [0]},
            "2": {"frequency": 1, "positions": [0]}
        }
    }
    save_index(index, str(path))
    assert json.loads(path.read_text()) == index


def test_load_index(tmp_path):
    path = tmp_path / "index.json"
    index = {"hello": {"1": {"frequency": 1, "positions": [0]}}}
    path.write_text(json.dumps(index))
    loaded_index = load_index(str(path))
    assert loaded_index == index


def test_load_index_missing_file(tmp_path, capsys):
    path = tmp_path / "nonexistent.json"
    loaded_index = load_index(str(path))
    out = capsys.readouterr().out.lower()
    assert loaded_index == {}
    assert "failed to load" in out