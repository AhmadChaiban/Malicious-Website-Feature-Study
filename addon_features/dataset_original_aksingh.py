import time
import pandas as pd
import numpy as np
import os
import geoip2.database
import socket
from tqdm import tqdm

tqdm.pandas()

pd.set_option('mode.chained_assignment', None) #Switch off warning

df = pd.read_csv('malicious_new_features.csv')

df['url_len'] = df['URL'].progress_apply(lambda x: len(x))



print(df.head())


