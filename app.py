import dash  # pip install dash
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components


app = dash.Dash(
    __name__, external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True
)

# for x in dash.page_registry.values():
#     print(x)

navbar = dbc.NavbarSimple(
    dbc.DropdownMenu(
        [
            dbc.DropdownMenuItem(page["name"], href=page["path"])
            for page in dash.page_registry.values()
            if page["module"] != "pages.not_found_404"
        ],
        nav=True,
        label="More Pages",
    ),
    brand="Salarios en el Futbol",
    color="primary",
    dark=True,
    className="mb-2",
)

app.layout = dbc.Container(html.Div([
    navbar, dash.page_container
]), fluid=True)

if __name__ == "__main__":
    app.run_server(debug=True)