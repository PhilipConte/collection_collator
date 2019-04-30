from urllib.request import urlopen as uo
from bs4 import BeautifulSoup as bs
import pandas as pd


def to_df(html):
    cols = [h.text for h in html.find_all('th')]
    t = [[c.text for c in r.find_all('td')] for r in html.find_all('tr')[1:]]
    return pd.DataFrame(t, columns=cols)


def get_tables(url):
    return [to_df(t) for t in bs(uo(url), 'html.parser').find_all('table')]


def gen_ytk():
    df = get_tables('http://ytk1.dlib.vt.edu/twitter/')[0]
    df = df.drop(labels=['', 'Screen Name'], axis=1)
    rename = {'Archive ID': 'ID', 'Keyword / Hashtag': 'Collection Terms'}
    df = df.rename(columns=rename)
    df['Database'] = 'Collect_yTK'
    df['Source'] = 'yTK'
    df['Create Time'] = df['Create Time'].map(lambda s: s.replace('/', '-'))
    return df


def gen_sfm():
    dfs = get_tables('http://vis.dlib.vt.edu/main/sfm_stat.php')
    rename = {'Archive ID': 'ID', 'Keyword / Hashtag': 'Collection Terms'}
    df = pd.concat([dfs[0], dfs[2]])  # currently excluding account collections
    df = df.rename(columns=rename)
    df['Database'] = 'Collect_yTK'
    df['Source'] = 'yTK, SFM'
    return df


def gen_all():
    df = pd.concat([gen_ytk(), gen_sfm()], sort=True)
    return df
