
import dash_leaflet as dl
from dash import Dash, html, Input, Output
import geopandas as gpd
from shapely.geometry import Polygon
import json
import pandas as pd
import geojson
import numpy as np

class Bbox:
    
    # bounds[0][1], bounds[0][0], bounds[1][1],bounds[1][0]
    
    def __init__(self, bbox, padding=0):
        self.bbox = bbox
        self.padding = padding

    def to_geojson(self):
        my_plygan = Polygon([
            [self.bbox[0]-self.padding, self.bbox[3]+self.padding],
            [self.bbox[2]+self.padding, self.bbox[3]+self.padding],
            [self.bbox[2]+self.padding, self.bbox[1]-self.padding],
            [self.bbox[0]-self.padding, self.bbox[1]-self.padding]
            ])

        return json.loads( 
            gpd.GeoDataFrame(
                pd.DataFrame(
                    columns = ['geom']
                    ),
                geometry = [my_plygan]).to_json()
        )

    def get_bounding_box(self):
        return self.bbox[0]-self.padding, self.bbox[1]-self.padding, self.bbox[2]+self.padding, self.bbox[3]+self.padding

app = Dash(prevent_initial_callbacks=True)
app.layout = html.Div([
    dl.Map(
        bounds = [[32.70281110073315, -96.97374343872072], [32.85536439443039, -96.64415359497072]],
        children=[

        dl.TileLayer(), dl.LayerGroup(id="layer"), dl.LayerGroup(id="layer2")],
           id="map", style={'width': '100%', 'height': '100vh', 'margin': "auto", "display": "block"}),
])



@app.callback(Output("layer", "children"), Output("layer2", "children"),[Input("map", "click_lat_lng")])
def map_click(click_lat_lng):

    geojson1 = Bbox((-96.92868232727052, 32.753210028851896, -96.81427001953126, 32.7983138222763), 0).geojson()
    geojson2 = Bbox((-96.92868232727052, 32.753210028851896, -96.81427001953126, 32.7983138222763), 0.025).geojson()


    layer1 = [dl.GeoJSON(data= geojson1)]
    
    layer2 = [dl.GeoJSON(data= geojson2)]
    return layer1, layer2

if __name__ == "__main__":
    app.run(debug=True)