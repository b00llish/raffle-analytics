import pandas as pd
from os.path import join, dirname, abspath
from app.models import Raffler, Raffle, Buy, Cancel, End, Winner
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from config import Config

# open files
basedir = abspath(dirname(__file__))

if __name__ == '__main__':
    path = join(basedir, '.database_reset', '1_exports') # if pasting into pyConsole
else:
    path = join(basedir, '1_exports')  # if running as script

# import data
df_rafflers = pd.read_pickle(join(path, 'rafflers'))
df_raffles = pd.read_pickle(join(path, 'raffles'))
df_buys = pd.read_pickle(join(path, 'buys'))
df_cancels = pd.read_pickle(join(path, 'cancels'))
df_wins = pd.read_pickle(join(path, 'winners'))
df_ends = pd.read_pickle(join(path, 'endings'))

# set session
session = Session(bind=create_engine(Config.SQLALCHEMY_DATABASE_URI))

# compile all rafflers
filt = df_wins.winner_wallet.isin(df_rafflers.wallet)
new_rafflers = df_wins.loc[~filt].drop_duplicates()
new_rafflers['dao_status'] = 'amateur/non-dao'
new_rafflers['twitter'] = 'unlinked'
new_rafflers.rename(columns={'winner_wallet': 'wallet'}, inplace=True)
new_rafflers = new_rafflers[['wallet', 'twitter', 'dao_status']]
df_rafflers = pd.concat([df_rafflers, new_rafflers]).drop_duplicates()

# Insert the df_raffles DataFrame into the raffles table
rafflers = [Raffler(
    wallet=row['wallet'],
    twitter=row['twitter'],
    dao_status=row['dao_status']
) for _, row in df_rafflers.iterrows()]

print(rafflers)  # Add this line to check if the Raffle instances are being properly created

session.bulk_save_objects(rafflers)
session.commit()

# Query all existing Raffler instances and create a dictionary with wallet as the key
rafflers = session.query(Raffler).all()

# Create a dictionary mapping account names to Raffle objects
rafflers_dict = {raffler.wallet: raffler for raffler in rafflers}

# Insert the df_raffles DataFrame into the raffles table
raffles = [Raffle(
    account=row['account'],
    dt_start=row['dt_start'],
    host_wallet=row['host_wallet'],
    host_id=rafflers_dict.get(row.host_wallet).id,
    nft_mint=row['nft_mint']
) for _, row in df_raffles.iterrows()]

print(raffles)  # Add this line to check if the Raffle instances are being properly created

session.bulk_save_objects(raffles)
session.commit()

# Query all existing Raffle instances and create a dictionary with account as the key
raffles = session.query(Raffle).all()

# Create a dictionary mapping account names to Raffle objects
raffles_dict = {raffle.account: raffle for raffle in raffles}

# Create a list of Buy instances with the appropriate Raffle relationship
buys = [Buy(
    account=row.account,
    dt_buy=row.dt_buy,
    amt_buy=row.amt_buy,
    buyer_wallet=row.buyer_wallet,
    raffle_id=raffles_dict.get(row.account).id,
    buyer_id=rafflers_dict.get(row.buyer_wallet).id
) for row in df_buys.itertuples(index=False)]

print(buys)  # Add this line to check if the Raffle instances are being properly created

# Bulk insert the Buy instances
session.bulk_save_objects(buys)
session.commit()

# Create a list of Cancel instances with the appropriate Raffle relationship
cancels = [Cancel(
    account=row.account,
    dt_cancel=row.dt_cancel,
    raffle_id=raffles_dict.get(row.account).id
) for row in df_cancels.itertuples(index=False)]

print(cancels)  # Add this line to check if the Cancel instances are being properly created

# Bulk insert the Cancel instances
session.bulk_save_objects(cancels)
session.commit()

filt = df_wins.account.isin(df_raffles.account)
df_wins = df_wins.loc[filt]

# Create a list of Winner instances with the appropriate Raffle relationship
wins = [Winner(
    account=row.account,
    raffle_id=raffles_dict.get(row.account).id,
    dt_win=row.dt_win,
    winner_wallet=row.winner_wallet,
    winner_id=rafflers_dict.get(row.winner_wallet).id
) for row in df_wins.itertuples(index=False)]

print(wins)  # Add this line to check if the Winner instances are being properly created

# Bulk insert the Winner instances
session.bulk_save_objects(wins)
session.commit()

filt = df_ends.account.isin(df_raffles.account)
df_ends = df_ends.loc[filt]

# Create a list of Endings instances with the appropriate Raffle relationship
ends = [End(
    account=row.account,
    raffle_id=raffles_dict.get(row.account).id,
    dt_end=row.dt_end
) for row in df_ends.itertuples(index=False)]

print(ends)  # Add this line to check if the End instances are being properly created

# Bulk insert the End instances
session.bulk_save_objects(ends)
session.commit()

# close session
# session.close()
