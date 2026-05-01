from search import get_pages_for_word, print_word, find_words


def test_get_pages_for_word():
    index = {
        "hello": {"1": {"frequency": 2, "positions": [0, 1]}},
        "world": {"1": {"frequency": 1, "positions": [2]}}
    }
    assert get_pages_for_word(index, "hello") == {"1"}
    assert get_pages_for_word(index, "world") == {"1"}
    assert get_pages_for_word(index, "nonexistent") == set()


def test_get_pages_for_word_empty_index():
    index = {}
    assert get_pages_for_word(index, "hello") == set()


def test_find_single_word():
    index = {"hello": {"1": {"frequency": 1, "positions": [0]}}}
    assert find_words(index, ["hello"]) == ["1"]


def test_find_multiple_words():
    index = {
        "hello": {"1": {"frequency": 1, "positions": [0]}},
        "world": {"1": {"frequency": 1, "positions": [1]}}
    }
    assert find_words(index, ["hello", "world"]) == ["1"]


def test_find_word_not_found():
    index = {}
    assert find_words(index, ["hello"]) == None


def test_empty_query():
    index = {
        "hello": {"1": {"frequency": 1, "positions": [0]}},
        "world": {"1": {"frequency": 1, "positions": [1]}}
    }
    assert find_words(index, []) == None


def test_print_word(capsys):
    index = {"hello": {"1": {"frequency": 1, "positions": [0]}}}
    print_word(index, "hello")
    captured = capsys.readouterr()
    assert "hello" in captured.out.lower()


def test_case_insensitive_search():
    index = {"hello": {"1": {"frequency": 1, "positions": [0]}}}
    result = find_words(index, ["HeLLo"])
    assert result == ["1"]


def test_search_with_punctuation():
    index = {"hello": {"1": {"frequency": 1, "positions": [0]}}}
    result = find_words(index, ["hello!"])
    assert result == ["1"]
