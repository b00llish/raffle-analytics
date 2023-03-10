import pandas as pd
import dash
from dash import ctx
from datetime import datetime as dt
from dash.dependencies import Input
from dash.dependencies import Output
from app.dashapp2.data import get_data
import json
from dash import html
from dash import dcc

def register_callbacks(dashapp):
    @dashapp.callback(
        Output('counts-table', 'data'),
        # Output('my-output', 'children'),
        Input('update-overview-data-btn', 'n_clicks')
    )
    def update_graph(n):
        # ctx_msg = json.dumps({
        #     'states': ctx.states,
        #     'triggered': ctx.triggered,
        #     'inputs': ctx.inputs
        # }, indent=2)
        # if ctx.triggered_id == 'update-overview-data-btn':
        new_data = get_data()
        # new_data.sort_values('date', ascending=True)
        # new_data = new_data[0]
        new_data, new_columns = new_data.dash.to_dash_table()
        return new_data# , html.Pre(ctx_msg)
    #
    # @dashapp.callback(
    #             Output('container-ctx-example','children'),
    #             Input('btn-1-ctx-example', 'n_clicks'),
    #             Input('btn-2-ctx-example', 'n_clicks'),
    #             Input('btn-3-ctx-example', 'n_clicks'),
    #             Input('update-overview-data-btn', 'n_clicks'))
    # def display(btn1, btn2, btn3, btn4):
    #     button_clicked = ctx.triggered_id
    #     ctx_msg = json.dumps({
    #         'states': ctx.states,
    #         'triggered': ctx.triggered,
    #         'inputs': ctx.inputs
    #     }, indent=2)
    #     return html.Div([
    #         dcc.Markdown(
    #             f'''You last clicked button with ID {button_clicked}
    #             ''' if button_clicked else '''You haven't clicked any button yet'''),
    #         html.Pre(ctx_msg)
    #     ],
    #
    #     )
