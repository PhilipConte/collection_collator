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
        result = get_result(term)
    except:
        return None, None

    if not result:
        return None, None

    return result['title_cs'], soup_to_text(get_soup(result))


def get_result(term):
    results = solr_instance.search('title:('+term+')', rows=1).docs
    if not len(results):
        return None
    result = results[0]

    regex = r'#REDIRECT\s*?\[\[(.*?)\]\]'
    redirect = re.search(regex, result['text'], re.IGNORECASE)
    while redirect:
        result = exact_search(redirect.group(1))
        if not result:
            return None
        redirect = re.search(regex, result['text'], re.IGNORECASE)
    return result


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

    try:
        markup = wiki_post_processor.parse(
            wiki_pre_processor.parse(result['text']).leaves()).value
    except:
        return None

    soup = bs(markup, 'html.parser')

    for a in soup.findAll('a'):
        if a['href'].startswith('Template:'):
            a.extract()

    return soup


def soup_to_text(soup):
    if not soup:
        return None
    text = soup.getText().strip()
    regex = r'<ref.*?>.*?<\/ref>|<ref.*?/>|<br[\s/]*?>|</?sub>'
    text = re.sub(r'\n', ' ', text)
    text = re.sub(regex, '', text)
    return text
