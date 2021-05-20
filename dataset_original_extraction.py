import pandas as pd
import requests
from tqdm import tqdm

tqdm.pandas()

pd.options.display.max_columns = 500

dataset = pd.read_csv('dataset_22_mal_new_features.csv')
dataset_20 = pd.read_csv('dataset_20_new_features.csv').drop(columns = ['Unnamed: 0'])

print(len(dataset))

tlds = dataset_20['tld'].unique()

def check_if_https(url):
    try:
        r = requests.get(url)
        if 'https' in r.url:
            return 'yes'
        else:
            return 'no'
    except:
        return 'unknown'


def get_tld(url):
    for tld in tlds:
        if tld in url:
            return tld
    return 'no_tld'

dataset['https'] = dataset['url'].progress_apply(lambda x: check_if_https(x))
dataset['tld'] = dataset['url'].progress_apply(lambda x: get_tld(x))

print(len(dataset[dataset['https'] == 'unknown']))

print(dataset.head())