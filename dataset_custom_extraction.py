import pandas as pd
from IPy import IP
import re
import urllib
import geograpy
import time


dataset_22 = pd.read_csv('./datasets_for_project/dataset_22.csv')
dataset_22_mal = dataset_22[dataset_22['label'] == 1]
dataset_22_mal['url'] = dataset_22_mal['url'].apply(lambda x: f'http://{x}' if 'http' not in x else x)

# urls = dataset_22_mal['url'][dataset_22_mal['label'] == 1].iloc[0:20]
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

dataset_22_mal['has_IP_in_URL'] = dataset_22_mal['url'].apply(lambda x: 1 if urls_have_ips(x) else 0)
dataset_22_mal['number_subdomains'] = dataset_22_mal['url'].apply(lambda x: get_number_subdomains(x))
dataset_22_mal['hostname'] = dataset_22_mal['url'].apply(lambda x: get_hostname(x))
dataset_22_mal['length_hostname'] = dataset_22_mal['url'].apply(lambda x: len(get_hostname(x)))
dataset_22_mal['ratio_digits_url'] = dataset_22_mal['url'].apply(lambda x: get_ratio_digits_url(x))
dataset_22_mal['having_@_in_url'] = dataset_22_mal['url'].apply(lambda x: check_at_symbol(x))
dataset_22_mal['ratio_digits_hostname'] = dataset_22_mal['hostname'].apply(lambda x: get_ratio_digits_url(x))
dataset_22_mal['number_underscores'] = dataset_22_mal['url'].apply(lambda x: x.count('_'))

dataset_22_mal.to_csv('dataset_22_mal_new_features.csv')

print(dataset_22_mal.head(30))


