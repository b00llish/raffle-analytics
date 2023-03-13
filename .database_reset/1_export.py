import pandas as pd
from os.path import join, dirname, abspath
from data import GetExistingFromDB
from tqdm import tqdm

basedir = abspath(dirname(__file__))
tables = ('raffles', 'buys', 'cancels', 'endings', 'winners', 'rafflers',
          'prices', 'collections', 'nfts')

# export and save
path = join(basedir, '.database_reset', '1_exports')
path = join(basedir, '1_exports')

for t in tqdm(tables):
    try:
        query = f'''select * from {t}'''
        df = GetExistingFromDB(query=query)
        file = join(path, t)
        df.to_pickle(file)
    except:
        continue
