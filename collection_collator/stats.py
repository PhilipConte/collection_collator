import pandas as pd
import os


def get_percent(df):
    count = df['Wikipedia'].count()
    rows = df.shape[0]
    print('{} of {} or {}%'.format(count, rows, round(count/rows*100, 2)))


for i in [f for f in os.listdir('.') if f.endswith('.csv')]:
    print(i[:-4]+':')
    get_percent(pd.read_csv(i))
