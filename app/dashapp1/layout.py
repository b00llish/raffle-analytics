from dash import dcc
from dash import html as html
from app.extensions import top_bar
from app.dashapp1.data import getdata
import plotly.graph_objects as go

r = getdata()
x = r.sell_volume
y = r.buy_volume
text = r.name

fig = go.Figure()
fig.add_scatter(
    x=x,
    y=y,
    text=text,
    mode='text'
)
fig.update_layout(
        title='Buy/Sell Volume (DAO members only)',
        xaxis_title='Sell Volume',
        yaxis_title='Buy Volume',
        # autosize=True,
        height=700,
)


layout = html.Div(id='main', children=[
    html.Div(top_bar),
    # html.Br(),
    # html.H1('Buy/Sell Volume'),
    html.Br(),
    # html.Div([
    #     dcc.Input(
    #         id='num-multi',
    #         type='number',
    #         value=5
    #     ),
    #     html.Table([
    #         html.Tr([html.Td(['x', html.Sup(2)]), html.Td(id='square')]),
    #         html.Tr([html.Td(['x', html.Sup(3)]), html.Td(id='cube')]),
    #         html.Tr([html.Td([2, html.Sup('x')]), html.Td(id='twos')]),
    #         html.Tr([html.Td([3, html.Sup('x')]), html.Td(id='threes')]),
    #         html.Tr([html.Td(['x', html.Sup('x')]), html.Td(id='x^x')]),
    #     ]),
    # ]),
    html.Div([
        dcc.Graph(
            id='volume-quad',
            figure=fig,
            config={
                'autosizable': True,
                'responsive': True,
                'fillframe': True
            }
        )
    ]#, style={'height': '750'}
    )

], style={'width': '500'})
