from dash.dependencies import Input, Output


def register_callbacks(dashapp):
    @dashapp.callback(
        Output('square', 'children'),
        Output('cube', 'children'),
        Output('twos', 'children'),
        Output('threes', 'children'),
        Output('x^x', 'children'),
        Input('num-multi', 'value'))
    def callback_a(x):
        return x ** 2, x ** 3, 2 ** x, 3 ** x, x ** x
