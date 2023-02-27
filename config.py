import os
from dotenv import load_dotenv, dotenv_values
from os.path import join, dirname, abspath

basedir = abspath(dirname(__file__))
dotenv_path = join(basedir, '.env')
load_dotenv(dotenv_path)

SECRET_KEY = os.environ.get("SECRET_KEY")


class Config:
    DEBUG = False
    DEVELOPMENT = False

    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ['SECRET_KEY']


class ProductionConfig(Config):
    pass


class StagingConfig(Config):
    DEBUG = True


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
