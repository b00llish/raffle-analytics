"""adding index to fact_buys

Revision ID: f118ddad3d89
Revises: 7c1ecf9f1d0e
Create Date: 2023-03-10 14:45:29.205289

"""
from alembic import op
import sqlalchemy as sa
from alembic_utils.pg_function import PGFunction
from sqlalchemy import text as sql_text

# revision identifiers, used by Alembic.
revision = 'f118ddad3d89'
down_revision = '7c1ecf9f1d0e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    public_refresh_mv = PGFunction(
        schema="public",
        signature="refresh-mv()",
        definition='returns event_trigger\n LANGUAGE plpgsql\nAS $function$BEGIN\n    REFRESH MATERIALIZED VIEW CONCURRENTLY public.fact_buys WITH DATA;\n    REFRESH MATERIALIZED VIEW CONCURRENTLY public.data_overview WITH DATA;\n\tREFRESH MATERIALIZED VIEW CONCURRENTLY public.fact_raffles WITH DATA;\n\tREFRESH MATERIALIZED VIEW CONCURRENTLY public.total_Sales WITH DATA;\nEND;\n\n$function$'
    )
    op.drop_entity(public_refresh_mv)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    public_refresh_mv = PGFunction(
        schema="public",
        signature="refresh-mv()",
        definition='returns event_trigger\n LANGUAGE plpgsql\nAS $function$BEGIN\n    REFRESH MATERIALIZED VIEW CONCURRENTLY public.fact_buys WITH DATA;\n    REFRESH MATERIALIZED VIEW CONCURRENTLY public.data_overview WITH DATA;\n\tREFRESH MATERIALIZED VIEW CONCURRENTLY public.fact_raffles WITH DATA;\n\tREFRESH MATERIALIZED VIEW CONCURRENTLY public.total_Sales WITH DATA;\nEND;\n\n$function$'
    )
    op.create_entity(public_refresh_mv)

    # ### end Alembic commands ###