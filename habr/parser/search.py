from typing import Optional

import requests
from bs4 import BeautifulSoup

from .article import Article, ArticleParser


class SearchParser:
    search: str
    order: str
    pages: int
    _articles: list[Article]

    def __init__(self, *, search: str, order: Optional[str] = 'relevance', pages: Optional[int] = 5):
        self.search = search
        self.order = order
        self.pages = pages
        self._articles = list()

    def parse(self) -> list[Article]:
        for page_num in range(1, self.pages + 1):
            print(f'Parsing page {page_num}')
            page = requests.get(f'https://habr.com/ru/search/page{page_num}'
                                f'?q={self.search}&target_type=posts&order={self.order}')

            soup = BeautifulSoup(page.text, "html.parser")
            els = soup.find_all("article", class_="tm-articles-list__item")

            if len(els) == 0:
                break

            for el in els:
                id = el.get('id')
                link = el.find('a', class_='tm-article-snippet__readmore', href=True)

                try:
                    link = link['href']
                    try:
                        self._articles.append(ArticleParser(id, link).parse())
                    except Exception as e:
                        print(id, ' skipped: ', link)
                        raise e

                except TypeError or KeyError:
                    title = el.find('h2', class_='tm-article-snippet__title tm-article-snippet__title_h2').find('span').text
                    user = el.find('span', class_='tm-user-info__user')
                    time = el.find('span', class_='tm-article-snippet__datetime-published')
                    body = el.find('div', class_='article-formatted-body')

                    self._articles.append(
                        Article(
                            id=el.get('id'),
                            title=title if title else "",
                            published=time.text.strip() if time else "",
                            author=user.text.strip() if user else "",
                            body=body.text.strip() if body else "",
                            tags=[]
                        )
                    )

        return self._articles
