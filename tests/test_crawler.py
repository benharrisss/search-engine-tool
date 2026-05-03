from bs4 import BeautifulSoup
from crawler import extract_text, parse_page_content, fetch_page_content, crawl_website
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


def test_parse_page_content_empty():
    html = ""
    text, next_url = parse_page_content(html)
    assert text == ""
    assert next_url is None


def test_parse_page_content_malformed_html():
    html = """
    <div class="quote">
        <span class="text">Hello world!
    </div>
    <li class="next"><a href="/page/2/">Next</a></li>
    """
    text, next_url = parse_page_content(html)
    assert "Hello world!" in text
    assert "/page/2/" in next_url


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


@patch("crawler.requests.get")
def test_fetch_page_content_non_200(mock_get):
    mock_get.return_value.raise_for_status.side_effect = requests.HTTPError("404 Not Found")
    url = "https://quotes.toscrape.com/"
    content = fetch_page_content(url)
    assert content is None

@patch("crawler.time.sleep")
@patch("crawler.parse_page_content")
@patch("crawler.fetch_page_content")
def test_crawl_website_politeness_between_pages(mock_fetch, mock_parse, mock_sleep):
    mock_fetch.side_effect = ["<html1>", "<html2>"]
    mock_parse.side_effect = [("Text1", "url2"), ("Text2", None)]
    pages = crawl_website("url1")
    assert pages == [{"page": 1, "text": "Text1"}, {"page": 2, "text": "Text2"}]
    mock_sleep.assert_called_with(6)


def test_crawl_website():
    with patch("crawler.fetch_page_content") as mock_fetch:
        mock_fetch.side_effect = [
            "<html><div class='quote'><span class='text'>Quote 1</span></div><li class='next'><a href='/page/2/'>Next</a></li></html>",
            "<html><div class='quote'><span class='text'>Quote 2</span></div></html>"
        ]
        pages = crawl_website("http://quotes.toscrape.com/")
        assert len(pages) == 2
        assert pages[0]["text"] == "Quote 1"
        assert pages[1]["text"] == "Quote 2"
