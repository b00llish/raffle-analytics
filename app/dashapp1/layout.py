from dash import dcc
from dash import html as html


from app.extensions import top_bar
layout = html.Div(id='main', children=[
    html.Div(top_bar),
    html.H1('Dashboard'),
    html.Div([
        dcc.Input(
            id='num-multi',
            type='number',
            value=5
        ),
        html.Table([
            html.Tr([html.Td(['x', html.Sup(2)]), html.Td(id='square')]),
            html.Tr([html.Td(['x', html.Sup(3)]), html.Td(id='cube')]),
            html.Tr([html.Td([2, html.Sup('x')]), html.Td(id='twos')]),
            html.Tr([html.Td([3, html.Sup('x')]), html.Td(id='threes')]),
            html.Tr([html.Td(['x', html.Sup('x')]), html.Td(id='x^x')]),
        ]),
    ])


], style={'width': '500'})
