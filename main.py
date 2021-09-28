from habr.parser import Parser


def main():
    articles = Parser(search='Криптография', pages=1).parse()
    print(articles)


if __name__ == '__main__':
    main()



