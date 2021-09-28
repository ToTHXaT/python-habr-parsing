from typing import NamedTuple, Optional

import requests
from bs4 import BeautifulSoup


class Article(NamedTuple):
    id: int
    title: str
    author: str
    published: str
    full_version: Optional[str]
    body: str


class Parser:
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
            page = requests.get(f'https://habr.com/ru/search/page{page_num}'
                                f'?q={self.search}&target_type=posts&order={self.order}')

            soup = BeautifulSoup(page.text, "html.parser")
            els = soup.find_all("article", class_="tm-articles-list__item")

            if len(els) == 0:
                break

            for el in els:
                title = el.find('h2', class_='tm-article-snippet__title tm-article-snippet__title_h2').find('span').text
                # title_span = title.find('span')
                # title_text = title_span.text

                user = el.find('span', class_='tm-user-info__user')
                time = el.find('span', class_='tm-article-snippet__datetime-published')
                link = el.find('a', class_='tm-article-snippet__readmore', href=True)
                body = el.find('div', class_='article-formatted-body')

                try:
                    link = 'habr.com' + link['href']
                except KeyError:
                    link = None

                self._articles.append(
                    Article(
                        id=el.get('id'),
                        title=title,
                        author=user.text.strip(),
                        published=time.text.strip(),
                        full_version=link,
                        body=body.text.strip()
                    )
                )

        return self._articles