# from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from dash import html
import dash_bootstrap_components as dbc

db = SQLAlchemy()
migrate = Migrate()


# login = LoginManager()


def dash_topNav():
    nav_contents = [
        dbc.NavItem(dbc.NavLink("Volume Quadrant", href="/volume-quad"
                                , external_link=True
                                )
                    ),
        dbc.NavItem(dbc.NavLink("Admin - Data Overview", href="/admin-overview"
                                , external_link=True
                                )
                    ),
        dbc.NavItem(dbc.NavLink("Dead End (for now)", href="/"
                                , external_link=True
                                ),
                    class_name="me-auto",
                    ),
    ]
    brand = dbc.Col(dbc.NavbarBrand("Raffflytics", external_link=True,
                                    className="ms-2"), )
    nav = dbc.Nav(nav_contents, pills=True, class_name="w-100")

    top_bar = dbc.Navbar(
        dbc.Container(
            [
                html.A(
                    dbc.Row(
                        brand,
                        align="center",
                        className="g-0",
                    ),
                    href="/",
                    style={"textDecoration": "none"},
                ),
                dbc.Row(
                    [
                        dbc.NavbarToggler(id="navbar-toggler"),
                        dbc.Collapse([nav], id="navbar-collapse",
                                     is_open=False,
                                     navbar=True,)
                        ],
                    class_name="flex-grow-1",
                ),
            ],
            fluid=True,
        ),
        dark=True,
        color="dark",
    )

        # children=[brand, nav],
        # color="dark",
        # dark=True,
    return top_bar


top_bar = dash_topNav()
