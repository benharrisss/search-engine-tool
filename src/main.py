from crawler import crawl_website
from indexer import build_index, save_index, load_index
from search import print_word, find_words

INDEX_FILENAME = "data/index.json"
TARGET_URL = "https://quotes.toscrape.com/"


def main():
    index = None

    print("Welcome to the Search Engine Tool! - Enter a command (build | load | print <word> | find <word1> <word2> ... | exit):")

    while True:
        command = input("> ")
        index = parse_command(command, index)


def handle_build():
    print("Building index...")

    pages = crawl_website(TARGET_URL)
    index = build_index(pages)
    save_index(index, INDEX_FILENAME)

    print(f"Index built and saved to {INDEX_FILENAME}.")
    


def handle_load():
    try:
        index = load_index(INDEX_FILENAME)
        print(f"Index loaded from {INDEX_FILENAME}.")
        return index
    except FileNotFoundError:
        print(f"Error: Index file {INDEX_FILENAME} not found. Please build the index first.")
        return None


def handle_print(index, command_parts):
    if index is None:
        print("Error: No index loaded. Please load the index first.")
        return

    if len(command_parts) != 2:
        print("Error: Print command requires exactly one word argument.")
        return

    word = command_parts[1]
    print_word(index, word)


def handle_find(index, command_parts):
    if index is None:
        print("Error: No index loaded. Please load the index first.")
        return

    if len(command_parts) < 2:
        print("Error: Find command requires at least one word argument.")
        return

    words = command_parts[1:]
    find_words(index, words)


def parse_command(command, index):
    command_parts = command.split()

    if not command_parts:
        return index

    command_name = command_parts[0].lower()
    
    if command_name == "build":
        handle_build()
    elif command_name == "load":
        index = handle_load()
    elif command_name == "print":
        handle_print(index, command_parts)
    elif command_name == "find":
        handle_find(index, command_parts)
    elif command_name == "exit":
        print("Exiting program.")
        exit(0)
    else:
        print(f"Error: Unknown command: {command_name}")

    return index


if __name__ == "__main__":
    main()