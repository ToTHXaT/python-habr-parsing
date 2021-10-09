from collections import Counter
import pickle
import os

from natasha import (
    NamesExtractor,
    MorphVocab,
    Doc,
    Segmenter,
    NewsNERTagger,
    NewsEmbedding,
)

from habr.parser.article import Article
from habr.parser.search import SearchParser


def main():
    search: str = 'Криптография'
    filename: str = f'{search}.pickle'

    if not os.path.isfile(filename):
        print('Started parsing articles')
        articles: list[Article] = SearchParser(search=search, pages=10).parse()
        print('Finished parsing articles')
        with open(filename, 'wb') as file:
            print('Dumping data into file')
            pickle.dump(articles, file)
            print('Finished dumping data')
    else:
        with open(filename, 'rb') as file:
            print('Loading data from file')
            articles: list[Article] = pickle.load(file)
            print('Finished loading data')

    from pymorphy2 import MorphAnalyzer

    pymorph = MorphAnalyzer()

    from yake import KeywordExtractor

    kwe = KeywordExtractor(lan='ru', n=2, top=5, dedupLim=0.9)

    kws: dict[str, int] = {}
    for article in articles:
        kw = kwe.extract_keywords(article.get_all_text())
        kwe2 = (pymorph.parse(i[0])[0].normal_form.lower() for i in kw)

        for i in kwe2:
            kws[i] = kws.get(i, 0) + 1

    print(Counter(kws).most_common(20))

    from wordcloud import WordCloud

    wc = WordCloud(background_color='white', height=400, width=600)

    wc.generate_from_frequencies({k: v for k, v in Counter(kws).most_common(40)})

    wc.to_file(f'{search}_kw_result.png')


    if not os.path.isfile(f'{search}_person_result.png'):

        persons: dict[str, int] = {}
        for article in articles:
            doc = Doc(article.get_all_text())
            doc.segment(Segmenter())
            doc.tag_ner(NewsNERTagger(NewsEmbedding()))

            morph_vocab = MorphVocab()
            names_extractor = NamesExtractor(morph_vocab)

            for span in doc.spans:
                if span.type == 'PER':
                    span.normalize(morph_vocab)
                    span.extract_fact(names_extractor)

            for span in doc.spans:
                if span.type == 'PER':
                    v = ' '.join(span.fact.as_dict.values()) if span.fact else ''
                    if not v:
                        continue
                    word = pymorph.parse(v)[0].normal_form.lower()
                    persons[word] = persons.get(word, 0) + 1

        from wordcloud import WordCloud

        wc = WordCloud(background_color='white', height=400, width=600)

        wc.generate_from_frequencies({k: v for k, v in Counter(persons).most_common(40)})

        wc.to_file(f'{search}_person_result.png')


if __name__ == '__main__':
    main()



