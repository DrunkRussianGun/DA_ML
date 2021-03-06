import codecs
from typing import List

import bs4
import requests


def download_wiki_page(url: str) -> str:
    return requests.get('https://en.wikipedia.org' + url).text


def get_link_url(tag: bs4.ResultSet) -> str:
    return str(tag.get('href'))


def get_link_urls(element: bs4.ResultSet) -> List[str]:
    return list(get_link_url(tag) for tag in element.find_all('a'))


def read_from_file(filename: str) -> str:
    file = codecs.open(filename, 'r', 'utf-8')
    content: str = file.read()
    file.close()
    return content


def save_to_file(filename: str, content: str):
    file = codecs.open(filename, 'w', 'utf-8')
    file.write(content)
    file.close()