import pysolr
import logging
from mediawiki_parser.preprocessor import make_parser as wiki_pre_parser
from mediawiki_parser.html import make_parser as wiki_html_parser
from bs4 import BeautifulSoup as bs
import re


logging.getLogger().setLevel(level=logging.ERROR)

EXACT_SEARCH_RESULTS = 100
solr_instance = pysolr.Solr('http://liuqing.dlib.vt.edu:8983/solr/wikipedia')
wiki_pre_processor = wiki_pre_parser({})
wiki_post_processor = wiki_html_parser()


def search(term):
    """Returns: page_name, full_text"""
    try:
        results = solr_instance.search('title:('+term+')', rows=1).docs
    except:
        return None, None
    
    if not len(results):
        return None, None

    return results[0]['title_cs'], soup_to_text(get_soup(results[0]))


def exact_search(name):
    try:
        results = solr_instance.search(
            'title_cs:"'+name+'"',
            rows=str(EXACT_SEARCH_RESULTS),
            fl='title_cs,id'
        ).docs
    except:
        return None

    for r in results:
        if r['title_cs'] == name:
            results = solr_instance.search('id:'+r['id']).docs
            if len(results) == 1:
                return results[0]
            return None
    return None


def get_soup(result):
    if not result:
        return None

    regex = r'#REDIRECT\s*?\[\[(.*?)\]\]'
    redirect = re.search(regex, result['text'], re.IGNORECASE)
    if redirect:
        return get_soup(exact_search(redirect.group(1)))

    try:
        markup = wiki_post_processor.parse(
            wiki_pre_processor.parse(result['text']).leaves()).value
    except:
        return None

    soup = bs(markup, 'html.parser')

    a_tags = soup.findAll('a')
    templates = [a for a in a_tags if a['href'].startswith('Template:')]
    for t in templates:
        t.extract()

    return soup


def soup_to_text(soup):
    if not soup:
        return None
    text = soup.getText().strip()
    regex = r'<ref.*?>.*?<\/ref>|<ref.*?/>|<br[\s/]*?>|</?sub>'
    text = re.sub(r'\n', ' ', text)
    text = re.sub(regex, '', text)
    return text
