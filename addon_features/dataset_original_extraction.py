import pandas as pd
import requests
from tqdm import tqdm
from tld import get_tld
import whois
import http.client
from bs4 import BeautifulSoup

tqdm.pandas()

pd.options.display.max_columns = 500

dataset = pd.read_csv('malicious_new_features.csv')
dataset_20 = pd.read_csv('../dataset_20_new_features.csv').drop(columns = ['Unnamed: 0'])

tlds = dataset_20['tld'].unique()

def check_if_https(url):
    https_status= 'no'
    try:
        conn = http.client.HTTPSConnection(url.replace('https://', '').replace('http://',''))
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
        r = requests.get(url).text
        soup = BeautifulSoup(r, 'html.parser')
        return str(soup)
    except:
        return 'could not fetch content'


#print(get_who_is(dataset['URL'].iloc[0]))

#dataset['https'] = dataset['URL'].progress_apply(lambda x: check_if_https(x))
#dataset.to_csv('final_malicious_features_https.csv', index=False)
# dataset['tld'] = dataset['URL'].progress_apply(lambda x: ret_tld(x))
# dataset['url_len'] = dataset['URL'].progress_apply(lambda x: len(x))
# dataset.to_csv('final_malicious_features_tld_urllen.csv', index=False)

#dataset['who_is'] = dataset['URL'].progress_apply(lambda x: get_who_is(x))
#dataset.to_csv('final_malicious_whois.csv', index=False)

dataset['content'] = dataset['URL'].progress_apply(lambda x: get_url_content(x))
dataset.to_csv('final_malicious_content.csv', index=False)


print(dataset.head())
print(len(dataset[dataset['https']=='yes']))

#dataset.to_csv('final_malicious_features_https.csv', index=False)

