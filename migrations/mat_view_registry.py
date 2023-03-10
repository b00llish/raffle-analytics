# my_view.py
from alembic_utils.pg_materialized_view import PGMaterializedView
from app.models import DataOverview_name, DataOverview_selectable
from app.models import FactRaffles_name, FactRaffles_selectable
from app.models import FactBuys_name, FactBuys_selectable
from app.models import TotalSales_name, TotalSales_selectable

data_overview_query_string = str(DataOverview_selectable.compile(compile_kwargs={"literal_binds": True}))

mv_data_overview = PGMaterializedView(
    schema="public",
    signature=DataOverview_name,
    definition=data_overview_query_string,
)

fact_raffles_query_string = str(FactRaffles_selectable.compile(compile_kwargs={"literal_binds": True}))

mv_fact_raffles = PGMaterializedView(
    schema="public",
    signature=FactRaffles_name,
    definition=fact_raffles_query_string,
)

total_sales_query_string = str(TotalSales_selectable.compile(compile_kwargs={"literal_binds": True}))

mv_total_sales = PGMaterializedView(
    schema="public",
    signature=TotalSales_name,
    definition=total_sales_query_string,
)

fact_buys_query_string = str(FactBuys_selectable.compile(compile_kwargs={"literal_binds": True}))

mv_fact_buys = PGMaterializedView(
    schema="public",
    signature=FactBuys_name,
    definition=fact_buys_query_string,
)
