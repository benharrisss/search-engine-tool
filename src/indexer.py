import re
import json


def build_index(pages):
    inverted_index = {}
    
    for page in pages:
        page_number = page["page"]
        text = page["text"]

        words = process_text(text)

        for position, word in enumerate(words):
            # Update the inverted index for each word
            update_index(inverted_index, word, page_number, position)

    return inverted_index


def process_text(text):
    # lowercase
    text = text.lower()

    # remove punctuation
    text = re.sub(r'[^\w\s]', '', text)

    # split into words
    words = text.split()

    return words


def update_index(index, word, page, position):
    if word not in index:
        index[word] = {}
    
    if page not in index[word]:
        index[word][page] = {"frequency": 0, "positions": []}

    index[word][page]["frequency"] += 1
    index[word][page]["positions"].append(position)


def save_index(index, filename):
    with open(filename, 'w') as f:
        json.dump(index, f)


def load_index(filename):
    with open(filename, 'r') as f:
        return json.load(f)
