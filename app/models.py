from __future__ import annotations
# from flask_login import UserMixin
# from werkzeug.security import check_password_hash
# from werkzeug.security import generate_password_hash

from app.extensions import db
# from app.extensions import login
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
from sqlalchemy_utils import URLType
from sqlalchemy import create_engine
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
from app.materialized_view_factory import create_mat_view, MaterializedView


class Raffler(db.Model):
    __tablename__ = 'rafflers'

    id = db.Column(db.Integer, Sequence('rafflers_id_seq'), primary_key=True, index=True, unique=True, nullable=False)
    wallet = db.Column(db.String(45))
    twitter = db.Column(db.String(125))
    dao_status = db.Column(db.String(45))

    hosts = relationship('Raffle', backref='raffler', lazy='dynamic')
    buyers = relationship('Buy', backref='raffler', lazy='dynamic')
    winners = relationship('Winner', backref='raffler', lazy='dynamic')

    def __init__(self, wallet, twitter, dao_status):
        self.wallet = wallet
        self.twitter = twitter
        self.dao_status = dao_status

    def __repr__(self):
        return f"Raffler(id={self.id}, wallet='{self.wallet}', twitter='{self.twitter}', " \
               f"dao_status='{self.dao_status}')"


class Raffle(db.Model):
    __tablename__ = 'raffles'

    id = db.Column(db.Integer, Sequence('raffles_id_seq'), primary_key=True, index=True, unique=True, nullable=False)
    account = db.Column(db.String(45), index=True, unique=True, nullable=False)
    dt_start = db.Column(db.DateTime(timezone=True), nullable=False, index=True)
    host_wallet = db.Column(db.String(45))

    # Relationship
    nft_mint = db.Column(db.String(45))
    host_id = db.Column(db.Integer, db.ForeignKey('rafflers.id'), nullable=False)
    buyers = relationship('Buy', backref='raffle', lazy='dynamic')
    canceled = relationship('Cancel', backref='raffle', lazy='dynamic')
    ended = relationship('End', backref='raffle', lazy='dynamic')
    winner = relationship('Winner', backref='raffle', lazy='dynamic')

    def __init__(self, account, dt_start, host_wallet, nft_mint, host_id):
        self.account = account
        self.dt_start = dt_start
        self.host_wallet = host_wallet
        self.nft_mint = nft_mint
        self.host_id = host_id

    def __repr__(self):
        return f"Raffle(id={self.id}, account='{self.account}', dt_start='{self.dt_start}', " \
               f"host_wallet='{self.host_wallet}', nft_mint='{self.nft_mint}')"


class Buy(db.Model):
    __tablename__ = 'buys'

    id = db.Column(db.Integer, Sequence('buys_id_seq'), primary_key=True)
    dt_buy = db.Column(db.DateTime(timezone=True), nullable=False, index=True)
    buyer_wallet = db.Column(db.String(45), nullable=False, index=True)
    account = db.Column(db.String(45), nullable=False, index=True)
    amt_buy = db.Column(db.Float, nullable=False)

    # Relationship
    raffle_id = db.Column(db.Integer, db.ForeignKey('raffles.id'), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('rafflers.id'), nullable=True)

    __table_args__ = (db.UniqueConstraint(
        'dt_buy', 'amt_buy', 'account', 'buyer_wallet', 'raffle_id',
        name='_buy_row_uc'),
    )

    def __init__(self, account, dt_buy, amt_buy, buyer_wallet, raffle_id, buyer_id):
        self.account = account
        self.dt_buy = dt_buy
        self.amt_buy = amt_buy
        self.buyer_wallet = buyer_wallet
        self.raffle_id = raffle_id
        self.buyer_id = buyer_id

    def __repr__(self):
        return f"<Buy(id={self.id}, account='{self.account}', dt_buy='{self.dt_buy}', " \
               f"amt_buy='{round(self.amt_buy, 2)}', buyer_wallet='{self.buyer_wallet}', " \
               f"raffle_id={self.raffle_id})>"


class Cancel(db.Model):
    __tablename__ = 'cancels'

    id = db.Column(db.Integer, Sequence('cancels_id_seq'), primary_key=True)
    dt_cancel = db.Column(db.DateTime(timezone=True), nullable=False)
    account = db.Column(db.String(45), nullable=False, index=True)

    # Relationship
    raffle_id = db.Column(db.Integer, db.ForeignKey('raffles.id'), nullable=False)

    def __init__(self, account, dt_cancel, raffle_id):
        self.account = account
        self.dt_cancel = dt_cancel
        self.raffle_id = raffle_id

    def __repr__(self):
        return f"<Cancel(id={self.id}, account='{self.account}'," \
               f" dt_cancel='{self.dt_cancel}', raffle_id={self.raffle_id})>"


class End(db.Model):
    __tablename__ = 'endings'

    id = db.Column(db.Integer, Sequence('endings_id_seq'), primary_key=True)
    dt_end = db.Column(db.DateTime(timezone=True), nullable=False)
    account = db.Column(db.String(45), nullable=False, index=True)

    # Relationship
    raffle_id = db.Column(db.Integer, db.ForeignKey('raffles.id'), nullable=False)

    def __init__(self, account, dt_end, raffle_id):
        self.account = account
        self.dt_end = dt_end
        self.raffle_id = raffle_id

    def __repr__(self):
        return f"End(id={self.id}, account='{self.account}', " \
               f"dt_end='{self.dt_end}', raffle_id={self.raffle_id})"


class Winner(db.Model):
    __tablename__ = 'winners'

    id = db.Column(db.Integer, Sequence('winners_id_seq'), primary_key=True)
    dt_win = db.Column(db.DateTime(timezone=True), nullable=False)
    account = db.Column(db.String(45), nullable=False, index=True)
    winner_wallet = db.Column(db.String(45), nullable=False, index=True)

    # Relationship
    raffle_id = db.Column(db.Integer, db.ForeignKey('raffles.id'), nullable=False)
    winner_id = db.Column(db.Integer, db.ForeignKey('rafflers.id'), nullable=True)

    def __init__(self, winner_wallet, account, dt_win, raffle_id, winner_id):
        self.account = account
        self.dt_win = dt_win
        self.winner_wallet = winner_wallet
        self.raffle_id = raffle_id
        self.winner_id = winner_id

    def __repr__(self):
        return f"Winner(id={self.id}, account='{self.account}', wallet='{self.winner_wallet}', " \
               f"dt_win='{self.dt_win}', raffle_id={self.raffle_id})"


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
    id = db.Column(db.Integer, Sequence('collections_id_seq'))
    def __init__(self, collection_name, collection_alias, collection_proper_name):
        self.collection_name = collection_name
        self.collection_alias = collection_alias
        self.collection_proper_name = collection_proper_name

    def __repr__(self):
        return 'Collection {} also goes by alias {} its Magic Eden ID is: {}.'.format(
            self.collection_proper_name, self.collection_alias, self.collection_name
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

class DataOverview(MaterializedView):
    __table__ = create_mat_view("data_overview",
                                db.select(
                                    db.func.date_trunc('day', Raffle.dt_start),
                                    db.func.count(db.func.distinct(Raffle.account)),  # .label('raffle_count')
                                ).select_from(Raffle
                                    # db.join(Raffle, Buy, isouter=True))

                                ).group_by(db.func.date_trunc('day', Raffle.dt_start)))# .label('date'))

# db.Index('data_overview_date_idx', db.func.date_trunc('day', Raffle.dt_start), unique=True)

# db.Index('gear_item_mv_id_idx', GearItemMV.id, unique=True)
    # = create_mat_view("gear_item_mv",
    #                   db.select(
    #                       [GearItem.id.label('id'),
    #                        db.func.count(GearReview.id).label('review_count'),
    #                        db.func.avg(GearReview.rating).label('review_rating'), ]
    #                   ).select_from(db.join(GearItem, GearReview, isouter=True)
    #                                 ).group_by(GearItem.id))
    # class RaffleMetrics(db.Model):
    #     __table__ = db.Table(
    #         'raffle_metrics',
    #         db.Column('date', db.Date, primary_key=True),
    #         db.Column('raffle_count', db.Integer, nullable=False),
    #         db.Column('raffles_net_cancels', db.Integer, nullable=False),
    #         db.Column('raffles_bought_count', db.Integer, nullable=False),
    #         db.Column('cancels_count', db.Integer, nullable=False),
    #         db.Column('ends_count', db.Integer, nullable=False),
    #         db.Column('wins_count', db.Integer, nullable=False),
    #         schema='public',
    #         autoload=True,
    #         autoload_with=db.engine,
    #         extend_existing=True,
    #     )
