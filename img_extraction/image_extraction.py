import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import sys
from multiprocessing import Pool
import progressbar
from glob import glob as globlin
import time
from tqdm import tqdm

dataset_20 = pd.read_csv('dataset_20_random_samples.csv')

url_df = dataset_20['url']

def capture_screenshot(url, image_name, driver):
    driver.get(url)
    time.sleep(1)
    driver.save_screenshot(image_name)

def check_progress():
    paths = globlin('./dataset_20_images/*.png')
    for i in range(len(paths)):
        paths[i] = int(paths[i].replace('./dataset_20_images/','').replace('_good.png','').replace('_bad.png',''))
    return max(paths) 


def make_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--ignore-ssl-errors=yes")
    options.add_argument("--ignore-certificate-errors")
    return webdriver.Firefox(options=options)

last_index = check_progress()-1


indexes = dataset_20.index[last_index:-1]

if __name__=='__main__':
    with tqdm(total = len(indexes)) as pbar:
        for i in indexes:
            driver = make_driver()
            try:
                current_url = url_df[i]
                image_name = f'dataset_20_images/{i}_{dataset_20["label"].iloc[i]}.png'
                capture_screenshot(current_url, image_name, driver)
                pbar.update(1)
                driver.close()
                driver.quit()
            except:
                driver.close()
                driver.quit()
                pbar.update(1)
        
	
