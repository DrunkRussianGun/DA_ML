from itertools import islice
from typing import List, Tuple

from bs4 import BeautifulSoup

import helper


def parse_page(html_content: str) -> Tuple[List[str], List[str]]:
    parser: BeautifulSoup = BeautifulSoup(html_content, 'html.parser')

    subcategories = parser.find_all(class_='CategoryTreeItem')
    subcategories_urls: List[str] = list(helper.get_link_url(subcategory.find('a')) for subcategory in subcategories)

    pages_block = parser.find('div', {'id': 'mw-pages'})
    if pages_block is not None:
        pages_urls: List[str] = helper.get_link_urls(pages_block.find(class_='mw-content-ltr'))
    else:
        pages_urls = []

    return subcategories_urls, pages_urls


def get_related_urls(categories_urls: List[str], max_urls_count: int) -> List[str]:
    urls_list: List[str] = []
    while len(categories_urls) > 0 and len(urls_list) < max_urls_count:
        current_url: str = categories_urls.pop()
        page_content: str = helper.download_page(current_url)

        subcategories_urls: List[str]
        pages_urls: List[str]
        subcategories_urls, pages_urls = parse_page(page_content)

        categories_urls.extend(subcategories_urls)

        remaining_urls_count: int = max_urls_count - len(urls_list)
        pages_urls = list(islice(pages_urls, remaining_urls_count))
        urls_list.extend(pages_urls)
    return urls_list
