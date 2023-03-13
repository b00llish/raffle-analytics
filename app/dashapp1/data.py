import connectorx as cx
import pandas as pd
from config import Config

def getdata():
    # get data and keep relevant columns
    # query='''SELECT * FROM fact_buys b LEFT JOIN fact_raffles r on b.raffle_id = r.raffle_id'''
    query = '''
                SELECT amount_buy, buyer_name, host_name, buyer_dao_status, host_dao_status 
                FROM fact_buys
                -- WHERE buyer_dao_status != 'amateur/non-dao' 
                --  AND buyer_dao_status is not null
    ''' ### CANT FILTER IN QUERY AND STILL GET TOTAL SELL VOLUME
    data = cx.read_sql(conn=Config.QUERY_DATABASE_URI, query=query, return_type="pandas")
    result = pd.concat([
        data.groupby(['buyer_name', 'buyer_dao_status']).agg({
            'amount_buy': [('buy_volume', 'sum'), ]
        }),
        data.groupby(['host_name', 'host_dao_status']).agg({
            'amount_buy': [('sell_volume', 'sum'), ]
        })
   ], axis=1).fillna(0)

    # adjust columns & index
    result.columns = result.columns.droplevel()
    result.reset_index(inplace=True)
    result.rename(columns={
        'level_0': 'name', 'level_1': 'status'
    }, inplace=True)

    # filter by status - may remove this later to make it optional
    result = result[result.status != 'amateur/non-dao']
    result = result[result.status != 'unlinked']
    result = result[~result.status.isnull()]
    #
    # # calculate buy volume
    # buy_volume = data.groupby(['buyer_name', 'buyer_dao_status']).agg({
    #             'amount_buy': [('buy_volume', 'sum'),]
    #              })
    # buy_volume.columns = buy_volume.columns.droplevel()
    #
    # # calculate sell volume
    # sell_volume = data.groupby('host_name').agg({
    #             'amount_buy': [('sell_volume', 'sum'),
    #              ]})
    # sell_volume.columns = sell_volume.columns.droplevel()
    #
    # # create status dict
    # status = data.loc[:, ['host_name', 'host_dao_status']].drop_duplicates().set_index('host_name')
    # status.rename(columns={'host_name':'name'})
    # status = status.to_dict()
    #
    # # combine outputs into result
    # result = pd.concat([buy_volume, sell_volume], axis=1).fillna(0)
    # result.reset_index(inplace=True)
    # result.rename(columns={'index':'name'}, inplace=True)
    # result['status'] = result.name.map(status['host_dao_status'])
    #
    # # filter by status
    # result = result[result.status != 'amateur/non-dao']
    # result = result[~result.status.isnull()]

    return result
