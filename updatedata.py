from dash import Dash, dcc, html, Input, Output, callback, State
import dash_mantine_components as dmc
import dash_ag_grid as dag
import pandas as pd

app = Dash(__name__)

def scrape_data ():
    url = 'https://en.wikipedia.org/wiki/World_population'
    dfs = pd.read_html(url)[:2]
    return dfs
app.layout = html.Div(
    [
      dmc.Button("Update Data", id="update-data-drawer-button"),
      dmc.Drawer(
            title="Update data ",
            id="update-data-drawer",
            size="100%",
            zIndex=100,
            children = [
                html.Div(id ='alert-container'),
                dmc.Group(  
                    children= [
                        dmc.Button("Scrape Data", id="scrape-data", mr = 10) , 
                        dmc.Button("Scrape Data", id="write-data")
                    ]
                ),
                dmc.LoadingOverlay(
                    html.Div(id = 'check-scraped-data', style = {'height':'80vh'}),
                    loaderProps={"variant": "dots", "color": "orange", "size": "xl"},
                ),
            ]
        )
    ]
)


@callback(
    Output("check-scraped-data", "children"),
    Input("scrape-data", "n_clicks"),
    prevent_initial_call=True,
)
def display_color(color):
    dfs = scrape_data()
    tables = []
    for table in dfs:
        tables.append(
            dag.AgGrid(
                   style={"height": 500},
                    columnSize="responsiveSizeToFit",
                id="get-started-example-basic-df",
                rowData=table.to_dict("records"),
                columnDefs=[{"field": i} for i in table.columns],
            )
        )

    return html.Div(
        style = {'height':'80vh'}, 
        children =tables
        )

@callback(
    Output("alert-container", "children"),
    Input("write-data", "n_clicks"),
    prevent_initial_call=True,
)
def display_color(n):

    # dfs = scrape_data()
    # for df in dfs:
    #     df.to_csv('somename.csv')
 
    return  dmc.Alert(
                title="Data Written Succesfully!",
                duration=3000,
            )

@callback(
    Output("update-data-drawer", "opened"),
    Input("update-data-drawer-button", "n_clicks"),
    prevent_initial_call=True,
)
def toggle_drawer(n_clicks):
    return True



if __name__ == "__main__":
    app.run_server(debug=True)
