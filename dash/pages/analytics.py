from dash import  ( 
    Output, Input, callback,
    register_page 
)
import dash_mantine_components as dmc

register_page(__name__, path="/analytics")


layout = dmc.Box(
    children = [
        dmc.Title("Analytics Page")
    ]
)



