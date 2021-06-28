import pandas as pd
from IPy import IP
import re
import urllib
import geograpy
import time
from tqdm import tqdm
tqdm.pandas()
pd.options.display.max_columns = 500


dataset = pd.read_csv('./1 - link_check_data/dataset_good_activity_5.csv')

dataset = dataset[dataset['status']=='active']

print(dataset.head())

# urls = dataset['url'][dataset['label'] == 1].iloc[0:20]
#
# def get_location(url):
#     # start_time = time.time()
#     print(url)
#     # places = geograpy.get_geoPlace_context(url=f'http://{url}')
#     # print(places)
#     # print(time.time() - start_time)

def urls_have_ips(url):
    split_string = re.split('/|.com', url)
    for word in split_string:
        try:
            IP(word)
            return True
        except:
            pass
    return False

def get_number_subdomains(url_string):
    removed_http = url_string.replace('http://', '').replace('https://', '')
    sub_array = removed_http.split('/')[0].replace('.com','').split('.')
    return len(sub_array) - 1

def get_hostname(url):
    parsed_url = urllib.parse.urlparse(url)
    return parsed_url.netloc

def get_ratio_digits_url(url):
    try:
        return sum(c.isdigit() for c in url)/len(url)
    except:
        return 0

def check_at_symbol(url):
    if '@' in url:
        return 1
    return 0

dataset['has_IP_in_url'] = dataset['url'].progress_apply(lambda x: 1 if urls_have_ips(x) else 0)
dataset['number_subdomains'] = dataset['url'].progress_apply(lambda x: get_number_subdomains(x))
dataset['hostname'] = dataset['url'].progress_apply(lambda x: get_hostname(x))
dataset['length_hostname'] = dataset['url'].progress_apply(lambda x: len(get_hostname(x)))
dataset['ratio_digits_url'] = dataset['url'].progress_apply(lambda x: get_ratio_digits_url(x))
dataset['having_@_in_url'] = dataset['url'].progress_apply(lambda x: check_at_symbol(x))
dataset['ratio_digits_hostname'] = dataset['hostname'].progress_apply(lambda x: get_ratio_digits_url(x))
dataset['number_underscores'] = dataset['url'].progress_apply(lambda x: x.count('_'))

dataset.to_csv('./2 - custom_features_data/benign_new_features_5.csv')

print(dataset.head(30))
