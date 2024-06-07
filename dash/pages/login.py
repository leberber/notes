import dash
from dash import html, dcc
from pages.utils import iconify
import dash_mantine_components as dmc 

dash.register_page(__name__)


layout = html.Form(
    [
        html.H2("Please log in to continue:", id="h1"),
        html.Div(
            [
       dcc.Input(placeholder="Enter your username", type="text", id="uname-box", name='username'),
        dcc.Input(placeholder="Enter your password", type="password", id="pwd-box", name='password'),
            ]
        ),
 
        html.Button(children="Login", n_clicks=0, type="submit", id="login-button"),
        html.Div(children="", id="output-state")
    ], method='POST'
)