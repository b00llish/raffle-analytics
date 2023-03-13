from config import Config
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy import text
from tqdm import tqdm

query = '''
    DROP MATERIALIZED VIEW IF EXISTS public.data_overview;
    DROP MATERIALIZED VIEW IF EXISTS public.fact_raffles;
    DROP MATERIALIZED VIEW IF EXISTS public.fact_buys;
    DROP MATERIALIZED VIEW IF EXISTS public.total_sales;
'''

# Create engine and metadata objects
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
metadata = MetaData()

# Reflect the database schema into the metadata
metadata.reflect(bind=engine)

with engine.connect() as connection:
    connection.execute(text(query))
    connection.commit()

tables = ('cancels', 'endings', 'winners', 'buys', 'raffles', 'rafflers',
          'nfts', 'collections', 'prices')

for t in tqdm(tables):
    print(f'working on dropping {t}...')
    metadata.tables[f'{t}'].drop(engine, checkfirst=True)
    print(f'{t} has been dropped.')

engine.dispose()
# Get the table objects
# cancels_table = metadata.tables['cancels']
# winners_table = metadata.tables['winners']
# endings_table = metadata.tables['endings']
# buyers_table = metadata.tables['buys']
# raffles_table = metadata.tables['raffles']
# rafflers_tables = metadata.tables['rafflers']
# nfts_tables = metadata.tables['nfts']
#
# # Drop the tables, making sure they exist first
# cancels_table.drop(engine, checkfirst=True)
# winners_table.drop(engine, checkfirst=True)
# endings_table.drop(engine, checkfirst=True)
# buyers_table.drop(engine, checkfirst=True)
# raffles_table.drop(engine, checkfirst=True)
# rafflers_tables.drop(engine, checkfirst=True)

# engine.dispose()
