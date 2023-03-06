import pandas as pd
import connectorx as cx
from sqlalchemy import create_engine
from config import Config

# indiv = 'tanrikulu_onur'
indiv = 'AFK_Sol'
# indiv = 'b00llish'
# 'mjbreese613'

# buy_hist = 'rafffle_buying_history'
# df_buy = pd.read_pickle(buy_hist)

# retrieve data
# connection = sqlite3.connect('rafffle_data.db')
query = f'''
                SELECT * 
                FROM fact_buys b 
                WHERE 
                    b.buyer_name = '{indiv}'
            '''
# my_buys = pd.read_sql(buys_query, connection, parse_dates='dt_buy')
my_buys = cx.read_sql(conn=Config.SQLALCHEMY_DATABASE_URI, query=query, return_type="pandas")

query = f''' SELECT * FROM fact_buys WHERE host_name = '{indiv}' '''
# my_buyers = pd.read_sql(buyers_query, connection, parse_dates='dt_buy')
my_buyers = cx.read_sql(conn=Config.SQLALCHEMY_DATABASE_URI, query=query, return_type="pandas")

# connection.close()
# my_buys = df_buy.loc[(df_buy['BUYER_NAME'] == indiv)].sort_values(by='DATE_BUY')
# my_buyers = df_buy.loc[(df_buy['HOST_NAME'] == indiv)].sort_values(by='DATE_BUY')
my_buys.dt_buy = my_buys.dt_buy.dt.tz_localize(None)
my_buyers.dt_buy = my_buyers.dt_buy.dt.tz_localize(None)

mb = (
    my_buys.groupby(
        ['buyer_name', 'host_name', pd.Grouper(
            key='dt_buy',
            freq='D',
            closed='right',
            label='right',
            sort='true',
            axis=0
        )]
    )['amt_buy']
    .sum()
    .unstack()
    .fillna(0)
)
mb = mb.reindex(sorted(mb.columns), axis=1)
#mb = mb.columns.dt.tz_localize(tz=None)
mb.loc[('column_total', ''), :] = mb.sum(axis=0)
mb.loc[:,'row_total'] = mb.sum(axis=1)
print(mb)

ms = (
    my_buyers.groupby(
        ['buyer_name', 'host_name', pd.Grouper(
            key='dt_buy',
            freq='D',
            closed='right',
            label='right',
            sort='true',
            axis=0
        )]
    )['amt_buy']
    .sum()
    .unstack()
    .fillna(0)
)
ms = ms.reindex(sorted(ms.columns), axis=1)
ms.loc[('column_total', ''), :] = ms.sum(axis=0)
ms.loc[:,'row_total'] = ms.sum(axis=1)
print(ms)

# mb.to_csv('indiv_activity_b00llish-mb2023.02.02.csv')
# ms.to_csv('indiv_activity_b00llish-ms-2023.02.02.csv')
max_dt = max(my_buys.dt_buy)
max_dt = max_dt.strftime('%Y.%m.%d')
writer = pd.ExcelWriter(f'indiv_activity_{indiv}-{max_dt}.xlsx', engine='xlsxwriter')
mb.to_excel(writer, sheet_name='mb')
ms.to_excel(writer, sheet_name='ms')
writer.close()