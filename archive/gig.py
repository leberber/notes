
import dash_leaflet as dl
from dash import Dash, html, Input, Output, ctx, dcc, State
from connection import get_postgis
from dash.exceptions import PreventUpdate
import json
from dash_extensions.javascript import arrow_function, assign,  Namespace
import dash_bootstrap_components as dbc
cluster = Namespace("myNamespace", "cluster")
point =  Namespace("myNamespace", "point")
dbscanArea = Namespace("myNamespace", "dbscanArea")
gig_poly = Namespace("myNamespace", "gig_poly")
none_gig_poly = Namespace("myNamespace", "none_gig_poly")



my_colors={
 'GIG':'#eb1607',
  'NONE GIG':'#0a0a0a',
 }

 

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




app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP], suppress_callback_exceptions=True)
app.layout = html.Div([
    dl.Map(
        id="map",
        style={'width': '100%', 'height': '100vh'},
        zoom=13,
        maxZoom =20,
        center =[32.779167, -96.808891],
        attributionControl=False,   
        
        children=[

            dl.LayersControl(
                [dl.BaseLayer(dl.TileLayer(url=key[1]),name=key[0], checked=key[0]== "mapbox street") for key in basemaps.items()] +
                [
                   dl.FeatureGroup([
            dl.EditControl(id="edit_control")]),
                    dl.Overlay(
                        dl.LayerGroup(
                                id="locations",   
                        ), name="competitors", 
                        checked=True
                    ),
                        dl.Overlay(
                        dl.LayerGroup(
                                id="ST_ClusterDBSCAN_GIG",   
                        ), name="DBSCAN GIG", 
                        checked=True
                    ),
                    dl.Overlay(
                        dl.LayerGroup(
                                id="ST_ClusterDBSCAN_NONE_GIG",   
                        ), name="DBSCAN_NONE_GIG", 
                        checked=True
                    ),
                    dl.Overlay(
                        dl.LayerGroup(
                                id="ClusterDBSCAN_AREA",   
                        ), name="DBSCAN AREA", 
                        checked=False
                    ),
                ]
            ),  
        ], 
    ),
     
    html.Div(
        [
    html.Div(divs, style={ 'zIndex': '1000', 'position': 'fixed', 'top':'10px', 'left':'55px','background-color':'white', 
     'padding':'5px', 'padding-left':'10px',"border-radius": "10px",}),
    # html.Div(id = 'zoomlevel', style={ 'zIndex': '1000', 'position': 'fixed', 'top':'20px', 'left':'60px', 'fontSize':'40px', 'color':'red', 'backgroundColor':'rgb(255, 255, 255, 0.8' }),
   
    html.Div([html.Span('Concave Hull', className='bot-text'),dbc.Input(className ='my-input', id='concavehull', type='number', value =0.97)],),
    html.Div([html.Span('Epsilon'),dbc.Input(className ='my-input',id='epsilon', type='number', value =100)],),
    html.Div([html.Span('Min Points'),dbc.Input(className ='my-input',id='min_points', type='number', value =10)]),
    html.Div(dbc.Button("Update", id = 'update',color="primary", className="btn btn-success"), style={'padding-top':'5px'}),
   
    
    ],style={'zIndex': '1000', "position": "fixed", "bottom": 10,
     "left": 10, 'background-color':'white', 
     'padding':'15px',"border-radius": "10px",
     'width':'150px'
     })

])




@app.callback(
    Output("locations", "children"), 
    Output("ST_ClusterDBSCAN_GIG", "children"), 
    Output("ST_ClusterDBSCAN_NONE_GIG", "children"), 
    # Output("zoomlevel", "children"), 
    
     State("map", "bounds"), 
    #  Input("map", "zoom"),
     State("concavehull", "value"),
    State("epsilon", "value"),
     State("min_points", "value"),
     Input("update", "n_clicks")

)
def map_click(bounds,concave,e,min_points, n):
    print(bounds)

    # print(n)
    # ctx_msg = json.dumps({
    #     'states': ctx.states,
    #     'triggered': ctx.triggered,
    #     'inputs': ctx.inputs
    # }, indent=2)
    # print(ctx_msg)
    # print(bounds, latlong)
    # print(zoom)
    bds = bounds[0][1], bounds[0][0], bounds[1][1],bounds[1][0],4326
    print(bds)
    # # print(bds)
    # if zoom > 13:
    #     return '', '', '', ''
    # if zoom <= 13:
    #     return   dl.Polygon(positions=[[32.753210028851896, -96.92868232727052], [32.7983138222763, -96.92868232727052], [32.7983138222763, -96.81427001953126], [32.753210028851896, -96.81427001953126]]), [ dl.CircleMarker(center=[32.60698915452777, -96.20178222656251])], dl.CircleMarker(center=[32.60698915452777, -97.4974822998047]), zoom
       
    # else:

  
    # bds = bounds[0][1], bounds[0][0], bounds[1][1],bounds[1][0],4326
    # print(bds)
    # if zoom > 17:
    #     sql=f"""SELECT pt, leadbichtrobnm FROM work_schema.hhp_pt WHERE pt && ST_MakeEnvelope{bds} """
    # else:
    #     sql=f"""SELECT pt, leadbichtrobnm FROM work_schema.hhp_pt WHERE pt && ST_MakeEnvelope{bds} limit 100 """
    # print(sql)
    sql =f"""
      SELECT pt,
        CASE 
            WHEN leadmaxdwnspdanycomp = '(F) Gigabit or Higher' Then 'GIG' 
            ELSE 'NONE GIG' END IS_GIG
        FROM work_schema.hhp_pt
        WHERE pt && ST_MakeEnvelope(-96.75676345825195, 33.06363647175957, -96.52227401733398, 33.15350515698044, 4326)
            
        """
    
    data = get_postgis(sql=sql, geom_col='pt')
    # print(len(data))
    data.drop_duplicates(keep=False,inplace=True)
    # print(data.is_gig.unique())
    # len_data=len(data)
  
    
    # data = data[data.is_gig =='NON_GIG_NO_SUB']
    print(data.head())
    print(len(data))
    data = data.head().to_json()
 
   
   
    data = json.loads(data)
       # data = geobuf.encode(data)


    # sql =f"""
    # SELECT cid AS which, ST_ConcaveHull (ptg, {concave}) AS poly 
    # FROM (
    #     SELECT cid,  st_collect ( pt)  AS ptg  
    #     FROM (
    #         SELECT pt, ST_ClusterDBSCAN(pt, eps := {e} / (6.4e6 * 2 * 3.14 / 360 ) , minpoints := {min_points}) over () AS cid
    #         FROM work_schema.hhp_pt h
    #         WHERE pt && ST_MakeEnvelope(-96.92868232727052, 32.753210028851896, -96.81427001953126, 32.7983138222763, 4326)
    #             AND leadmaxdwnspdanycomp   like '%%Gigabit%%') m
    # WHERE m.cid is not null
    # GROUP BY 1 
    # LIMIT 200
    # )foo;
    # """
    sql =f"""
        SELECT cid AS which, ST_ConcaveHull (ptg, {concave}) AS poly
    FROM (
        SELECT cid,  st_collect ( pt)  AS ptg  
        FROM (
            SELECT pt, ST_ClusterDBSCAN(pt, eps := {e} / (6.4e6 * 2 * 3.14 / 360 ) , minpoints := {min_points}) over () AS cid
            FROM (
            	SELECT DISTINCT pt 
            	FROM 
                    work_schema.hhp_pt
            	WHERE pt && ST_MakeEnvelope(-96.75676345825195, 33.06363647175957, -96.52227401733398, 33.15350515698044, 4326)
                	AND leadmaxdwnspdanycomp  like '%%Gigabit%%'
            )s                  
         ) m
	    WHERE m.cid is not null
	    GROUP BY 1 
    )foo;
    """

    poly = get_postgis(sql, geom_col='poly')

    # print(len(poly))
    poly = poly.to_json()
    
    poly = json.loads(poly)

    sql =f"""
        SELECT cid AS which, ST_ConcaveHull (ptg, {concave}) AS poly
    FROM (
        SELECT cid,  st_collect ( pt)  AS ptg  
        FROM (
            SELECT pt, ST_ClusterDBSCAN(pt, eps := {e} / (6.4e6 * 2 * 3.14 / 360 ) , minpoints := {min_points}) over () AS cid
            FROM (
            	SELECT DISTINCT pt 
            	FROM 
                    work_schema.hhp_pt
            	WHERE pt && ST_MakeEnvelope(-96.75676345825195, 33.06363647175957, -96.52227401733398, 33.15350515698044, 4326)
                	AND leadmaxdwnspdanycomp not like '%%Gigabit%%'
            )s                  
         ) m
	    WHERE m.cid is not null
	    GROUP BY 1 
    )foo;
    """

    poly_no_gig = get_postgis(sql, geom_col='poly')

    # print(len(poly))
    poly_no_gig = poly_no_gig.to_json()
    
    poly_no_gig = json.loads(poly_no_gig)


    
    

    
    gsonpoints = [ dl.GeoJSON(
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
        )]

    dbsacn_gig = [ dl.GeoJSON(
                                data= poly, 
                            options=dict(style=gig_poly('style')),
                        )]

    dbsacn_no_gig = [ dl.GeoJSON(
                                data= poly_no_gig, 
                            options=dict(style=none_gig_poly('style')),
                        )]

    dbscan_area = dl.Polygon(positions=[[32.753210028851896, -96.92868232727052], [32.7983138222763, -96.92868232727052], [32.7983138222763, -96.81427001953126], [32.753210028851896, -96.81427001953126]]),
    # zoom =  f" Zoom Level:  {zoom}, Number of points: {len_data}"
    return gsonpoints, dbsacn_gig, dbsacn_no_gig
                           


@app.callback(Output("tooltips", "children"), [Input("gig_no_gig", "hover_feature")])
def map_click(feature):
    # print(ctx.triggered)
    if feature == None:
        return ''
    # else:
    #     print(feature)
    return str(feature['properties']['is_gig'])

if __name__ == '__main__':
    app.run(debug=True, port = 8020)