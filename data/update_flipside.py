# from os import environ
from os.path import join, basename, dirname, abspath
import pandas as pd
from data import OpenSQL
from shroomdk import ShroomDK
from app.models import Raffler, Raffle, Buy, Cancel, End, Winner
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from config import Config
from data import GetExistingFromDB

sdk = ShroomDK(Config.SHROOM_KEY)
session = Session(bind=create_engine(Config.SQLALCHEMY_DATABASE_URI))

# open files
basedir = abspath(dirname(__file__))

# set file path
if basename(__file__) == '<input>':
    path = join(basedir, 'data', 'queries')  # if pasting into pyConsole
    print(path)
else:
    path = join(basedir, 'queries')  # if running as script
    print(path)


def df_fromSQL(sqlFile):
    file = OpenSQL(sqlFile)
    query_result_set = sdk.query(file, ttl_minutes=12)
    df = pd.DataFrame.from_dict(query_result_set.records)
    return df


# create dict for mapping
rafflers = session.query(Raffler).all()
rafflers_dict = {raffler.wallet: raffler for raffler in rafflers}
print('got rafflers dict')

# get new raffles
sqlFile = join(path, 'raffles_flipside')
print(sqlFile)
df_raffles = df_fromSQL(sqlFile=sqlFile)
print('got result from flipside')
df_raffles.dt_start = pd.to_datetime(df_raffles.dt_start).dt.tz_localize('UTC')
all_raffles = GetExistingFromDB(query='''select account from raffles''')
filt = df_raffles.account.isin(all_raffles.account)
df_raffles = df_raffles.loc[~filt]
print('got new raffles')
# get new buys
sqlFile = join(path, 'buys_flipside')
df_buys = df_fromSQL(sqlFile=sqlFile)
df_buys.dt_buy = pd.to_datetime(df_buys.dt_buy).dt.tz_localize('UTC')
all_buys = GetExistingFromDB(query='''select * from buys''')
all_buys.dt_buy = pd.to_datetime(all_buys.dt_buy).dt.tz_localize('UTC')
df_buys = pd.concat([df_buys, all_buys, all_buys])
# keep relevant columns
df_buys = df_buys[['dt_buy', 'buyer_wallet', 'account', 'amt_buy']]
# drop all dupes to prevent errors loading in to db
df_buys.drop_duplicates(keep=False, ignore_index=True, inplace=True)
print('got new buys')
# get new wins
sqlFile = join(path, 'wins_flipside')
df_wins = df_fromSQL(sqlFile=sqlFile)
df_wins.dt_win = pd.to_datetime(df_wins.dt_win).dt.tz_localize('UTC')
all_winners = GetExistingFromDB(query='''select account from winners''')
filt = df_wins.account.isin(all_winners.account)
df_wins = df_wins.loc[~filt]
print('got new wins')
# get new ends
sqlFile = join(path, 'ends_flipside')
df_ends = df_fromSQL(sqlFile=sqlFile)
df_ends.dt_end = pd.to_datetime(df_ends.dt_end).dt.tz_localize('UTC')
all_endings = GetExistingFromDB(query='''select account from endings''')
filt = df_ends.account.isin(all_endings.account)
df_ends = df_ends.loc[~filt]

# get new cancels
sqlFile = join(path, 'cancels_flipside')
df_cancels = df_fromSQL(sqlFile=sqlFile)
df_cancels.dt_cancel = pd.to_datetime(df_cancels.dt_cancel).dt.tz_localize('UTC')
all_cancels = GetExistingFromDB(query='''select account from cancels''')
filt = df_cancels.account.isin(all_cancels.account)
df_cancels = df_cancels.loc[~filt]
print('finished querying data')
# determine rafflers to add
all_rafflers = GetExistingFromDB(query='''select wallet from rafflers''')
new_rafflers = pd.concat([df_raffles.host_wallet, df_buys.buyer_wallet, df_wins.winner_wallet])
new_rafflers.drop_duplicates(inplace=True)
filt = new_rafflers.isin(all_rafflers.wallet)
new_rafflers = pd.DataFrame(new_rafflers.loc[~filt])

# add twitter and dao_status
new_rafflers['dao_status'] = 'amateur/non-dao'
new_rafflers['twitter'] = 'unlinked'
new_rafflers.rename(columns={0: 'wallet'}, inplace=True)
new_rafflers = new_rafflers[['wallet', 'twitter', 'dao_status']]

# insert new rafflers
rafflers = [Raffler(
    wallet=row['wallet'],
    twitter=row['twitter'],
    dao_status=row['dao_status']
) for _, row in new_rafflers.iterrows()]

# commit new rafflers
session.bulk_save_objects(rafflers)
session.commit()
print ('committed rafflers')
# create dict for mapping
rafflers = session.query(Raffler).all()
rafflers_dict = {raffler.wallet: raffler for raffler in rafflers}


# filt = df_raffles.host_wallet.isin(rafflers.wallet)

# insert new raffles
raffles = [Raffle(
    account=row['account'],
    dt_start=row['dt_start'],
    host_wallet=row['host_wallet'],
    host_id=rafflers_dict.get(row.host_wallet).id,
    nft_mint=row['nft_mint']
) for _, row in df_raffles.iterrows()]

# commit new raffles
session.bulk_save_objects(raffles)
session.commit()
print('committed raffles')
# create dict for mapping
raffles = session.query(Raffle).all()
raffles_dict = {raffle.account: raffle for raffle in raffles}

# get accounts for all raffles
all_raffles = GetExistingFromDB(query='''select account from raffles''')

# keep buys for raffles in db
df_buys = df_buys.loc[df_buys.account.isin(all_raffles.account)]

# insert new buys
buys = [Buy(
    account=row.account,
    dt_buy=row.dt_buy,
    amt_buy=row.amt_buy,
    buyer_wallet=row.buyer_wallet,
    raffle_id=raffles_dict.get(row.account).id,
    buyer_id=rafflers_dict.get(row.buyer_wallet).id
) for row in df_buys.itertuples(index=False)]

# save & commit
session.bulk_save_objects(buys)
session.commit()
print('committed buys')
# keep wins for raffles in db
df_wins = df_wins.loc[df_wins.account.isin(all_raffles.account)]

# insert new wins
wins = [Winner(
    account=row.account,
    raffle_id=raffles_dict.get(row.account).id,
    dt_win=row.dt_win,
    winner_wallet=row.winner_wallet,
    winner_id=rafflers_dict.get(row.winner_wallet).id
) for row in df_wins.itertuples(index=False)]

# save & commit
session.bulk_save_objects(wins)
session.commit()

# keep ends for raffles in db
df_cancels = df_cancels.loc[df_cancels.account.isin(all_raffles.account)]

# insert new cancels
cancels = [Cancel(
    account=row.account,
    dt_cancel=row.dt_cancel,
    raffle_id=raffles_dict.get(row.account).id
) for row in df_cancels.itertuples(index=False)]

# save & commit
session.bulk_save_objects(cancels)
session.commit()

# filter ends
df_ends = df_ends.loc[df_ends.account.isin(all_raffles.account)]

# insert new ends
ends = [End(
    account=row.account,
    raffle_id=raffles_dict.get(row.account).id,
    dt_end=row.dt_end
) for row in df_ends.itertuples(index=False)]

# save & commit
session.bulk_save_objects(ends)
session.commit()
print('committed all data')
# refresh materialized views
session.execute(text('''REFRESH MATERIALIZED VIEW CONCURRENTLY public.data_overview WITH DATA;'''))
print('refreshed mv: data overview')
session.execute(text('''REFRESH MATERIALIZED VIEW CONCURRENTLY public.fact_raffles WITH DATA;'''))
print('refreshed mv: fact_raffles')
session.execute(text('''REFRESH MATERIALIZED VIEW CONCURRENTLY public.total_sales WITH DATA;'''))
print('refreshed mv: total sales')
# close
session.close()
print('session closed')
