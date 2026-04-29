from crawler import crawl_website
from indexer import build_index
from search import print_word, find_words


def main():
    # Tests that crawler.py works as expected
    pages = crawl_website("http://quotes.toscrape.com/")
    index = build_index(pages)

    print_word(index, "life")
    find_words(index, ["life", "love"])
    find_words(index, ["nonexistentword"])
    find_words(index, [])


def handle_build():
    # Placeholder for handling build logic
    print("Handling build command...")
    


def handle_load():
    # Placeholder for handling load logic
    print("Handling load command...")


def handle_print(command_args):
    # Placeholder for handling print logic
    print(f"Handling print command with args: {command_args}")


def handle_find(command_args):
    # Placeholder for handling find logic
    print(f"Handling find command with args: {command_args}")


def parse_command(command):
    print(f"Parsing command: {command}")
    command_parts = command.split()
    command_name = command_parts[0]
    command_args = command_parts[1:]
    
    if command_name == "build":
        handle_build()
    elif command_name == "load":
        handle_load()
    elif command_name == "print":
        handle_print(command_args)
    elif command_name == "find":
        handle_find(command_args)
    else:
        print(f"Unknown command: {command_name}")


if __name__ == "__main__":
    main()