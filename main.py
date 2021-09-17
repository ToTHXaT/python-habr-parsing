from pprint import pprint, pformat
import requests
from bs4 import BeautifulSoup
import json
import csv

order = ['relevance', 'date', 'rating'][0]

articles = []
for page in range(1, 6):
    search = 'WebAssembly'
    page = requests.get(f'https://habr.com/ru/search/page{page}?q={search}&target_type=posts&order={order}')

    soup = BeautifulSoup(page.text, "html.parser")
    els = soup.find_all("article", class_="tm-articles-list__item")

    if len(els) == 0:
        break

    for el in els:
        title = el.find('h2', class_='tm-article-snippet__title tm-article-snippet__title_h2')
        title_span = title.find('span')
        title_text = title_span.text

        user = el.find('span', class_='tm-user-info__user')
        time = el.find('span', class_='tm-article-snippet__datetime-published')
        link = el.find('a', class_='tm-article-snippet__readmore', href=True)
        body = el.find('div', class_='article-formatted-body')

        try:
            link = 'habr.com' + link['href']
        except:
            link = None

        articles.append({
            'id': el.get('id'),
            'title': title_text,
            'author': user.text.strip(),
            'published': time.text.strip(),
            'full_version': link,
            'body': body.text.strip(),
        })

with open('result.txt', 'w') as file:
    file.write(pformat(articles))
# with open('result.csv', 'w') as file:
#     writer = csv.writer(file, delimiter="\t")
#     for article in articles:
#         writer.writerow([article['id'], article['title'], article['author'], article['published'], article['full_version'], article['body']])
import pickle
with open('file.pickle', 'wb') as file:
    pickle.dump(articles, file)



