import pandas as pd
from data.nft import NFT
from data import GetExistingFromDB

raffles = GetExistingFromDB(query="""select * from raffles where dt_start >= '3/10/2023' """)

mint_list = list(raffles.nft_mint.unique())

result = NFT().collection_mint_mapping(mint_list, limit=len(mint_list))['data']
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
