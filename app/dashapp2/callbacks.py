import pandas as pd
import dash
from dash import ctx
from datetime import datetime as dt
from dash.dependencies import Input
from dash.dependencies import Output
from app.dashapp2.data import get_data


def register_callbacks(dashapp):
    @dashapp.callback(
        Output('counts-table', 'data'),
        Input('update-overview-data-btn', 'n_clicks')
    )
    def update_graph(x):
        print(x)
        if ctx.triggered_id == 'update-overview-data-btn':
            new_data = get_data()
            # new_data = new_data[0]

            return new_data
