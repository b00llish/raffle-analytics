# from flask_login import LoginManager
# from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import dash_bootstrap_components as dbc

db = SQLAlchemy()


# migrate = Migrate()
# login = LoginManager()


def dash_topNav():
    nav_contents = [
        dbc.NavItem(dbc.NavLink("Dashboard", href="/dashboard/", external_link=True)),
        dbc.NavItem(dbc.NavLink("Example", href="/example/")),
        dbc.NavItem(dbc.NavLink("Link", href="/", external_link=True)),
    ]
    brand = dbc.Col(dbc.NavbarBrand("Raffflytics", href="/"), )
    nav = dbc.Nav(nav_contents, pills=True)
    top_bar = dbc.NavbarSimple(
        children=[brand, nav],
        color="dark",
        dark=True,
    )
    return top_bar


top_bar = dash_topNav()
