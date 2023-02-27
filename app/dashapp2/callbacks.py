import os
import pandas as pd
import connectorx as cx
import dash
from dash import dcc
from datetime import datetime as dt

import pandas_datareader as pdr
from dash.dependencies import Input
from dash.dependencies import Output

dt_begin = '2023-02-15'

def create_tab(content, label, value):
        return dash.dcc.Tab(
                content,
                label=label,
                value=value,
                id=f'{value}-tab',
                className='single-tab',
                selected_className='single-tab--selected'
        )
used_columns = [
        'dt_start', 'dt_end', 'collection', 'name', 'host_name',
        'host_status', 'winner_name', 'winner_status'
                ]
query = f'''
            SELECT 
                *
            FROM fact_raffles r
            where 
                r.dt_end >= '{dt_begin}'
            AND r.dt_end is not null
        '''

def register_callbacks(dashapp):
    @dashapp.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value')])
    def update_graph(selected_dropdown_value):
        df = pdr.get_data_yahoo(selected_dropdown_value, start=dt(2017, 1, 1), end=dt.now())
        return {
            'data': [{
                'x': df.index,
                'y': df.Close
            }],
            'layout': {'margin': {'l': 40, 'r': 0, 't': 20, 'b': 30}}
        }