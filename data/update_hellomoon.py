import pandas as pd
from data.nft import NFT
from data import GetExistingFromDB
from config import Config
import requests

raffles = GetExistingFromDB(query="""select * from raffles where dt_start >= '3/8/2023' """)

# nft_mint = ['2GSMjN1f68q3pkfcKfSPDpJyPwD5ASYrC8TMccQAnvRg', '6voZnEjnDszYfZfvS7Wj3sEUxKEkdWALB4ERQtkBm4mM']
# mints = raffles.nft_mint
mint_list = list(raffles.nft_mint.unique())

result = NFT().collection_mint_mapping(mint_list, limit=len(mint_list))['data']
# x = result['data']
df = pd.DataFrame.from_records(result)

raffles2 = pd.merge(
    raffles,
    df,
    how='left',
    left_on='nft_mint',
    right_on='nftMint'
)
# r = raffles2.id.isin(raffles.id)
r = raffles2.duplicated(subset='id')
# r = raffles2.duplicated()
r = raffles2[r]
d = raffles2.loc[(raffles2.id.isin(r.id))]
#
# def get_mints(list, data, mint_list, start=False,):
#     payload = {"nftMint": mint_list, "limit": 1000}
#     headers = {
#         "accept": "application/json",
#         "content-type": "application/json",
#         "authorization": f"Bearer {Config.HELLOMOON_API}"
#     }
#     base = 'https://rest-api.hellomoon.io/v0'
#     path = "/nft/collection/mints"
#     url = base + path
#     if start:
#         response = requests.post(url, json=payload, headers=headers)
#         data = response.json()
#         list.extend(data['data'])
#         return get_mints(list, data)
#     elif 'paginationToken' in data:
#         payload['paginationToken'] = data['paginationToken']
#         response = requests.post(url, json=payload, headers=headers)
#         data = response.json()
#         list.extend(data['data'])
#         return get_mints(list, data)
#     else:
#         return list
# list = []
# data = []
#
# list = get_mints([], [], mint_list, start=True)
#
# print(f"found {len(list)} mints")
# print(f"first mint example {list[0]}")
#
# coll_ids = df.helloMoonCollectionId.unique()
# ids_list = list(coll_ids)
