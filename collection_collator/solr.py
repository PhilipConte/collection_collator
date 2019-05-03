import pysolr
import wikitextparser as wtp
import logging
from mediawiki_parser.preprocessor import make_parser as pre_parser
from mediawiki_parser.html import make_parser as html_parser

logging.getLogger().setLevel(level=logging.ERROR)

solr_instance = pysolr.Solr('http://liuqing.dlib.vt.edu:8983/solr/wikipedia')
preprocessor = pre_parser({})
parser = html_parser()


def search(terms):
    return solr_instance.search('title:('+terms+')').docs


def process(result):
    description = wtp.parse(result['text']).sections[0].contents

    if description.startswith('#redirect [['):
        new_page = description.split('[[')[1].split(']]')[0]
        new_result = search(new_page)[0]
        if new_result['title'] == result['title']:
            return None
        return process(new_result)

    preprocessed_text = preprocessor.parse(description)
    return parser.parse(preprocessed_text.leaves()).value


if __name__ == '__main__':
    import sys
    print(process(search(' '.join(sys.argv[1:]))[0]))
