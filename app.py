from dash import Dash, callback, html, dcc
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import matplotlib as mpl
import gunicorn
from whitenoise import WhiteNoise

# Instantiate dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

# Reference the underlying flask app (Used by gunicorn webserver in Heroku production deployment)
server = app.server

# Enable Whitenoise for serving static files from Heroku (the /static folder is seen as root by Heroku)
server.wsgi_app = WhiteNoise(server.wsgi_app, root='static/')

def create_dash_layout(app):
    # Set browser tab title
    app.title = "Rafffle Analytics"

    # Header
    header = html.Div([html.Br(), dcc.Markdown(
        """ # Rafffle Analytics - Built with Dash."""
    ),
                       html.Br()
                       ])

    # Body
    body = html.Div([
        dcc.Markdown(""" ## This is the body """), html.Br()
    ])

    # Footer
    footer = html.Div([html.Br(), html.Br(), dcc.Markdown(
        """ This is a footer """
    )])

    # Assemble dash layout
    app.layout = html.Div([header, body, footer])

    return app

# Construct the dash layout
create_dash_layout(app)

# Run flask app
if __name__ == "__main__": app.run_server(debug=False, host='0.0.0.0', port=8050)