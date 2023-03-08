"""adding max dt

Revision ID: 1650ae512449
Revises: 62da305f69be
Create Date: 2023-03-06 21:42:09.185906

"""
from alembic import op
import sqlalchemy as sa
from alembic_utils.pg_materialized_view import PGMaterializedView
from sqlalchemy import text as sql_text

# revision identifiers, used by Alembic.
revision = '1650ae512449'
down_revision = '62da305f69be'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    public_data_overview = PGMaterializedView(
                schema="public",
                signature="data_overview",
                definition="SELECT date_trunc('day', raffles.dt_start) AS dt_start, max(raffles.dt_start) AS max_dt, count(distinct(raffles.account)) AS raffle_count, count(distinct(buys.account)) AS buy_count, count(distinct(cancels.account)) AS cancel_count, count(distinct(endings.account)) AS end_count, count(distinct(winners.account)) AS win_count, count(distinct(raffles.account)) - count(distinct(cancels.account)) AS raffles_net_cancels \nFROM raffles LEFT OUTER JOIN buys ON raffles.id = buys.raffle_id LEFT OUTER JOIN cancels ON raffles.id = cancels.raffle_id LEFT OUTER JOIN endings ON raffles.id = endings.raffle_id LEFT OUTER JOIN winners ON raffles.id = winners.raffle_id GROUP BY date_trunc('day', raffles.dt_start)",
                with_data=True
            )

    op.replace_entity(public_data_overview)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    public_data_overview = PGMaterializedView(
                schema="public",
                signature="data_overview",
                definition="SELECT date_trunc('day'::text, raffles.dt_start) AS dt_start,\n    count(DISTINCT raffles.account) AS raffle_count,\n    count(DISTINCT buys.account) AS buy_count,\n    count(DISTINCT cancels.account) AS cancel_count,\n    count(DISTINCT endings.account) AS end_count,\n    count(DISTINCT winners.account) AS win_count,\n    (count(DISTINCT raffles.account) - count(DISTINCT cancels.account)) AS raffles_net_cancels\n   FROM ((((raffles\n     LEFT JOIN buys ON ((raffles.id = buys.raffle_id)))\n     LEFT JOIN cancels ON ((raffles.id = cancels.raffle_id)))\n     LEFT JOIN endings ON ((raffles.id = endings.raffle_id)))\n     LEFT JOIN winners ON ((raffles.id = winners.raffle_id)))\n  GROUP BY (date_trunc('day'::text, raffles.dt_start))",
                with_data=True
            )

    op.replace_entity(public_data_overview)
    # ### end Alembic commands ###