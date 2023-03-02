from __future__ import annotations
# from flask_login import UserMixin
# from werkzeug.security import check_password_hash
# from werkzeug.security import generate_password_hash

from app.extensions import db
# from app.extensions import login
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
from sqlalchemy_utils import URLType

from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy import Integer

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from typing import Optional

# db.Model(DeclarativeBase)
# class Base(DeclarativeBase):
#     pass


# @login.user_loader
# def load_user(id):
#     return User.query.get(int(id))
#
#
# class User(UserMixin, db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(64), index=True, unique=True)
#     password_hash = db.Column(db.String(128))
#
#     def set_password(self, password):
#         self.password_hash = generate_password_hash(password)
#
#     def check_password(self, password):
#         return check_password_hash(self.password_hash, password)
#
#     def __repr__(self):
#         return '<User {}>'.format(self.username)

from sqlalchemy.sql.schema import Sequence


class Raffle(db.Model):
    __tablename__ = 'raffles'

    id = db.Column(db.Integer, Sequence('raffles_id_seq'), primary_key=True, index=True, unique=True, nullable=False)
    account = db.Column(db.String(45), index=True, unique=True, nullable=False)
    dt_start = db.Column(db.DateTime(timezone=True), nullable=False, index=True)

    # Relationship
    host_wallet = db.Column(db.String(45))
    nft_mint = db.Column(db.String(45))

    buyers = relationship('Buy', backref='raffle', lazy='dynamic')

    def __init__(self, account, dt_start, host_wallet, nft_mint):
        self.account = account
        self.dt_start = dt_start
        self.host_wallet = host_wallet
        self.nft_mint = nft_mint

    def __repr__(self):
        return f"<Raffle(id={self.id}, account='{self.account}', dt_start='{self.dt_start}', " \
               f"host_wallet='{self.host_wallet}', nft_mint='{self.nft_mint}')>"

class Buy(db.Model):
    __tablename__ = 'buys'

    id = db.Column(db.Integer, Sequence('buys_id_seq'), primary_key=True)
    dt_buy = db.Column(db.DateTime(timezone=True), nullable=False, index=True)
    buyer_wallet = db.Column(db.String(45))
    account = db.Column(db.String(45), nullable=False, index=True)

    amt_buy = db.Column(db.Float, nullable=False)
    raffle_id = db.Column(db.Integer, db.ForeignKey('raffles.id'), nullable=False)

    __table_args__ = (db.UniqueConstraint(
        'dt_buy', 'amt_buy', 'account', 'buyer_wallet', 'raffle_id',
        name='_buy_row_uc'),
    )

    def __init__(self, account, dt_buy, amt_buy, buyer_wallet, raffle_id):
        self.account = account
        self.dt_buy = dt_buy
        self.amt_buy = amt_buy
        self.buyer_wallet = buyer_wallet
        self.raffle_id = raffle_id

    def __repr__(self):
        return f"<Buy(id={self.id}, account='{self.account}', dt_buy='{self.dt_buy}', " \
               f"amt_buy='{round(self.amt_buy, 2)}', buyer_wallet='{self.buyer_wallet}', " \
               f"raffle_id={self.raffle_id})>"



class Cancel(db.Model):
    __tablename__ = 'cancels'

    id = db.Column(db.Integer, Sequence('buys_id_seq'), primary_key=True)
    dt_cancel = db.Column(db.DateTime(timezone=True), nullable=False)

    # Relationship
    account = db.Column(db.String(45), db.ForeignKey('raffles.account'))

    # ID goes last

    def __init__(self, account, dt_cancel):
        self.account = account
        self.dt_cancel = dt_cancel

    def __repr__(self):
        return 'Raffle account {}, was canceled on {}.'.format(
            self.account, self.dt_cancel
        )

#
# class End(db.Model):
#     __tablename__ = 'endings'
#
#     # id = db.Column(db.Integer, primary_key=True)
#     dt_end = db.Column(db.DateTime(timezone=True), nullable=False)
#
#     # Relationship
#     account = db.Column(db.String(45), db.ForeignKey('raffles.account'))
#
#     # ID goes last
#     id = db.Column(db.Integer, primary_key=True)
#
#     def __init__(self, account, dt_end):
#         self.account = account
#         self.dt_end = dt_end
#
#     def __repr__(self):
#         return 'Raffle account {} ended on {}.'.format(
#             self.account, self.dt_end
#         )
#
#
# class Winner(db.Model):
#     __tablename__ = 'winners'
#
#     # id = db.Column(db.Integer, primary_key=True)
#     dt_win = db.Column(db.DateTime(timezone=True), nullable=False)
#
#     # Relationship
#     account = db.Column(db.String(45), db.ForeignKey('raffles.account'))
#     winner_wallet = db.Column(db.String(45), db.ForeignKey('rafflers.wallet'))
#     # ID goes last
#     id = db.Column(db.Integer, primary_key=True)
#
#     def __init__(self, wallet, account, dt_win):
#         self.account = account
#         self.dt_win = dt_win
#         self.wallet = wallet
#
#     def __repr__(self):
#         return 'Raffle account {} was won by wallet {} on {}.'.format(
#             self.account, self.wallet, self.dt_win
#         )
#
#
class NFT(db.Model):
    __tablename__ = 'nfts'

    nft_mint = db.Column(db.String(45), primary_key=True)
    name = db.Column(db.String(120))

    # Relationship
    collection = db.Column(db.String(45), db.ForeignKey('collections.collection_name'))

    def __init__(self, nft_mint, name, collection):
        self.nft_mint = nft_mint
        self.name = name
        self.collection = collection

    def __repr__(self):
        return '{} has mint address {} and belongs to collection: {}.'.format(
            self.name, self.nft_mint, self.collection
        )


class Collection(db.Model):
    __tablename__ = 'collections'

    collection_name = db.Column(db.String(45), primary_key=True)
    collection_alias = db.Column(db.String(45))
    collection_proper_name = db.Column(db.String(45))

    def __init__(self, collection_name, collection_alias, collection_proper_name):
        self.collection_name = collection_name
        self.collection_alias = collection_alias
        self.collection_proper_name = collection_proper_name

    def __repr__(self):
        return 'Collection {} also goes by alias {} its Magic Eden ID is: {}.'.format(
            self.collection_proper_name, self.collection_alias, self.collection_name
        )


class Raffler(db.Model):
    __tablename__ = 'rafflers'

    wallet = db.Column(db.String(45), primary_key=True)
    twitter = db.Column(db.String(45))
    dao_status = db.Column(db.String(45))

    def __init__(self, wallet, twitter, dao_status):
        self.wallet = wallet
        self.twitter = twitter
        self.dao_status = dao_status

    def __repr__(self):
        return 'Wallet {} belongs to {} whose DAO status is: {}.'.format(
            self.wallet, self.twitter, self.dao_status
        )


class Price(db.Model):
    __tablename__ = 'prices'

    # id = db.Column(db.Integer, primary_key=True)
    floor = db.Column(DOUBLE_PRECISION)
    dt_floor = db.Column(db.DateTime(timezone=True), nullable=False)

    # Relationship
    collection = db.Column(db.String(45), db.ForeignKey('collections.collection_name'))

    # ID goes last
    id = db.Column(db.Integer, primary_key=True)

    def __init__(self, floor, dt_floor, collection):
        self.floor = floor
        self.dt_floor = dt_floor
        self.collection = collection

    def __repr__(self):
        return 'Collection:{} had floor price {} on {}.'.format(
            self.floor, self.collection, self.dt_floor
        )

    class ScrapedRaffle(db.Model):
        __tablename__ = 'raffles_scraped'

        account = db.Column(db.String(45))
        collection_name = db.Column(db.String(100))
        me_link = db.Column(URLType)
        name = db.Column(db.String(100))
        floor = db.Column(db.String(45))  # TODO: update to float
        tkt_cost = db.Column(db.String(45))  # TODO: why cant tkt_cost be length 15
        tkt_price = db.Column(DOUBLE_PRECISION)
        tkt_token = db.Column(db.String(15))
        tkt_sold = db.Column(db.Integer)
        tkt_total = db.Column(db.Integer)
        raffler_twitter = db.Column(db.String(100))
        dt_start = db.Column(db.DateTime(timezone=True))
        status = db.Column(db.String(45))
        status_text = db.Column(db.String(45))
        dt_scraped = db.Column(db.DateTime(timezone=True), nullable=False)

        # calculated/generated go last
        dt_status = db.Column(db.DateTime(timezone=True))
        tkt_remaining = db.Column(db.Integer, db.Computed("tkt_total - tkt_sold"))
        total_sales = db.Column(DOUBLE_PRECISION, db.Computed("tkt_sold * tkt_price"))
        id = db.Column(db.Integer, primary_key=True)

        def __init__(self, floor, dt_floor, collection):
            self.floor = floor
            self.dt_floor = dt_floor
            self.collection = collection

        def __repr__(self):
            return 'Collection:{} had floor price {} on {}.'.format(
                self.floor, self.collection, self.dt_floor
            )
