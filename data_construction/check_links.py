import pandas as pd
from tqdm import tqdm
import urllib.request
import requests

tqdm.pandas()

dataset_good = pd.read_csv('./malicious_urls_2.csv').sample(frac=1, random_state=42).iloc[40000: , :].head(21000).drop_duplicates()
# .iloc[200000: , :]
def check_if_url_is_active(url):
    try:
        response = requests.head(url, timeout=1)
        if response.status_code == 200:
           return 'active'
        return 'not active'

    except:
        return 'not active'

if __name__ == '__main__':

    print('#################################')
    print('Setting http for each url... ')
    dataset_good['url'] = dataset_good['url'].progress_apply(
        lambda url: ('http://' + url) if 'http' not in url else url
    )
    print('#################################')
    print('Checking if links are active...')
    dataset_good['status'] = dataset_good['url'].progress_apply(
        lambda url: check_if_url_is_active(url)
    )
    print('#################################')
    print('Saving activity dataframe...')
    dataset_good.to_csv('./1 - link_check_data/dataset_bad_activity_8.csv', index=False)

    print(dataset_good['status'].value_counts())
