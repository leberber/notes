
import dash_leaflet as dl
from dash import Dash, html, Input, Output, ctx
from connection import get_postgis
from dash.exceptions import PreventUpdate
import json
from dash_extensions.javascript import arrow_function, assign,  Namespace
import dash_bootstrap_components as dbc
cluster = Namespace("myNamespace", "cluster")
point =  Namespace("myNamespace", "point")

my_colors={
 'GIG':'#e32214',
 'NONE GIG':'#1a1919',
 }

 

external_scripts = [
    'https://www.google-analytics.com/analytics.js',
    {'src': 'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.4/Chart.js'},
    {
        'src': 'https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.10/lodash.core.js',
        'integrity': 'sha256-Qqd/EfdABZUcAxjOkMi8eGEivtdTkh3b65xCZL4qAQA=',
        'crossorigin': 'anonymous'
    }
]
divs=[]
for x, y in my_colors.items():
    divs.append(html.Div(
        [
            html.Div(style={ 'display': 'inline-block', 'width': '10px', 'height': '10px', 'backgroundColor': y, 'margin-right':'7px'}),
            html.Div(x,style={ 'display': 'inline-block', 'font-family':'Robato', 'fontSize':'12px', 'color':'#52504a', 'font-weight':'bold'}),
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




app = Dash(prevent_initial_callbacks=True, external_scripts=external_scripts, suppress_callback_exceptions=True)
app.layout = html.Div([
    dl.Map(
        id="map",
        style={'width': '100%', 'height': '100vh'},
        zoom=10,
        maxZoom =20,
        center =[32.779167, -96.808891],
        attributionControl=False,   
        
        children=[
            dl.LayersControl(
                [dl.BaseLayer(dl.TileLayer(url=key[1]),name=key[0], checked=key[0]== "mapbox street") for key in basemaps.items()] +
                [
                    dl.Overlay(
                        dl.LayerGroup(
                                id="locations",   
                        ), name="competitors", 
                        checked=True
                    ),
                        dl.Overlay(
                        dl.LayerGroup(
                                id="ST_ClusterDBSCAN",   
                        ), name="DBSCAN Cluster", 
                        checked=True
                    ),
                ]
            ),  
        ], 
    ),

    html.Div(id = 'zoomlevel', style={ 'zIndex': '1000', 'position': 'fixed', 'top':'20px', 'left':'60px', 'fontSize':'40px', 'color':'red', 'backgroundColor':'rgb(255, 255, 255, 0.8' }),
    html.Div(divs, style={'zIndex': '1000', "position": "fixed", "top": 100, "left": 20,  'backgroundColor':'white'})
   
])




@app.callback(
    Output("locations", "children"), 
    Output("ST_ClusterDBSCAN", "children"), 
    Output("zoomlevel", "children"), 
    
     Input("map", "bounds"), 
     Input("map", "zoom")
)
def map_click(bounds, zoom):
    # print(zoom)
    # bds = bounds[0][1], bounds[0][0], bounds[1][1],bounds[1][0],4326
    # print(bds)

    if zoom < 13:
        return    [ dl.CircleMarker(center=[55, 10])], [dl.CircleMarker(center=[55, 10])], zoom
       
    else:
  
        bds = bounds[0][1], bounds[0][0], bounds[1][1],bounds[1][0],4326
        print(bds)
        # if zoom > 17:
        #     sql=f"""SELECT pt, leadbichtrobnm FROM work_schema.hhp_pt WHERE pt && ST_MakeEnvelope{bds} """
        # else:
        #     sql=f"""SELECT pt, leadbichtrobnm FROM work_schema.hhp_pt WHERE pt && ST_MakeEnvelope{bds} limit 100 """
        # print(sql)
        sql =f"""
            SELECT pt,
            CASE 
                WHEN leadmaxdwnspdanycomp = '(F) Gigabit or Higher' THEN 'GIG' 
                ELSE 'NONE GIG' END IS_GIG
            FROM work_schema.hhp_pt
            WHERE pt && ST_MakeEnvelope{bds}
                
            """
        
        data = get_postgis(sql=sql, geom_col='pt')
        # print(len(data))
        data.drop_duplicates(keep=False,inplace=True)
        print(data.is_gig.unique())
        len_data=len(data)
        
        data = data.to_json()
        
        data = json.loads(data)


        sql =f"""
        SELECT cid AS which, ST_ConcaveHull (ptg, .97) AS poly 
        FROM (
            SELECT cid,  st_collect ( pt)  AS ptg  
            FROM (
                SELECT pt, ST_ClusterDBSCAN(pt, eps := 400 / (6.4e6 * 2 * 3.14 / 360 ) , minpoints := 200) over () AS cid
                FROM work_schema.hhp_pt h
                WHERE pt && ST_MakeEnvelope{bds}
                    AND leadmaxdwnspdanycomp   like '%%Gigabit%%') m
        WHERE m.cid is not null
        GROUP BY 1 
        LIMIT 200
        )foo;
        """

        poly = get_postgis(sql, geom_col='poly')

        print(len(poly))
        poly = poly.to_json()
        
        poly = json.loads(poly)

      

        return [
            dl.GeoJSON(
                data= data, 
                id="gig_no_gig",
                # cluster=True,
                # spiderfyOnMaxZoom = True,
                options=dict(pointToLayer=point("pointToLayer")),
                # clusterToLayer=cluster("pointToLayer"),
                # zoomToBoundsOnClick=True,
                # superClusterOptions=dict(radius=300),
                # hoverStyle=arrow_function(dict(weight=1, color='red', dashArray='**')),
                hideout=dict(colorProp='is_gig', circleOptions=dict(fillOpacity=1,  color = 'transparent',radius=4, zIndex=800),
                                colorscale=list(my_colors.values()), classes=list(my_colors.keys()
                                )
                                ),
                                children=[dl.Tooltip(id = 'tooltips')]
            )
        ], [     dl.GeoJSON(
                                 data= poly, 
                                
                                
                                # options=dict(style=dallas_track),
                                
                                hoverStyle=arrow_function(
                                    dict(weight=1, color='red', dashArray='**')
                                )
                            )],f" Zoom Level:  {zoom}, Number of points: {len_data}"


@app.callback(Output("tooltips", "children"), [Input("gig_no_gig", "hover_feature")])
def map_click(feature):
    print(ctx.triggered)
    if feature == None:
        return ''
    # else:
    #     print(feature)
    return str(feature['properties']['is_gig'])

if __name__ == '__main__':
    app.run(debug=True, port = 8020)