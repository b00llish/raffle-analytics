import dash
import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask.helpers import get_root_path

import dash_bootstrap_components as dbc

# from app.nav import nav
# from flask_nav.elements import *
# from flask_nav.elements import Navbar, View
# from flask_login import login_required

from config import Config


def create_app():
    server = Flask(__name__)
    env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
    server.config.from_object(env_config)

    from app.dashapp1.layout import layout as layout1
    from app.dashapp1.callbacks import register_callbacks as register_callbacks1
    register_dashapp(server, 'Volume Quadrant', 'volume-quad', layout1, register_callbacks1)

    from app.dashapp2.layout import layout as layout2
    from app.dashapp2.callbacks import register_callbacks as register_callbacks2
    register_dashapp(server, 'Data Overview', 'admin-overview', layout2, register_callbacks2)

    register_extensions(server)
    register_blueprints(server)
    bootstrap = Bootstrap(server)

    return server


def register_dashapp(app, title, base_pathname, layout, register_callbacks_fun):
    # Meta tags for viewport responsiveness
    meta_viewport = {
        "name": "viewport",
        "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}

    my_dashapp = dash.Dash(__name__,
                           server=app,
                           url_base_pathname=f'/{base_pathname}/',
                           assets_folder=get_root_path(__name__) + f'/{base_pathname}/assets/',
                           meta_tags=[meta_viewport],
                           # external_stylesheets=[dbc.themes.BOOTSTRAP] # Default
                           external_stylesheets=[dbc.themes.LUX] # Bootswatch
                           # external_stylesheets=[dbc.themes.SKETCHY] # Bootswatch
                           )

    with app.app_context():
        my_dashapp.title = title
        my_dashapp.layout = layout
        register_callbacks_fun(my_dashapp)
    # _protect_dashviews(my_dashapp)


#
# def _protect_dashviews(dashapp):
#     for view_func in dashapp.server.view_functions:
#         if view_func.startswith(dashapp.config.url_base_pathname):
#             dashapp.server.view_functions[view_func] = login_required(
#                 dashapp.server.view_functions[view_func])
#
#
def register_extensions(server):
    from app.extensions import db
    # from app.extensions import login
    from app.extensions import migrate
    #
    db.init_app(server)


#     login.init_app(server)
#     login.login_view = 'main.login'
    migrate.init_app(server, db)
#
#
def register_blueprints(server):
    from app.webapp import server_bp

    server.register_blueprint(server_bp)
