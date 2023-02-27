import os
import pandas as pd
from data import OpenSQL
from shroomdk import ShroomDK

sdk = ShroomDK(os.environ.get('SHROOM_KEY_1'))

def df_fromSQL(sqlFile):
    file = OpenSQL(sqlFile)
    query_result_set = sdk.query(file, ttl_minutes=10)
    df = pd.DataFrame.from_dict(query_result_set.records)
    return df
