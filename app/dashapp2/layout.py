# from data import GetExistingFromDB
from dash import dcc
from dash import dash_table
from dash import html
from dash import ctx
from datetime import datetime as dt
from dash.dependencies import Input
from dash.dependencies import Output
import pandas_dash
import dash_bootstrap_components as dbc
from app.dashapp2.data import get_data, create_table, create_tab

# query = '''select * from data_overview'''

df = get_data()
data, columns = df.dash.to_dash_table()

#id='button-refresh'

counts_table = create_table('counts', data, columns)
counts_tab = create_tab(counts_table, 'Data Summary', 'data_counts')

table_tabs = dcc.Tabs(
    [counts_tab],
    className='tabs-container',
    id='table-tabs',
    value='data_counts'  # active tab
)

from app.extensions import top_bar

layout = dbc.Container(
[
        html.Div(top_bar),
        dbc.Button('Update Data', n_clicks=0, id='update-overview-data-btn'),
        html.Div(dash_table.DataTable(data=data, columns=columns)),
        dcc.Interval(
            id='interval-component',
            interval=1 * 1000, # in milliseconds,
            n_intervals=0
        ),
]

        )

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
# df = GetExistingFromDB(query=query)
