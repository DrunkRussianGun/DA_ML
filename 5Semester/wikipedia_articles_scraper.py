from typing import Tuple, List

from bs4 import BeautifulSoup

import helper

article_prefix: str = '/wiki/'
file_prefix: str = '/wiki/File:'


def parse_page(html_content: str) -> Tuple[str, List[str]]:
    parser: BeautifulSoup = BeautifulSoup(html_content, 'html.parser')

    body = parser.find(class_='mw-parser-output')
    [tag.extract() for tag in body.find_all('style')]
    [tag.extract() for tag in body.find_all('div', class_='hatnote navigation-not-searchable')]
    [tag.extract() for tag in body.find_all('a') if not helper.get_link_url(tag).startswith(article_prefix)]

    links = helper.get_link_urls(body)
    links = (url for url in links if not str(url).startswith(file_prefix))

    return body.get_text(), list(links)


def get_text_and_links(url: str) -> Tuple[str, List[str]]:
    page_content: str = helper.download_page(url)
    return parse_page(page_content)
