from dash import Dash,  html, dcc, Output,Input, callback, page_container,  ALL, ctx, clientside_callback, ClientsideFunction
import dash_mantine_components as dmc
from dash_iconify import DashIconify

app = Dash(
     __name__, 
    #  external_scripts=[
    #     'https://code.highcharts.com/highcharts.js', 
    #     'http://code.highcharts.com/highcharts-more.js',
    # ],

)

server = app.server

app.layout = html.Div(
    children = [
		dmc.ActionIcon(
			DashIconify(icon="gravity-ui:play-fill", width=20),
			id = 'play-chart',
			size=50,
			variant="filled",
			color='blue',
			radius=50,
			ml ='40%'
            
        ),
        html.Div(id="container")
    ]
)

clientside_callback(
    ClientsideFunction(
        namespace='highcharts',
        function_name='packedbubble'
    ),
 Output("container", "children"),
 Input("play-chart", "n_clicks"),
)


if __name__ == '__main__':
	app.run_server(port=8070,  debug = True)