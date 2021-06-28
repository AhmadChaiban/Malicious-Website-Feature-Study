# !pip install pysafebrowsing
# !pip install tld
# !pip install whois
# !pip install geoip2

# pip uninstall whois
# pip install python-whois


import pandas as pd
import requests
from tqdm import tqdm
from tld import get_tld
import whois
import http.client
from bs4 import BeautifulSoup

tqdm.pandas()

pd.options.display.max_columns = 500

dataset = pd.read_csv('./2 - custom_features_data/malicious_new_features_8.csv')

def check_if_https(url):
    https_status= 'no'
    try:
        conn = http.client.HTTPSConnection(url.replace('https://', '').replace('http://',''), timeout=1)
        conn.request("HEAD", "/")
        res = conn.getresponse()
        if res.status == 200 or res.status==301 or res.status==302:
            https_status = 'yes'
        #print(x,res.status,res.reason,https_status)
    except Exception as msg:
        return 'no'
        #print(x,"Error: ",msg)
    finally:
        return https_status


def get_who_is(url):
    try:
        domain = whois.whois(url)
        #print(domain.registrar)
        if len(str(domain.registrar)) >1 :
            return 'complete'
        else:
            return 'incomplete'
    except:
        return 'incomplete'

def ret_tld(url):
    try:
        u = url
        s = get_tld(str(u), fix_protocol=True)
        return s
    except:
        return 'unknown'


def get_url_content(url):
    try:
        r = requests.get(url, timeout=10).text
        soup = BeautifulSoup(r, 'html.parser')
        return str(soup)
    except:
        return 'could not fetch content'


#print(get_who_is(dataset['url'].iloc[0]))

# dataset['https'] = dataset['url'].progress_apply(lambda x: check_if_https(x))
# dataset.to_csv('./3 - separate_pending_data/batch_mal_8/malicious_https.csv', index=False)
# print(dataset['https'].value_counts())
#
#
# dataset['tld'] = dataset['url'].progress_apply(lambda x: ret_tld(x))
# dataset['url_len'] = dataset['url'].progress_apply(lambda x: len(x))
# dataset.to_csv('./3 - separate_pending_data/batch_mal_8/malicious_tld_urllen.csv', index=False)
# print(dataset['tld'].value_counts())

# dataset['who_is'] = dataset['url'].progress_apply(lambda x: get_who_is(x))
# dataset.to_csv('./3 - separate_pending_data/batch_mal_8/malicious_whois.csv', index=False)
# print(dataset['who_is'].value_counts())

dataset['content'] = dataset['url'].progress_apply(lambda x: get_url_content(x))
dataset.to_csv('./3 - separate_pending_data/batch_mal_8/malicious_content.csv', index=False)
print(len(dataset[dataset['content'] == 'could not fetch content']))


# print(dataset.head())

#dataset.to_csv('final_malicious_features_https.csv', index=False)
