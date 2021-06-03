import pandas as pd 
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def get_20_links(page):
    response = requests.get(f'https://db.aa419.org/fakebankslist.php?start={page}').text

    soup = BeautifulSoup(response, 'html.parser') 

    page_links = []
    for i in soup.find_all('a', href=True):
        if 'http://www.' in str(i) or 'https://www.' in str(i):
            page_links.append(process_url(i))
    page_links = clean_url_set(page_links)
    return page_links[0:20]


def process_url(url):
    return str(url).split('a href="')[1].split('" rel=')[0]


def clean_url_set(url_set):
    new_set = []
    negation_set = ["https://www.aa419.org", "validator.w3.org", "www.w3.org"]
    for i in range(len(url_set)):
        if any(negation in url_set[i] for negation in negation_set):
            pass
        else:
            new_set.append(url_set[i])
    return new_set

full_links = []
counter = 40001
for i in tqdm(range(0, 2000)):
    for link in get_20_links(counter):
        full_links.append(link)
    counter += 20

print(full_links)

new_malicious = pd.DataFrame(full_links)

new_malicious.to_csv('new_malicious_2.csv', index=False)




