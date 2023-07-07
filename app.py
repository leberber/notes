
import dash_leaflet as dl
from dash import Dash, html, Input, Output, no_update
import psycopg 
con = psycopg.connect( host = 'localhost', user = 'postgres', dbname = 'postgres', port='5432', password='',
        keepalives=1, keepalives_idle= 60, keepalives_interval= 15, keepalives_count=5, autocommit= True)


import dash_mantine_components as dmc

def card(text):
    return dmc.Card(
    children=[
        dmc.CardSection(
            dmc.Image(
                src="https://images.unsplash.com/photo-1527004013197-933c4bb611b3?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=720&q=80",
                height=160,
            )
        ),
        dmc.Group(
            [
                dmc.Text(text, weight=500),
                dmc.Badge("On Sale", color="red", variant="light"),
            ],
            position="apart",
            mt="md",
            mb="xs",
        ),
        dmc.Text(
            "With Fjord Tours you can explore more of the magical fjord landscapes with tours and activities on and around the fjords of Norway",
            size="sm",
            color="dimmed",
        ),
        dmc.Button(
            "Book classic tour now",
            variant="light",
            color="blue",
            fullWidth=True,
            mt="md",
            radius="md",
        ),
    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    style={"width": 350},
)
# import psycopg 
# from sqlalchemy import create_engine 
# import geopandas as gpd
# from dash.exceptions import PreventUpdate
# import json
# from dash_extensions.javascript import arrow_function, assign,  Namespace

# cluster = Namespace("myNamespace", "cluster")
# point =  Namespace("myNamespace", "point")
# engine = create_engine('postgresql://localhost/postgres')

def fetch_json (sql:str):
    cur = con.cursor()
    sql = f"""
        SELECT json_build_object(
            'type', 'FeatureCollection',
            'features', json_agg(ST_AsGeoJSON(t.*)::json)
        )
        FROM (
       {sql}
            ) t;
        """
    cur.execute (sql) 
    
    return cur.fetchone()[0]

my_colors={
 'GVEC.net':'#ff66ff',
 'Vyve Broadband':'#ff0000',
 'Google Fiber':'#003366',
 'North State Communications':'#996633',
 'AT&T':'#ccff33',
 'No Tracked Competition':'#33ccff',
 'Sparklight':'#99ff66',
 'GVTC Communications':'#66ffff',
 'Grande':'#cc9900',
 'Frontier':'#ccccff',
 'Access Media 3':'#006600',
 'Verizon FWA':'#ff66ff'
 }

divs=[]
for x, y in my_colors.items():
    divs.append(html.Div(
        [
            html.Div(style={ 'display': 'inline-block', 'width': '10px', 'height': '10px', 'background-color': y, 'margin-right':'7px'}),
            html.Div(x,style={ 'display': 'inline-block', 'font-family':'Robato', 'font-size':'12px', 'color':'#52504a'}),
        ]
        ) )

basemaps = {
'Open Street Map' :  'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
'osm fr':'https://{s}.tile.openstreetmap.fr/osmfr/{z}/{x}/{y}.png',
'osm':'http://{s}.tile.osm.org/{z}/{x}/{y}.png',
'Dark no Labels' : 'https://{s}.basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}{r}.png',
'Dark with Labels': 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
'watercolor':'http://{s}.tile.stamen.com/watercolor/{z}/{x}/{y}.png',
'carto' :'https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_nolabels/{z}/{x}/{y}.png',
'mapbox light':  "https://api.mapbox.com/styles/v1/mapbox/light-v9/tiles/{z}/{x}/{y}{r}?access_token=pk.eyJ1IjoibHBlYXJzb24tbWFwcyIsImEiOiJjazRhZDh5djQwMnpuM2dud3RpbXp2MGNrIn0.ohZKBd1TFwW85VjKje4DAg",
'mapbox street':  "https://api.mapbox.com/styles/v1/mapbox/streets-v9/tiles/{z}/{x}/{y}{r}?access_token=pk.eyJ1IjoibHBlYXJzb24tbWFwcyIsImEiOiJjazRhZDh5djQwMnpuM2dud3RpbXp2MGNrIn0.ohZKBd1TFwW85VjKje4DAg",
'mapbox satellite':"https://api.mapbox.com/styles/v1/mapbox/satellite-streets-v9/tiles/{z}/{x}/{y}{r}?access_token=pk.eyJ1IjoibHBlYXJzb24tbWFwcyIsImEiOiJjazRhZDh5djQwMnpuM2dud3RpbXp2MGNrIn0.ohZKBd1TFwW85VjKje4DAg",
'test':'https://cartodb-basemaps-a.global.ssl.fastly.net/light_all/{z}/{x}/{y}@2x.png'
}


app = Dash(prevent_initial_callbacks=True, suppress_callback_exceptions=True)
app.layout = html.Div([
    dl.Map(
        id="map",
        style={'width': '100%', 'height': '100vh'},
        zoom=10,
        # maxZoom =13,  
        center =[36.6168, 3.98707],
        attributionControl=False,   
        
        children=[
            dl.LayersControl(
                [dl.BaseLayer(dl.TileLayer(url=key[1]),name=key[0], checked=key[0]== "osm") for key in basemaps.items()] +
                [
                    dl.Overlay(
                        dl.LayerGroup(
                                id="locations",   
                        ), name="competitors", 
                        checked=True
                    ),
                ]
            ),  
        ], 
    ),
    html.Div( divs,style={ "position": "fixed", "bottom": 10, "left": 10, 'z-index':'1000'})
   
])


@app.callback(
    Output("locations", "children"), 
     Input("map", "bounds"), 
     Input("map", "zoom"),
    
)
def map_click(bounds, zoom):
    print(zoom, bounds)
    bds = bounds[0][1], bounds[0][0], bounds[1][1],bounds[1][0],4326
    s= f'select * from doctors WHERE geometry && ST_MakeEnvelope{bds}'
    _json = fetch_json(s)

    # if zoom <= 13:
    #     return no_update
    # else:
    #     bds = bounds[0][1], bounds[0][0], bounds[1][1],bounds[1][0],4326
    #     if zoom > 17:

    #         sql=f"""SELECT pt, leadbichtrobnm FROM work_schema.hhp_pt WHERE pt && ST_MakeEnvelope{bds} """
    #     else:
    #         sql=f"""SELECT pt, leadbichtrobnm FROM work_schema.hhp_pt WHERE pt && ST_MakeEnvelope{bds} limit 100 """


    #     print("len data: ",len(data))
    #     data = data.to_json()
        
        # data = json.loads(data)

    return dl.GeoJSON(data=_json, id="doctors", children=[dl.Tooltip(id = 'tooltips')]), 

@app.callback(
        Output("tooltips", "children"), 
        Input("doctors", "hover_feature"),
        prevent_initial_call=True,
              )
def map_click(feature):
    # print(ctx.triggered)
    if feature == None:
        return ''
    # else:
    #     print(feature)
    return  card(feature['properties']['name'])


if __name__ == '__main__':
    app.run_server(debug=True, port = 8010)


