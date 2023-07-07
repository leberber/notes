import dash
from dash import Dash, dcc, html, Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
import json

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# plot creation
df_plot = px.data.tips()

fig = px.scatter(df_plot, x="total_bill", y="tip", color="smoker")
fig.add_annotation(
    text='annotation 1',
    x=0, y=0,
    xref='paper',
    yref='paper',
    showarrow=False,
    bordercolor='darkred',
    bgcolor='white',
    borderwidth=2
)
fig.update_layout(legend=dict(bordercolor = 'red', borderwidth=2))

#### anchor fig ####
anchor_fig = go.Figure()

anchor_fig.add_trace(go.Scatter(
    x=[1, 1, 1, 5, 5, 5, 9, 9, 9],
    y=[1, 5, 9, 1, 5, 9, 1, 5, 9],
    mode="markers",
    marker_size=10
))

anchor_fig.add_trace(go.Scatter(
    x=[0.5, 0.5, 0.5, 2, 5, 8],
    y=[2, 5, 8, 10, 10, 10],
    text = ['yref="bottom"', 'yref="middle"', 'yref="top"', 'xref="left"', 'xref="center"', 'xref="right"'],
    mode="text",
))

# Add shapes
for i in range(3) :
    for j in range(3):
        anchor_fig.add_shape(type="rect",
            x0=1+3*i, x1=3+3*i, y0=1+3*j, y1=3+3*j, 
            line=dict(color="RoyalBlue"),
            xref='x', yref='y',
        )

anchor_fig.update_layout(
    xaxis={'showgrid':False, 'showticklabels':False},
    yaxis={'showgrid':False, 'showticklabels':False},
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    margin={'b':0, 't':0},
    showlegend=False
)

#### utilities for layout ####
default_values =  {
    'xanchor':'center',
    'x':1,
    'xref':'paper',
    'yanchor':'middle',
    'y':1,
    'yref':'paper'
}

def legend_code(values=default_values) :
    return f'''
# legend
for i in [12,45]:
    print(i)
fig.update_layout(
    legend=dict(
        x={values.get('x')}, 
        xanchor="{values.get('xanchor')}", 
        y={values.get('y')}, 
        yanchor="{values.get('yanchor')}"
    )
)
        '''

def annotation_code(values=default_values) :
    return f'''
# annotation
fig.update_annotations(
    x={values.get('x')}, 
    xanchor="{values.get('xanchor')}",
    xref="{values.get('xref')}", 
    y={values.get('y')}, 
    yanchor="{values.get('yanchor')}",
    yref="{values.get('yref')}",
)
        '''

intro_text = '''
    This app allows you to play around with the relevant arguments for annotation and legend positioning in Plotly plots, so that you can:
    
    * Generate and copy the code to update your plot with that legend/annotation position.
    * Understand better how this arguments work in the background.

    If you want to learn more about annotation and legend positioning, click on the arrow under this text to show an explanation.
    
    If you want to learn more about each argument, click on the button with its name and a short description will appear under it.
'''

explanation_text = ['''
    When we talk about changing their position, legends are just a special type of annotations, so both are modified in the same way.
    To understand better how their arguments work, it's easier to **think about them like boxes**.
    There's a point inside each annotation box that is used as a reference by the arguments `x` and `y`.
    When we change `xanchor` or `yanchor`, we change the position of that point inside the box. 
    This is useful if we want to specify that an annotation needs to start at a certain point (`xanchor="left"`), end at that point (`xanchor="right"`) 
    or be centered at that point (`xanchor="center"`). And the same for `yanchor`, but in the vertical axis.
    ''',
    '''
    When we change `xref` or `yref`, we change the type of axis where the annotation box (and its anchor point) will be placed:

    * `xref="x"` and `yref="y"` are useful when we want to place the annotation inside the plot grid, with the rest of the traces. 
    In that case, `x` and `y` mean the same position as when we indicate x and y for a point in a scatterplot.
    * `xref="paper"` and `yref="paper"` are useful when we want to place the annotation outside the plot grid, in the area around it. 
    The points 0 and 1 indicate the corners of the grid, so any value <0 or >1 will place the annotation outside the plot grid. 
    Any value between 0 and 1 will place it inside the plot grid, but `x=0.5` will mean the middle point of the plot grid, not x=0.5 in the plot axis.
    If the xaxis range is \\[0,4\\], the annotation will be in xaxis=2, not xaxis=0.5.
    * `xref="x domain"` and `yref="y domain"` are useful when we have subplots and we want to apply the logic  of `xref="paper"` and `yref="paper"` only to one of the subplots.
    For example, if we wanted to put the annotation in the middle of the second (vertically stacked) subplot, we would specify: `yref="y2 domain"` and `y="0.5`.

    These arguments don't appear when we are modifying the legend because for the legend `xref` or `yref` are always equeal to `"paper"` 
    (they are always outside the plot grid and aren't affected by subplots)
''']

collapse_text = {
    'annotation' : dcc.Markdown('''
        More information about Legends: [Examples](https://plotly.com/python/legend/)   [Full reference](https://plotly.com/python/reference/layout/#layout-legend) \n
        More information about Annotations: [Examples](https://plotly.com/python/text-and-annotations/)  [Full reference](https://plotly.com/python/reference/layout/annotations/)
        '''),
    'xanchor' : '''
        Horizontal position of the anchor inside the annotation box.
    ''' ,
    'yanchor' : '''
        Vertical position of the anchor inside the annotation box.
    ''' ,
    'x' : '''
        Horizontal position of the annotation box anchor in the whole figure area. 
        0 is the left side of the plot grid and 1 is the left side of the plot grid, 
        but `x` can take negative values and values higher than 1.
    ''' ,
    'y' : '''
        Vertical position of the annotation box anchor in the whole figure area.
        0 is the bottom of the plot grid and 1 is the top of the plot grid, 
        but `y` can take negative values and values higher than 1.
    ''' ,
    'xref' : '''
        Which type of x axis is used for the x position: 
        * x axis id (e.g. `"x"` or `"x2"`): the `x` position refers to a x coordinate inside the plot grid. 
        * "paper": the `x` position refers to the distance from the left of the plotting area in normalized coordinates where "0" ("1") corresponds to the left (right). 
        * x axis ID followed by "domain" (separated by a space - e.g. "x domain"): the position behaves like for "paper". It only makes a difference for **subplots**.  
        With `xref="x2 domain"` the `x` value refers to the distance in fractions from the left of the domain of that axis: 
        e.g., `x=0.5` refers to the middle point between the left and the right of the domain of the second x axis.
    ''' ,

    'yref':'''
        Which type of y axis is used for the x position: 
        * y axis id (e.g. `"y"` or `"y2"`): the `y` position refers to a y coordinate inside the plot grid. 
        * "paper": the `y` position refers to the distance from the left of the plotting area in normalized coordinates where "0" ("1") corresponds to the left (right). 
        * x axis ID followed by "domain" (separated by a space - e.g. "x domain"): the position behaves like for "paper". It only makes a difference for **subplots**.  
        With `xref="x2 domain"` the `x` value refers to the distance in fractions from the left of the domain of that axis: 
        e.g., `x=0.5` refers to the middle point between the left and the right of the domain of the second x axis.
    '''

}

def control_content(index, control_item, label=None, text=None, link=None, collapse_children=None) :

    if label is None :
            label = index

    if collapse_children is None :
        if link is None :
            link = 'https://plotly.com/python/reference/layout/annotations/#layout-annotations-items-annotation-' + index
        if text is None:
            text = collapse_text.get(index)
        collapse_children = [
                dcc.Markdown(text),
                html.A("Check in Plotly Docs", href=link, target="_blank")
                ]

    component = [
        dbc.Row([
            dbc.Col(
                dbc.Button(
                    label, id={'type':'button', 'index':index}, style={'width':'-webkit-fill-available'}), 
                    width = 3, style={'margin-top':'10px'}),
            dbc.Col(
                control_item, width = 9, 
                style={'align-self': 'center','margin-top': '10px'})
            ], id={'type':'container', 'index':index}, style={'display':'flex'}),
        dbc.Row(dbc.Collapse(
            dbc.Card(dbc.CardBody(collapse_children)), id={'type':'collapse', 'index':index}, is_open=False), style={'margin-top':'10px'})
        ]
    
    return component

# layout
app.layout = html.Div([
    dbc.Row([
        dbc.Accordion(dbc.AccordionItem(
            title='Plotly legend and annotations tutorial',
            children=dcc.Markdown(intro_text, style={'margin':'15px'})
        )),
        dbc.Accordion(dbc.AccordionItem(
            title='Show explanation',
            children=dbc.CardBody([
                dcc.Markdown(explanation_text[0]),
                dcc.Graph(figure=anchor_fig),
                dcc.Markdown(explanation_text[1])
            ])
        ), start_collapsed=True)
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card(dbc.CardBody(
                control_content(
                    'annotation',
                    dcc.RadioItems(
                        ['legend', 'annotation 1'], 'legend', id={'type':'control-item', 'index':'annotation'},
                        inline= True,
                        labelStyle = {'margin-right':'25px'},
                        inputStyle={"margin-right": "5px"}
                        ),
                    collapse_children=collapse_text.get('annotation')
                    )
            ), style={'margin':'10px', 'margin-bottom':'0px', 'margin-left':'0px'}),
            dbc.Card(dbc.CardBody(
                # xanchor
                control_content(
                    'xanchor',
                    dcc.RadioItems(
                        ['center', 'left', 'right'], default_values.get('xanchor'), 
                        id={'type':'control-item', 'index':'xanchor'},
                        inline= True,
                        labelStyle = {'margin-right':'25px'},
                        inputStyle={"margin-right": "5px"}
                    )
                ) +   
                # x-slider   
                control_content(
                    'x',
                    dcc.Slider(
                        -0.5,1.5,
                        step=None,
                        value=default_values.get('x'),
                        id={'type':'control-item', 'index':'x'}
                    )
                ) +     
                # xref
                control_content(
                    'xref',
                    dcc.RadioItems(
                        ['paper','x'], default_values.get('xref'), 
                        id={'type':'control-item', 'index':'xref'},
                        inline= True,
                        labelStyle = {'margin-right':'25px'},
                        inputStyle={"margin-right": "5px"}
                        ),
                ) 
            ), style={'margin':'10px', 'margin-bottom':'0px', 'margin-left':'0px'}),
            # y settings
            dbc.Card(dbc.CardBody(
                # yanchor
                control_content(
                    'yanchor',
                    dcc.RadioItems(
                        ['middle', 'bottom', 'top'], default_values.get('yanchor'), 
                        id={'type':'control-item', 'index':'yanchor'},
                        inline= True,
                        labelStyle = {'margin-right':'25px'},
                        inputStyle={"margin-right": "5px"}
                        ),
                ) +   
                # y-slider   
                control_content(
                    'y',
                    dcc.Slider(
                        -0.5,1.5,
                        step=None,
                        value=default_values.get('y'),
                        id={'type':'control-item', 'index':'y'}
                    )
                ) +     
                # yref
                control_content(
                    'yref',
                    dcc.RadioItems(
                        ['paper','y'], default_values.get('yref'), 
                        id={'type':'control-item', 'index':'yref'},
                        inline= True,
                        labelStyle = {'margin-right':'25px'},
                        inputStyle={"margin-right": "5px"}
                        ),
                ) 
            ), style={'margin':'10px', 'margin-bottom':'0px', 'margin-left':'0px'})
        ], lg = 6, md = 12), # https://subscription.packtpub.com/book/data/9781800568914/2/ch02lvl1sec09/learning-how-to-structure-the-layout-and-managing-themes
        dbc.Col([
            dbc.Card(dbc.CardBody([
                dcc.Graph(id='graph', figure=fig),
                html.Br(),
                dbc.Row(style={'margin':'5px'}, children=
                    dmc.Prism(
                        language='python', id='code',
                        children = legend_code()
                        )
                )
            ]), style={'margin':'10px', 'margin-right':'0px', 'margin-left':'0px'})
        ], lg = 6, md = 12)      
    ])
], style={'margin':'10px'})

# Callbacks

@app.callback(
    Output('graph', 'figure'),
    Output({'type':'control-item', 'index':ALL}, 'value'),
    Output('code', 'children'),
    Input({'type':'control-item', 'index':ALL}, 'value'),
    State('graph', 'figure'),
    prevent_initial_call=True
    )
def update_figure(*args):

    current_state =  {json.loads(k.split('.')[0])['index']:v for k, v in dash.callback_context.inputs.items()}
    trigger = json.loads(dash.callback_context.triggered[0]['prop_id'].split('.')[0])['index']

    fig = args[1]
    fig = go.Figure(fig)

    if current_state.get('annotation') == 'legend' :
        if trigger  == 'annotation' :
            for i in ['xanchor', 'yanchor', 'x', 'y']:
                current_state[i] = fig['layout']['legend'][i] if fig['layout']['legend'][i] else default_values.get(i)
        else  :
            fig.update_layout(legend={
                trigger:current_state.get(trigger)
            })
        code = legend_code(current_state)

    elif current_state.get('annotation') == 'annotation 1' :
        if trigger  == 'annotation' :
            for i in default_values.keys():
                current_state[i] = fig['layout']['annotations'][0][i] if fig['layout']['annotations'][0][i] else default_values.get(i)
        else  :
            fig['layout']['annotations'][0][trigger] = current_state.get(trigger)

        code = annotation_code(current_state)

    current_state  = list(current_state.values())

    return fig, current_state, code

@app.callback(
    Output({'type':'collapse', 'index':MATCH}, 'is_open'),
    Input({'type':'button', 'index':MATCH}, 'n_clicks'),
    State({'type':'collapse', 'index':MATCH}, 'is_open'),
    prevent_initial_call = True
)
def update_figure(click, is_open):
    if click :
        return not is_open

@app.callback(
    Output({'type':'container', 'index':'xref'}, 'style'),
    Output({'type':'container', 'index':'yref'}, 'style'),
    Input({'type':'control-item', 'index':'annotation'}, 'value'),
    State({'type':'container', 'index':'xref'}, 'style'),
    State({'type':'container', 'index':'yref'}, 'style'),
)
def update_figure(value, x_style, y_style):
    if value == 'legend' :
        x_style['display'] = 'none'
        y_style['display'] = 'none'
    else :
        x_style['display'] = 'flex'
        y_style['display'] = 'flex'

    return x_style, y_style

if __name__ == '__main__':
    app.run_server(debug=True)
