import os
import pandas as pd
import connectorx as cx

from config import Config

from dotenv import load_dotenv
from os.path import join, basename, dirname, abspath

basedir = abspath(dirname(__file__))

# dotenv_path = join(basedir, '.env')
# load_dotenv(dotenv_path)


def OpenSQL(filename):
    queries_path = join(basedir, 'queries')
    filename = join(queries_path, filename) + '.sql'
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()
    return sqlFile


def GetExistingFromDB(filename):
    query = OpenSQL(filename)
    df = cx.read_sql(conn=Config.SQLALCHEMY_DATABASE_URI, query=query, return_type="pandas")
    return df