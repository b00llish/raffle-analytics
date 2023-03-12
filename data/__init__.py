import os
import pandas as pd
import connectorx as cx
from config import Config
from os.path import join, basename, dirname, abspath
import requests

basedir = abspath(dirname(__file__))

# set file path
if basename(__file__) == '<input>':
    path_queries = join(basedir, 'data', 'queries')  # if pasting into pyConsole
else:
    path_queries = join(basedir, 'queries')  # if running as script


def OpenSQL(filename):
    queries_path = join(basedir, 'queries')
    filename = join(queries_path, filename) + '.sql'
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()
    return sqlFile


def GetExistingFromDB(filename=None, query=None):
    if not query:
        query = OpenSQL(filename)
    table = cx.read_sql(conn=Config.SQLALCHEMY_DATABASE_URI, query=query, return_type="arrow")
    df = table.to_pandas(split_blocks=False, date_as_object=False)
    return df


def _make_post_request(url, api_key, payload):
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {api_key}"
    }
    response = requests.post(url=url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError(f'Error: {response.status_code}: {response.content}')
