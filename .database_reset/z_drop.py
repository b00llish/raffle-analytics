from app.models import Raffle, Buy
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from config import Config

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

with engine.begin() as connection:
    connection.execute('TRUNCATE TABLE buys CASCADE')
    connection.execute('TRUNCATE TABLE raffles CASCADE')

session = Session(bind=engine)
session.commit()
session.close()
