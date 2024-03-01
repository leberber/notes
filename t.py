from dash import Dash,  html, dcc, Output,Input, callback, page_container,  ALL, ctx
import dash_mantine_components as dmc


app = Dash(__name__)

server = app.server

tabs = dmc.Tabs(
    [
        dmc.TabsList(
            [
                dmc.Tab("Mergers and aquisitions", value="mergers"),
                dmc.Tab("Consolidated assets", value="consolidated"),
            ]
        ),
        dmc.TabsPanel("Mergers and aquisitions content", value="mergers"),
        dmc.TabsPanel("Consolidated assets content", value="consolidated"),
    ],
    color="red",
    # orientation="vertical",
    value = "mergers"
)

buttons = html.Div(
            children = [
                dmc.Button("Default button", color = 'dark_blue'),
                dmc.Button("Subtle button", variant="subtle", color = 'green'),
                dmc.Button("Gradient button", variant="gradient"),
            ]
	    )
style = {
    "border": f"1px solid {dmc.theme.DEFAULT_COLORS['indigo'][4]}",
    "textAlign": "center",
    "height": '100px'
}
grid1 = dmc.Grid(
    children=[
        dmc.Col(html.Div("First Graph", style=style),  md = 6, sm=12),
        dmc.Col(html.Div("Second Graph", style=style), md = 6, sm = 12),

    ],
)
grid2 = dmc.Grid(
    children=[
        dmc.Col(html.Div("Third Graph", style=style),  md = 6, sm=12),
        dmc.Col(html.Div("Fourth Graph", style=style), md = 6, sm = 12),

    ],
)



app.layout = dmc.MantineProvider(
    theme={
        "fontFamily": "'Inter', sans-serif, Roboto",
        "colors": {
             "dark_blue": ["#4A5468", "#465064", "#424C60", "#3E485B", "#3A4457", "#354053", "#313C4F", "#2D384A", "253042"],
             "green":     ["#96E4C0", "#80E1B4", "#6BDFA9", "#57DE9F", "#42DE95", "#2FDF8C", "#1EDE84", "#1FCB7B", "#20B972"],
             "light_blue":["#AFE3EA", "#98DCE5", "#82D7E2", "#6DD3E0", "#58CFDF", "#44CDDF", "#30CBE0", "#25C3D8", "#25B3C6"]
        }
    },
    children=[
        tabs,
	buttons,
	grid1,
	grid2,
	
    
    ]
)

if __name__ == '__main__':
	app.run_server(
          port=8070,  
          debug = True
          )
