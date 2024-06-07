
from dash import (
    html, dcc, Output, Input, callback, 
    register_page
)
import dash_mantine_components as dmc
from flask_login import current_user

register_page(__name__, path="/login_required")



def layout(**kwargs):
    if not current_user.is_authenticated:
        return html.Div(["Please ", dcc.Link("login", href="/login"), " to continue"])

    return dmc.Box(
        children =[
           'You have succesfully login'
        ]
    )


