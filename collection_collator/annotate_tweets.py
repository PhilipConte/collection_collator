import pandas as pd
from get_tweets import gen_all
from search_wikipedia import get_wiki_page
from middleware import process_row

tags_df = pd.read_csv('tags.csv')


def wiki_lookup(row):
    """
    returns a series of [wikipedia, Description, Event Name]
    """
    collection_term = row['Collection Terms']

    wiki_page = get_wiki_page(collection_term)
    print('wiki_page: ' + str(bool(wiki_page)))
    if not wiki_page:
        print("[{}][{}] No Page Found for '{}' \n".format(
            row['Database'], row['ID'], collection_term))
        return pd.Series((None, row['Description'], None,))
    else:
        return pd.Series(process_row(row['Description'], wiki_page, collection_term))


def get_tags(row):
    """
    returns a series of ['Tags', 'Category_1', 'Category_2', 'Category_3']
    """
    match = tags_df.loc[tags_df['Collection Terms'] == row['Collection Terms']]
    if (match.shape[0] == 0):
        return pd.Series((None, None, None, None,))

    match = match.iloc[0]
    return pd.Series((row['Tags'] if row['Tags'] else match['Tags'],
                      match['Category_1'], match['Category_2'],
                      match['Category_3']))


def annotate(path):
    df = gen_all()
    df[['Wikipedia', 'Description',
        'Event Name']] = df.apply(wiki_lookup, axis=1)
    df[['Tags', 'Category_1', 'Category_2', 'Category_3']
       ] = df.apply(get_tags, axis=1)
    df = df[['Database', 'ID', 'Source', 'Collection Terms', 'Wikipedia',
             'Description', 'Tags', 'Category_1', 'Category_2', 'Category_3',
             'Event Name', 'Create Time', 'Count']]
    df.to_csv(path, index=False)


if __name__ == '__main__':
    import sys
    if (len(sys.argv) == 2):
        annotate(sys.argv[1])
    else:
        print("please provide the path to write to (including name)")
