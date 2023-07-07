import dash_mantine_components as dmc
from dash import Dash, Input, Output, html

from datetime import datetime


app = Dash(__name__)

app.layout = html.Div(
    [dmc.DatePicker(
    id="datepicker-error",
    value=datetime.now().date(),
    label="Date",
    required=True,
    clearable=False,
    style={"width": 200},
)
    ]
)


# @app.callback(Output("text", "children"), Input("datepicker", "date"))
# def datepicker(date):
#     return date





@app.callback(Output("datepicker-error", "error"), Input("datepicker-error", "value"))
def datepicker_error(date):
    day = datetime.strptime(date, "%Y-%M-%d").day
    return "Please select an even date." if day % 2 else ""



if __name__ == "__main__":
    app.run_server(debug=True)