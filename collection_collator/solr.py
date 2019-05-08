import pysolr
import wikitextparser as wtp
import logging
from mediawiki_parser.preprocessor import make_parser as wiki_pre_parser
from mediawiki_parser.html import make_parser as wiki_html_parser
from bs4 import BeautifulSoup as bs


logging.getLogger().setLevel(level=logging.ERROR)

EXACT_SEARCH_RESULTS = 100
solr_instance = pysolr.Solr('http://liuqing.dlib.vt.edu:8983/solr/wikipedia')
wiki_pre_processor = wiki_pre_parser({})
wiki_post_processor = wiki_html_parser()


def search(terms):
    return solr_instance.search('title:('+terms+')').docs


def exact_search(name):
    results = solr_instance.search(
        'title_cs:"'+name+'"',
        rows=str(EXACT_SEARCH_RESULTS),
        fl='title_cs,id'
    ).docs

    for r in results:
        if r['title_cs'] == name:
            results = solr_instance.search('id:'+r['id']).docs
            if len(results) == 1:
                return results[0]
            return None
    return None


def get_soup(result):
    description = wtp.parse(result['text']).sections[0].contents
    markup = wiki_post_processor.parse(
        wiki_pre_processor.parse(description).leaves()).value
    soup = bs(markup, 'html.parser')

    if soup.find().find().name == 'ol' \
            and soup.find().find().find().text.startswith('REDIRECT'):
        name = soup.find().find().find().text
        name = ' '.join(name.split()[1:])
        result = exact_search(name)
        if result is None:
            return None
        return get_soup(result)

    return soup
    

def massage_soup(soup):
    first_tag = soup.find().find()
    children = set([child.name for child in first_tag.findAll()])
    if len(children) == 1 and children.pop() == 'a':
        first_tag.extract()
    return soup


if __name__ == '__main__':
    import sys
    print(massage_soup(get_soup(search(' '.join(sys.argv[1:]))[0])))
