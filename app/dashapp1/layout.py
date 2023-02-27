# import dash_core_components as dcc
from dash import html as html


from app.extensions import top_bar
layout = html.Div(id='main', children=[
    html.Div(top_bar),
    html.H1('Dashboard')

], style={'width': '500'})
