import os
from dotenv import load_dotenv
from os.path import join, dirname, abspath

basedir = abspath(dirname(__file__))
dotenv_path = join(basedir, '.env')
load_dotenv(dotenv_path)

MAINNET_BASE_URL = "https://rest-api.hellomoon.io/v0"
DEVNET_BASE_URL = ""


class Config(object):
    DEBUG = False
    DEVELOPMENT = False

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace(
        'postgres://', 'postgresql://')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ['SECRET_KEY']
    SHROOM_KEY = os.environ['SHROOM_KEY_1']
    QUERY_DATABASE_URI = os.environ.get('QUERY_URL', '').replace(
        'postgres://', 'postgresql://')
    UPDATE_DATABASE_URI = os.environ.get('UPDATE_URL', '').replace(
        'postgres://', 'postgresql://')
    HELLOMOON_API = os.environ['HELLO_MOON_KEY']


class ProductionConfig(Config):
    pass


class StagingConfig(Config):
    DEBUG = True


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
