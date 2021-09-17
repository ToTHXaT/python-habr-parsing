from pprint import pprint, pformat
import requests
from bs4 import BeautifulSoup

search = 'JavaScript'
page = requests.get(f'https://habr.com/ru/search/?q={search}&target_type=posts&order=relevance')

with open('index.html', 'w') as file:
    file.write(page.text)


soup = BeautifulSoup(page.text, "html.parser")
els = soup.find_all("article")

articles = []
for el in els:
    title = el.find('h2', class_='tm-article-snippet__title tm-article-snippet__title_h2')
    title_span = title.find('span')
    title_text = title_span.text

    user = el.find('span', class_='tm-user-info__user')
    time = el.find('span', class_='tm-article-snippet__datetime-published')
    link = el.find_all('a', class_='tm-article-snippet__readmore')
    body = el.find('div', class_='article-formatted-body')

    try:
        l = link[0]
    except:
        l = None

    articles.append({
        'title': title_text,
        'author': user.text.strip(),
        'published': time.text.strip(),
        'full_version': l,
        'body': body.text.strip()
    })

pprint(articles)
# with open('result.txt', 'w') as file:
#     file.write(pformat(article))

