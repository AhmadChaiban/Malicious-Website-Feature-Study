import pandas as pd

dataset_https = pd.read_csv('./3 - separate_pending_data/batch_mal_7/malicious_https.csv')
dataset_tld_urllen = pd.read_csv('./3 - separate_pending_data/batch_mal_7/malicious_tld_urllen.csv')
dataset_content = pd.read_csv('./3 - separate_pending_data/batch_mal_7/malicious_content.csv')
dataset_whois = pd.read_csv('./3 - separate_pending_data/batch_mal_7/malicious_whois.csv')

dataset = pd.concat([
    dataset_tld_urllen,
    dataset_https['https'],
    dataset_whois['who_is'],
    dataset_content['content']
],axis=1).drop(columns=['Unnamed: 0'])


dataset['label'] = 'bad'

dataset.to_csv('./4 - final_data/final_mal_7.csv', index=False)
