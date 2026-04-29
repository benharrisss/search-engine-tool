import re


def normalise_query(words):
    normalised_words = []

    for word in words:
        # lowercase
        word = word.lower()

        # remove punctuation
        word = re.sub(r'[^\w\s]', '', word)

        # Only add non-empty words
        if word:
            normalised_words.append(word)

    return normalised_words


def get_pages_for_word(index, word):
    if word in index:
        key_set = set()
        for key in index[word]:
            key_set.add(key)
        return key_set
    else:
        return set()


def print_word(index, word):
    if word:
        word = normalise_query([word])[0]
    else:
        print("Error: No word provided for print command.")
        return

    if word not in index:
        print(f"Word '{word}' not found in index.")
        return

    print(f"Inverted index for '{word}':")

    for page, data in index[word].items():
        print(f"Page {page}: Frequency = {data['frequency']}, Positions = {data['positions']}")


def find_words(index, words):
    words = normalise_query(words)

    if not words:
        print("Error: No words provided for find command.")
        return

    page_sets = []

    for word in words:
        pages = get_pages_for_word(index, word)

        if not pages:
            print(f"Word '{word}' not found in index. No results.")
            return

        page_sets.append(pages)

    # Intersect the sets of pages for all words
    result_pages = set.intersection(*page_sets)

    if not result_pages:
        print("No pages contain all the specified words.")
        return []

    result_pages = sorted(result_pages)

    print(f"Pages containing {' and '.join(words)}: {result_pages}")

    return result_pages