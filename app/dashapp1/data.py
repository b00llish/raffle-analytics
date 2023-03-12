import connectorx as cx
import pandas as pd
from config import Config

def getdata():
    # get data and keep relevant columns
    query='''SELECT * FROM fact_buys b LEFT JOIN fact_raffles r on b.raffle_id = r.raffle_id'''
    data = cx.read_sql(conn=Config.QUERY_DATABASE_URI, query=query, return_type="pandas")

    # calculate buy volume
    buy_volume = data.groupby('buyer_name').agg({
                'amount_buy': [('buy_volume', 'sum'),]
                 })
    buy_volume.columns = buy_volume.columns.droplevel()

    # calculate sell volume
    sell_volume = data.groupby('host_name').agg({
                'amount_buy': [('sell_volume', 'sum'),
                 ]})
    sell_volume.columns = sell_volume.columns.droplevel()

    # create status dict
    status = data.loc[:, ['host_name', 'host_dao_status']].drop_duplicates().set_index('host_name')
    status.rename(columns={'host_name':'name'})
    status = status.to_dict()

    # combine outputs into result
    result = pd.concat([buy_volume, sell_volume], axis=1).fillna(0)
    result.reset_index(inplace=True)
    result.rename(columns={'index':'name'}, inplace=True)
    result['status'] = result.name.map(status['host_dao_status'])

    # filter by status
    result = result[result.status != 'amateur/non-dao']
    result = result[~result.status.isnull()]

    return result