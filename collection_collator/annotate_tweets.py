import pandas as pd
import wordninja
from get_tweets import gen_all
from search_wikipedia import populate_description
from solr import search

tags_df = pd.read_csv('tags.csv')


def wiki_lookup(row):
    """
    returns a series of [Description, Event Name]
    """
    terms = row['Collection Terms']
    if len(terms) > 4:
        terms = ' '.join(wordninja.split(terms))
    print(row['Collection Terms']) # japan earthquake
    name, full_text = search(terms)

    if not name or not full_text:
        print("[{}][{}] No Page Found for '{}' \n".format(
            row['Database'], row['ID'], row['Collection Terms']))
        return pd.Series((row['Description'], None,))

    if row['Description']:
        return pd.Series((row['Description'], name,))

    return pd.Series((populate_description(full_text, row['Collection Terms']), name,))


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
    df[['Description', 'Event Name']] = df.apply(wiki_lookup, axis=1)
    df[['Tags', 'Category_1', 'Category_2', 'Category_3']
       ] = df.apply(get_tags, axis=1)
    df = df[['Database', 'ID', 'Source', 'Collection Terms',
             'Description', 'Tags', 'Category_1', 'Category_2', 'Category_3',
             'Event Name', 'Create Time', 'Count']]
    df.to_csv(path, index=False)


if __name__ == '__main__':
    import sys
    if (len(sys.argv) == 2):
        annotate(sys.argv[1])
    else:
        print("please provide the path to write to (including name)")
