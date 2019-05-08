import pysolr
import wikitextparser as wtp
import logging
from mediawiki_parser.preprocessor import make_parser as wiki_pre_parser
from mediawiki_parser.html import make_parser as wiki_html_parser
from bs4 import BeautifulSoup as bs


logging.getLogger().setLevel(level=logging.ERROR)

solr_instance = pysolr.Solr('http://liuqing.dlib.vt.edu:8983/solr/wikipedia')
wiki_pre_processor = wiki_pre_parser({})
wiki_post_processor = wiki_html_parser()


def search(terms):
    return solr_instance.search('title:('+terms+')').docs


def exact_search(name):
    return solr_instance.search('title_cs:('+name+')').docs[0]


def process(result):
    print('process')
    soup = to_html(result)
    if soup.find().find().name == 'ol' \
            and soup.find().find().find().text.startswith('REDIRECT'):
        return process(exact_search(soup.find().find().find().text))

    return soup


def to_html(result):
    description = wtp.parse(result['text']).sections[0].contents
    return bs(wiki_parser(description), 'html.parser')


def wiki_parser(v):
    return wiki_post_processor.parse(
        wiki_pre_processor.parse(v).leaves()).value


if __name__ == '__main__':
    import sys
    print(process(search(' '.join(sys.argv[1:]))[0]))
