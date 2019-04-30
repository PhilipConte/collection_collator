import pandas as pd
from .get_tweets import gen_all
from .search_wikipedia import get_wiki_page
from .middleware import process_row


def wiki_lookup(row):
    """
    returns a series of [wikipedia, Description, Tags, Event Name]
    """
    collection_term = row['Collection Terms']

    wiki_page = get_wiki_page(collection_term)
    print('wiki_page: ' + str(bool(wiki_page)))
    if not wiki_page:
        print("[{}][{}] No Page Found for '{}' \n".format(
            row['Database'], row['ID'], collection_term))
        return pd.Series((None, row['Description'], row['Tags'], None,))
    else:
        return pd.Series(process_row(row['Description'], wiki_page, collection_term))


def annotate(path):
    df = gen_all()
    df[['Wikipedia', 'Description', 'Tags',
        'Event Name']] = df.apply(wiki_lookup, axis=1)
    df = df[['Database', 'ID', 'Source', 'Collection Terms', 'Wikipedia',
             'Description', 'Tags', 'Event Name', 'Create Time', 'Count']]
    df.to_csv('annotated.csv', index=False)


if __name__ == '__main__':
    import sys
    if (len(sys.argv) == 2):
        collection_collator.annotate(sys.argv[1])
    else:
        print("please provide the path to write to (including name)")
