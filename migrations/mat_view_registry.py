# my_view.py
from alembic_utils.pg_materialized_view import PGMaterializedView
from app.extensions import db
from app.models import Raffle
from app.models import DataOverview_name, DataOverview_selectable
# from app.materialized_view_factory import create_mat_view, MaterializedView

# copy query from models.py
data_overview_query = db.select(
                                db.func.date_trunc('day', Raffle.dt_start).label('start_date'),
                                db.func.count(db.func.distinct(Raffle.account)).label('raffle_count'),
                                ).select_from(Raffle
                                ).group_by(db.func.date_trunc('day', Raffle.dt_start))

data_overview_query_string = str(DataOverview_selectable.compile(compile_kwargs={"literal_binds": True}))

mv_data_overview = PGMaterializedView(
    schema="public",
    signature=DataOverview_name,
    definition=data_overview_query_string,
)
