from typing import Tuple, List
from bs4 import BeautifulSoup

import helper


def parse_page(html_content: str) -> Tuple[str, List[str]]:
    parser = BeautifulSoup(html_content, 'html.parser')

    body = parser.find(class_='mw-parser-output')
    [tag.extract() for tag in body.find_all('style')]
    [tag.extract() for tag in body.find_all('div', class_='hatnote navigation-not-searchable')]
    [tag.extract() for tag in body.find_all('a') if not helper.get_link_url(tag).startswith('/wiki/')]

    links = helper.get_link_urls(body)

    return body.get_text(), list(links)


def get_text_and_links(url: str) -> Tuple[str, List[str]]:
    page_content: str = helper.download_wiki_page(url)
    return parse_page(page_content)
