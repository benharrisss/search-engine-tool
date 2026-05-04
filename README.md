# Search Engine Tool

## Project Overview:
This project is a command-line search engine tool developed in Python. It crawls a target website, builds an inverted index of its content, and provides the ability to perform search queries efficiently.

The target website used is:
https://quotes.toscrape.com/

## Features:

The tool is designed to support 4 commands in the command-line interface:
- build
- load
- print {word}
- find {word1} {word2} ...

Additionally the tool features:
- Politeness delay between requests (6 seconds)
- Case-insensitive processing of text
- Inverted index (index.json) containing word frequency and word position(s)
- Unit testing suite with ~95% test coverage

## Project Installation and Setup Instructions:

### 1. Clone the repository 
```bash
git clone https://github.com/benharrisss/search-engine-tool.git
cd search-engine-tool
```

### 2. Create a virtual environment
```bash
python -m venv venv
```

Then activate it using:
```bash
# For Windows
source venv/Scripts/activate

# For Linux or Mac:
source venv/bin/activate
```

### 3. Install depedencies for project
```bash
pip install -r requirements.txt
```
The main dependencies include: requests, beautifulsoup4, pytest, and pytest-cov.

## Usage Examples:

### Running the application:
From the project root, you will want to run:
```bash
python src/main.py
```
You should then be prompted to enter commands by an '>' symbol.

### Build command
Crawls the website and creates the inverted index:
```bash
> build
```

### Load command
Loads a previously saved index from the 'data' directory:
```bash
> load
```

### Print command
Displays the inverted index in the terminal for a given word:
```bash
> print nonsense
```

### Find command
Searches for pages containing one or more inputted words.
```bash
# Single word
> find indifference

# Multiple words
> find good friends
```

### Edge case handling
- All invalid commands are handled with error messages
- Empty queries are rejected
- Non-existent words return no results from the index


## Testing Instructions:

### Running the test suite with pytest:
Again from the project root, you will want to run:
```bash
# For all tests
pytest

# For individual tests
python -m pytest tests/test_crawler.py
python -m pytest tests/test_indexer.py
python -m pytest tests/test_search.py
```

### Checking the test coverage:
```
# To check basic coverage
pytest --cov=src

# For more in-depth statistics on coverage
python -m pytest -q --cov=src --cov-branch --cov-report=term-missing --cov-report=html
```

## Project Structure (As Recommended In The Brief):

```bash
search-engine-tool/
│── src/
│   ├── crawler.py
│   ├── indexer.py
│   ├── search.py
│   ├── main.py
│
│── tests/
│   ├── test_crawler.py
│   ├── test_indexer.py
│   ├── test_search.py
│
│── data/
│   └── index.json
│
│── requirements.txt
│── README.md
│── .gitignore
```

