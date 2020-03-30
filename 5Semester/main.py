from collections import Counter
from typing import List, Dict

import pandas as pd
from pandas import Series
from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import TfidfVectorizer

import helper
import wikipedia_articles_scraper as articles_scraper
import wikipedia_categories_scraper as categories_scraper


def main():
    categories_urls: List[str] = [
        '/wiki/Category:Cars', '/wiki/Category:Countries', '/wiki/Category:Money', '/wiki/Category:Nature'
    ]

    print("Collecting URLs of articles from categories…")
    get_articles_urls(categories_urls, 'articles.csv')

    print("Downloading articles…")
    download_articles('articles.csv', '.html', 'articles.csv')

    print("Parsing articles…")
    parse_articles('articles.csv', 'articles_content.csv', 'articles_links.csv')

    content = pd.read_csv('articles_content.csv', index_col=0)
    tfidf_matrix = calculate_tfidf(content['text'])
    print(tfidf_matrix)


def get_articles_urls(categories_urls: List[str], urls_output_file: str):
    urls_list: pd.DataFrame = pd.DataFrame()
    while len(categories_urls) > 0:
        current_category: str = categories_urls.pop()
        pages_urls: List[str] = categories_scraper.get_related_urls([current_category], 2000)
        urls_list = urls_list.append(pd.DataFrame({'url': pages_urls}), ignore_index=True)
    urls_list.to_csv(urls_output_file)


def download_articles(urls_input_file: str, output_files_prefix: str, paths_output_file: str):
    urls = pd.read_csv(urls_input_file, index_col=0)
    urls = urls.assign(filename=pd.Series(dtype=str))
    for index, row in urls.iterrows():
        url = row['url']
        html_content: str = helper.download_page(url)
        filename: str = str(index) + output_files_prefix
        helper.save_to_file(filename, html_content)
        urls.at[index, 'filename'] = filename
    urls.to_csv(paths_output_file)


def parse_articles(urls_input_file: str, content_output_file: str, links_output_file: str):
    urls = pd.read_csv(urls_input_file, index_col=0)
    indexes_by_urls: Dict[str, int] = {}
    for index, row in urls.iterrows():
        indexes_by_urls[row['url']] = index

    pages_content: pd.DataFrame = pd.DataFrame()
    links: pd.DataFrame = pd.DataFrame()
    for index, row in urls.iterrows():
        html_content: str = helper.read_from_file(row['filename'])

        text, links_on_page = articles_scraper.parse_page(html_content)
        pages_content = pages_content.append(pd.DataFrame(data={'text': [text]}, index=[index]))

        links_on_page_indexes: Counter[int] = Counter(
            indexes_by_urls[url] for url in links_on_page if url in indexes_by_urls)
        links = links.append(pd.DataFrame(
            {
                'from': [index] * len(links_on_page_indexes),
                'to': list(links_on_page_indexes.keys()),
                'count': list(links_on_page_indexes.values())
            }),
                             ignore_index=True)
    pages_content.to_csv(content_output_file)
    links.fillna('NaN').astype(int).to_csv(links_output_file, index=False)


def calculate_tfidf(corpus: Series) -> csr_matrix:
    vectorizer = TfidfVectorizer(stop_words='english')
    return vectorizer.fit_transform(corpus)


if __name__ == '__main__':
    main()
