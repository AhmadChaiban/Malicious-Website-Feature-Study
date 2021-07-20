import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import sys
from multiprocessing import Pool
from glob import glob as globlin
import time
from tqdm import tqdm

dataset_surtur = pd.read_csv('dataset_surtur.csv')

dataset_surtur = dataset_surtur[dataset_surtur['label'] == 1]

url_df = dataset_surtur['url']


def capture_screenshot(url, image_name, driver):
    driver.get(url)
    time.sleep(1)
    driver.save_screenshot(image_name)


def check_progress():
    paths = globlin('./dataset_surt_images_malicious/*.png')
    for i in range(len(paths)):
        paths[i] = int(paths[i].replace('./dataset_surt_images_malicious/','').replace('_0.png','').replace('_1.png',''))
    return max(paths)


def make_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--ignore-ssl-errors=yes")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--port=0")
    return webdriver.Firefox(options=options)


def manage_driver(index):
    driver = make_driver()
    #try:
    current_url = url_df[i]
    image_name = f'dataset_surt_images_malicious/{i}_{dataset_surtur["label"].iloc[i]}.png'
    capture_screenshot(current_url, image_name, driver)
    pbar.update(1)
    driver.close()
    driver.quit()
    #except:
    #    driver.close()
    #    driver.quit()
    #    pbar.update(1)

#last_index = check_progress()

indexes = dataset_surtur[20000:-1].index

if __name__=='__main__':
    with tqdm(total = len(indexes)) as pbar:
        for i in indexes:
            manage_driver(i)

            