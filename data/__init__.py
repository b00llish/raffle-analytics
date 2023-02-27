import os
import pandas as pd
import connectorx as cx
from shroomdk import ShroomDK
from dotenv import load_dotenv

load_dotenv()

sdk = ShroomDK(os.environ.get('SHROOM_KEY_1'))
os.path.basename(__file__)

def OpenSQL(filename):
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()
    return sqlFile


def df_fromSQL(sqlFile):
    file = OpenSQL(sqlFile)
    query_result_set = sdk.query(file, ttl_minutes=10)
    df = pd.DataFrame.from_dict(query_result_set.records)
    return df


def GetExistingFromDB(filename):
    query = OpenSQL(filename)
    df = cx.read_sql(conn=os.environ.get('db_uri'), query=query, return_type="pandas")
    return df