from dataclasses import dataclass
from typing import NamedTuple, Optional
import requests
from bs4 import BeautifulSoup


@dataclass
class Article:
    __slots__ = ('id', 'title', 'author', 'published', 'body', 'tags')
    id: int
    title: str
    author: str
    published: str
    body: str
    tags: list[str]

    def __str__(self):
        return f"{self.id}: {self.title}\n by {self.author}\n at {self.published}\n {self.body[:20]}..."

    def get_all_text(self) -> str:
        return '\n'.join((self.title, self.author, self.body))


class ArticleParser:
    __slots__ = ('id', 'link')
    id: int
    link: str

    def __init__(self, _id: int, link: str):
        self.id = _id
        self.link = link

    def parse(self) -> Optional[Article]:
        print(f'    Parsing article {self.link}')
        article_page = requests.get(f'http://habr.com{self.link}')

        soup = BeautifulSoup(article_page.text, 'html.parser')

        article = soup.find('article', class_='tm-page-article__content tm-page-article__content_inner')

        if article:
            try:
                title = article.find('h1', class_='tm-article-snippet__title tm-article-snippet__title_h1').find('span')

                user = article.find('span', class_='tm-user-info__user')
                time = article.find('span', class_='tm-article-snippet__datetime-published')
                article_body = article.find('div', class_='tm-article-body')

                try:
                    _tags = article.find('div', class_='tm-article-body__tags-links')\
                        .find_all('span', class_='tm-article-body__tags-item')
                    tags = [i.text for i in _tags]
                except Exception:
                    tags = []

                return Article(
                    id=self.id,
                    title=title.text.strip(),
                    author=user.text.strip(),
                    published=time.text.strip(),
                    body=article_body.text.strip(),
                    tags=tags
                )
            except ValueError:
                return None

