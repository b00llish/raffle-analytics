from config import Config
from sqlalchemy import create_engine, Table, MetaData


# Create engine and metadata objects
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
metadata = MetaData()

# Reflect the database schema into the metadata
metadata.reflect(bind=engine)

# Get the table objects
cancels_table = metadata.tables['cancels']
winners_table = metadata.tables['winners']
endings_table = metadata.tables['endings']
buyers_table = metadata.tables['buys']
raffles_table = metadata.tables['raffles']
rafflers_tables = metadata.tables['rafflers']

# Drop the tables, making sure they exist first
cancels_table.drop(engine, checkfirst=True)
winners_table.drop(engine, checkfirst=True)
endings_table.drop(engine, checkfirst=True)
buyers_table.drop(engine, checkfirst=True)
raffles_table.drop(engine, checkfirst=True)
rafflers_tables.drop(engine, checkfirst=True)

engine.dispose()
