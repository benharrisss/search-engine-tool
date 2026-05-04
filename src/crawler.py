import time
import requests

from bs4 import BeautifulSoup

TARGET_URL = "https://quotes.toscrape.com/"


def crawl_website(url):
    pages = []
    current_url = url
    page_number = 1

    while current_url:
        print(f"Crawling page {page_number}: {current_url}")
        
        html_content = fetch_page_content(current_url)
        if html_content is None:
            print(f"Error: Failed to fetch content from {current_url}")
            break
        
        text, next_url = parse_page_content(html_content)
        
        # Store the page number and text in the pages list
        pages.append({"page": page_number, "text": text})

        # Move to the next page
        current_url = next_url
        page_number += 1

        if current_url:
            # Politeness window of at least 6 seconds between requests
            time.sleep(6)

    return pages


def fetch_page_content(url):
    print(f"Fetching content from: {url}")
    try:
        # Make the HTTP request to fetch the page content
        response = requests.get(url)
        response.raise_for_status()
        return response.text

    except requests.RequestException as e:
        print(f"Error: Failed to fetch {url}: {e}")
        return None


def parse_page_content(html_content):
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Extract text from the page
    text = extract_text(soup)

    # Find the link to the next page through next button, if it exists
    next_button = soup.find("li", class_="next")
    if next_button:
        next_link = next_button.find("a")["href"]
        next_url = TARGET_URL + next_link
    else:
        next_url = None

    return text, next_url


def extract_text(soup):
    # Extract quotes as text
    quotes = soup.find_all("div", class_="quote")

    text_list = []

    for quote in quotes:
        # Extract the quote text and add it to the text list
        quote_text = quote.find("span", class_="text").get_text()
        text_list.append(quote_text)

    return " ".join(text_list)