from bs4 import BeautifulSoup
from crawler import extract_text, parse_page_content, fetch_page_content
from unittest.mock import patch
import requests


def test_extract_text_simple():
    html = """
    <div class="quote">
        <span class="text">"Hello world!"</span>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")
    assert "Hello world!" in extract_text(soup)


def test_extract_text_multiple_quotes():
    html = """
    <div class="quote">
        <span class="text">"Quote one"</span>
    </div>
    <div class="quote">
        <span class="text">"Quote two"</span>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")
    assert "Quote one" in extract_text(soup)
    assert "Quote two" in extract_text(soup)


def test_extract_text_empty():
    html = """
    <html>
        <body>
        </body>
    </html>
    """
    soup = BeautifulSoup(html, "html.parser")
    assert extract_text(soup) == ""


def test_parse_page_content_next_url():
    html = """
    <div class="quote">
        <span class="text">Hello world!</span>
    </div>
    <li class="next"><a href="/page/2/">Next</a></li>
    """
    text, next_url = parse_page_content(html)
    assert text == "Hello world!"
    assert "/page/2/" in next_url


def test_parse_page_content_no_next():
    html = """
    <div class="quote">
        <span class="text">Hello world!</span>
    </div>
    """
    text, next_url = parse_page_content(html)
    assert text == "Hello world!"
    assert next_url is None


@patch("crawler.requests.get")
def test_fetch_page_content_success(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = "<html></html>"

    url = "https://quotes.toscrape.com/"
    content = fetch_page_content(url)
    assert content == "<html></html>"


@patch("crawler.requests.get")
def test_fetch_page_content_failure(mock_get):
    mock_get.side_effect = requests.RequestException("Network error")

    url = "https://quotes.toscrape.com/"
    content = fetch_page_content(url)
    assert content is None


