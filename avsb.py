from dash import html, dcc, callback, Input, Output, State,  register_page, ctx, no_update

import dash_mantine_components as dmc
import numpy as np
import dash_ag_grid as dag
import plotly.graph_objects as go
import pandas as pd
from pages.utils import cell_styles, myFormater, myformatter
from pages.connections import cur
from pages.graphlayout import gl
from pages.components import info_header

def get_data(sql):
    cursor = cur.cursor()
    return cursor.execute(sql).fetch_pandas_all()

register_page(__name__, path='/')

from pages.avsb.layout import layout
from pages.avsb.sql import avsb, avsb_actuals, avsb_categ_imact, ab_interaction_importance
from pages.sql import is_continous, create_bins,generate_case

layout = layout



@callback(
   
    Output("avsb-model-grid-modal", "opened"),
    Input("avsb-select-model-modal", "n_clicks"),
    State("avsb-model-grid-modal", "opened"),
    prevent_initial_call=True,
)
def open_the_metadata_table_modal(n_clicks,  opened):

    return not opened

@callback( 
          
    Output("avsb-model-metadata", "data"),
    Output("avsb-model-model_id", "data"),
   
    
    Output("avsb-select-a", "data"),
    Output("avsb-select-b", "data"),
    Output("avsb-select-global-filter", "data"),
    Input("avsb-selection-single-grid", "selectionChanged"),
    prevent_initial_call=True,
)

def getting_model_metadata( selected ):
    if not selected:
        return no_update
    
    model_id=  selected[0]['Model Hash']
    model_name=  selected[0]['Label'].replace('"',"")
    
    md = get_data(f"""select * from models_metadata where "Model Hash" = '{model_id}'  """).to_dict('records')[0]
    
        
    n_feat = sorted([ s.strip() for s in md['Numeric Features'].split(',')])
    c_feat =  sorted([ s.strip() for s in md['Categorical Features'].split(',')])
    # md['all_cols'] = n_feat + c_feat
    md['Categorical Features'] = c_feat
    md['Numeric Features'] = n_feat
    
    # all_featues = sorted(c_feat+ n_feat)
    # all_featues = dict(zip(all_featues, all_featues))
    # used_cols_options = [{ 'value':i, 'label':i} for i in all_featues]

    base_cols_options = sorted(get_data(f"""select * from _{model_id}_base_data limit 0"""))
    base_cols_options = [{ 'value':i, 'label':i} for i in base_cols_options]
   
    return md, model_id, base_cols_options, base_cols_options, base_cols_options



@callback(
    Output("avsb-cards-row", "children"),
    Output("avsb-model-features", "children"),
    Input("avsb-model-metadata", "data")
)
def feature_importance_barchart(md):
    if not md:
        return no_update

    header, feature =info_header(md)
    return header, feature 

@callback(
    
    Output("avsb-global-ace-editor-input", "value"), 
    Input("avsb-select-global-filter", "value"),
    prevent_initial_call=True,
)
def avsb_callback(value ):
    return f"WHERE {value} "


@callback(
    Output("avsb-a-ace-editor-input", "value"),
    Input("avsb-select-a", "value"), 
    prevent_initial_call=True,
)
def avsb_callback(value ):
    return f"WHERE {value} "

@callback(
    Output("avsb-b-ace-editor-input", "value"),
    Input("avsb-select-b", "value"), 
    prevent_initial_call=True,
)
def avsb_callback(value ):
    return f"WHERE {value} "


@callback(Output('avsb-adjust-div', 'style'), 
            Input('avsb-yaxis', 'value'))
def hide_show_the_adjsut(yaxis):
    if yaxis == 'Y-Axis':
        return {'display':'none'}
    else:
        return {'display': 'block'}


@callback(
    Output("avsb-main-waterfall", "figure"),
    Output("avsb-main-waterfall", "style"),
    Output("avsb-ab-filters-in-graph", "children"),
    
    Input("avsb-model-model_id", "data"), 
    State("avsb-global-ace-editor-input", "value"),
    State("avsb-a-ace-editor-input", "value"),
    State("avsb-b-ace-editor-input", "value"),
    State("avsb-allother-threshold", "value"),
    State("avsb-a-change", "value"),
    State("avsb-b-change", "value"),
    Input("avsb-yaxis", "value"),
    State("avsb-no-axis-adjust", "value"),
    Input("avsb-reverse-color", "checked"),
    Input("run-avsb-btn", "n_clicks"),
    prevent_initial_call=True,
)
def avsb_callback(model_id, gf,  a_f, b_f, alloter, a_change, b_change, yaxis, adjust,color, run_btn):
    
    if not model_id :
        return {},{'display': 'none'}, html.Div()
    if ctx.triggered_id == 'avsb-model-model_id':
        return {},{'display': 'none'}, html.Div()
    # print( f"model_id = '{model_id}'")
    # print( f"gf = '{gf}'")
    # print( f"a_f = '{a_f}'")
    # print( f"b_f = '{b_f}'")
    # print( 'alloter= ', alloter)
    # print( 'b_change= ', b_change)
    # print( 'a_change= ', a_change)
    # print( f"yaxis = '{yaxis}'")
    # print( 'color= ', color)
    # print(model_id)

    if yaxis == 'Y-Axis':
        my_y_axis = 'contribution'
        ax_visibale = True
    else:
        ax_visibale = False
        my_y_axis = 'no_yaxis'

    if color == False:
        red = '255, 49, 49'
        green = '126, 217, 87'
    else:
        green = '255, 49, 49'
        red = '126, 217, 87'

    df = avsb(model_id, gf, a_f,  b_f)

    a = get_data(avsb_actuals(model_id, gf, a_f)).to_dict('records')[0]
    a_actual = float(a['actual'])
    a_residual = float(a['residual'])

    b = get_data(avsb_actuals(model_id, gf,b_f)).to_dict('records')[0]
    b_actual = float(b['actual']) 
    b_residual = float(b['residual'])
    if a_change and b_change:
        a_actual = a_change /100
        b_actual  = b_change /100

    alloc = b_actual - a_actual - b_residual + a_residual




    df['alloc'] = alloc
    df['proportion'] = (df.AVG_SHAP_DIFF/df.AVG_SHAP_DIFF.sum()) * 100
    df['contribution'] =  df['proportion'] * (alloc)

    allOther = df[abs(df['contribution']) < alloter]['contribution'].sum()
    df = df[abs(df['contribution']) >= alloter]
    df= df[['PREDICTOR_NAME', 'contribution']]
    df.loc[len(df.index)] = ['allOther',  allOther]
    # print('b_actual',b_actual, 'a_actual',a_actual, 'b_resi',b_residual ,'a_resi',a_residual, alloc, df.contribution.sum())

    df['no_yaxis'] = df['contribution']
    df['measure'] = 'relative'
    df = df.sort_values(by=['contribution'], ascending=False)
    values = df.values.tolist()
    df = df.sort_values(by=['contribution'])
    values.insert(0,   ['A',  a_actual*100, a_actual*adjust, 'absolute'])
    values.append(['A Residuals', - a_residual*100,  - a_residual*100, 'relative'])
    values.append(['B Residuals', b_residual*100, b_residual*100, 'relative'])
    values.append(['B',  b_actual*100, b_actual*adjust, 'total'])

    df = pd.DataFrame(values, columns = df.columns)
    # print(df)

    fig  = go.Figure()
    fig.add_trace(go.Waterfall(
        width= [0.8] * len(df),
                x = df['PREDICTOR_NAME'], 
                    y = df[my_y_axis],
                measure = df['measure'],
                base = 0,
                cliponaxis= False,
                textfont=dict(
                    family="verdana, arial, sans-serif",
                    size=10,
                    color="rgb(148, 144, 144)"
                ),
                text =  df['contribution'].apply(lambda x: '{0:1.2f}%'.format(x)),
                textposition = 'outside',
                decreasing = {"marker":{"color":f"rgba({red}, 0.7)",  "line":{"color":f"rgba({red}, 1)","width":2}}},
                increasing = {"marker":{"color":f"rgba({green}, 0.7)","line":{"color":f"rgba({green}, 1)", "width":2}}},
                totals     = {"marker":{"color":"rgba(12, 192, 223, 0.7)", "line":{"color":"rgba(12, 192, 223, 1)", "width":2}}},
                    connector = {"line":{"color":"rgba(217, 217, 217, 1)", "width":1}},
                ))
    # title={
    #         'text': 'Explained By change in Sales Mix between Septemer and December, 2022',
    #         'x':0.525,
    #         'xanchor': 'center',
    #         'yanchor': 'top'  
    #     }
    gl['margin']= dict(l=20, r=50, t=0, b=20)
    # gl['title']= title
    fig.update_layout(height=400)
    end = 0.5 + len(df) -2
    start = 0.5 + len(df) -4
    fig.update_yaxes(visible=ax_visibale)
    # gl['yaxis'] ['ticksuffix'] = "%"
    fig.add_vrect(x0=start, x1=end,
                fillcolor="pink", opacity=0.15 , line_color="pink")
    fig.update_annotations(font=dict( size=14, color="rgb(148, 144, 144)"))
    fig.update_yaxes(ticksuffix = "%")
    fig.update_layout(gl)


    grid_ab = dmc.Grid(
    children=[
        dmc.Col(html.Div(dmc.Prism(a_f.replace('WHERE', 'A ->') ,language="sql", noCopy =True, className='avsb-waterfall-prism')), span=6),
        dmc.Col(html.Div(dmc.Prism(b_f.replace('WHERE', 'B ->') ,language="sql", noCopy =True, className='avsb-waterfall-prism')), span=6),

    ],
    
)


    return  fig, {'display': 'block'}, grid_ab


#   div = html.Div(
#         [
#             g, dcc.Graph(figure=fig, id = 'avsb-main-waterfall')
#         ], style= {'background-color':'white', 'borderRadius':'15px', 'padding':'25px 15px 15px 15px', 'margin-top':'15px'}
#     )
@callback(
    Output("avsb-modal-custom-bin", "opened"),
    Input("avsb-modal-custum-bin-btn", "n_clicks"),
    Input('avsb-ace-custom-bin-btn', 'n_clicks'),      
    State("avsb-modal-custom-bin", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks, close, opened):
    return not opened

@callback(
    Output('avsb-interaction-bar', 'children'),
    Input("avsb-model-model_id", "data"), 
    Input('avsb-main-waterfall', 'clickData'),
    State("avsb-global-ace-editor-input", "value"),
    State("avsb-a-ace-editor-input", "value"),
    State("avsb-b-ace-editor-input", "value"),
    prevent_initial_call=True,
)
def ab_interaction_import(model_id, predictor, gf,  a_f, b_f):
    # print(predictor)
    if not predictor :
        return html.Div()
    if ctx.triggered_id == 'avsb-model-model_id':
        return html.Div()
    

    alloc = float(predictor['points'][0]['text'].replace("%", ""))/100
    predictor = predictor['points'][0]['x']
    

    df = ab_interaction_importance(model_id, predictor,gf, a_f, b_f)
    df['alloc'] = alloc
    df['proportion'] = (df.AVG_SHAP_DIFF/df.AVG_SHAP_DIFF.sum()) * 100
    df['contribution'] =  df['proportion'] * (alloc)
    # df = df.reindex(df.contribution.abs().sort_values(ascending=False).index).reset_index()
    # df = df [['PREDICTOR_NAME', 'contribution']]
    # allOther= df[df.index > 4 ]['contribution'].sum()
    # df = df.head(5)
    # df.loc[len(df.index)] = ['allOther', allOther]
    df = df.reindex(df.contribution.abs().sort_values(ascending=True).index)
    # print(sum([abs(i) for i in list(df.contribution)]))
    # print(sum(df.contribution))
    df['PREDICTOR']=df.PREDICTOR_NAME.str.replace('_X_'+predictor, '')
    df['PREDICTOR']=df.PREDICTOR.str.replace(predictor+'_X_', '')

   
    # df = df.sort_values(by=['contribution'], axis=1, key=np.abs, ascending=False)
    # df = df.sort_values(by=['contribution'])
    
 

    df['color'] = np.where(df.contribution > 0, 'rgba(126, 217, 87, 0.6)', 'rgba(255, 49, 49, 0.6)')
    df['line'] = np.where(df.contribution > 0, 'rgba(126, 217, 87, 1)', 'rgba(255, 49, 49, 1)')

    fig = go.Figure(
            go.Bar(
                y=df.PREDICTOR, 
                x=df.contribution, 
                marker_color=df.color, 
                marker_line=dict(width=2, color=df.line),  
                width= [0.8] * len(df), orientation='h',
                 text=df['contribution'].apply(lambda x: '{0:1.2f}%'.format(x)),
                textposition='outside',
                 hoverinfo='none',
                cliponaxis= False,
                   textfont=dict(
                    family="verdana, arial, sans-serif",
                    size=10,
                    color="rgb(148, 144, 144)"
                ),
    )
    )
    fig.update_xaxes(visible=False, showticklabels=False)
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside")
    fig.update_layout(barmode='relative', title_text='Relative Barmode')
    fig.update_layout(
        title={'text': f'Interactions of {predictor}', 'x':0.525, 'xanchor': 'center', 'yanchor': 'top'}
        )
    gl['margin']= dict(l=20, r=50, t=50, b=20, pad = 50)
    # fig.update_layout(height=400)
    fig.update_layout(gl)
    fig.update_layout(  
        font=dict(
        size=9,
      
    ),)
      

    # print(df)
    return html.Div(dcc.Graph(figure=fig, style={'height':35*len(df)}), className='avsb-waterfall-left')



@callback(
        Output('avsb-category-impact-grid', 'children'),
        Output('avsb-ace-custom-bin', 'value'),
        Output('avsb-bin-feature-default', 'data'),
        Output('avsb-filter-csv','style'),
        Input("avsb-model-model_id", "data"), 
        Input('avsb-main-waterfall', 'clickData'),
        State("avsb-global-ace-editor-input", "value"),
        State("avsb-a-ace-editor-input", "value"),
        State("avsb-b-ace-editor-input", "value"),
        State('avsb-ace-custom-bin', 'value'),
        State('avsb-bin-feature-default', 'data'),
        Input('avsb-ace-custom-bin-btn', 'n_clicks'),
        prevent_initial_call=True, 
        )
def category_impact_grid(model_id, predictor, gf, a_f, b_f, custom_sql_value, saved_custom_bin, custom_btn):
    # print(saved_custom_bin)
    if not model_id or not predictor:
        return html.Div(), html.Div(), no_update, no_update
    
    if ctx.triggered_id == 'avsb-model-model_id':
        return html.Div(), html.Div(), no_update, no_update
    model_id = "_"+model_id
    color_conditions = { '> 0' :'rgba(157, 227, 216, 0)' , ' < 0': 'rgba(191, 80, 152, 0)'}
    
    noUpdateList = ['A', 'B', 'allOther', 'A Residuals', 'B Residuals']
    predictor = predictor['points'][0]['x']
    

    if predictor in noUpdateList:
        return html.Div(), html.Div(), no_update, no_update
    else:
        if ctx.triggered_id=='avsb-ace-custom-bin-btn':
            predictor_s = custom_sql_value
            saved_custom_bin[predictor] = custom_sql_value
        else:
            if is_continous(predictor, model_id):
                if predictor in saved_custom_bin:
                    predictor_s = saved_custom_bin[predictor]
                else:
                    intervals = create_bins(model_id, predictor, gf,  num_bins=10)
                    predictor_s = f"{generate_case(intervals, predictor)}"
            else: 
                predictor_s = predictor
    sql = avsb_categ_imact(model_id, predictor,predictor_s,  gf, a_f, b_f)
            
    df = get_data(sql).round(4)  
      
    feature1_dict = {
        f"{predictor}": { "group":"", "format": "None", "columnGroupShow": "open","headerTooltip":""},
        "Segment A Observtion Count":  { "group":"", "format": "number", "columnGroupShow": "open","headerTooltip":""},
        "Segment A Observtion %":  { "group":"", "format": "percent", "columnGroupShow": "open","headerTooltip":""},
        "Segment A Avg Shap Value":  { "group":"", "format": "number", "columnGroupShow": "open","headerTooltip":""},
        "Segment B Observtion Count":  { "group":"", "format": "number", "columnGroupShow": "open","headerTooltip":""},
        "Segment B Observtion %":  { "group":"", "format": "percent", "columnGroupShow": "open","headerTooltip":""},
        "Segment B Avg Shap Value":  { "group":"", "format": "number", "columnGroupShow": "open","headerTooltip":""},
        "Observation % Diff (B minus A)":  { "group":"", "format": "percent", "columnGroupShow": "open","headerTooltip":""},
        "Average Shap Diff (B minus A)":  { "group":"", "format": "percent", "columnGroupShow": "open","headerTooltip":""},
        "Total Shap Diff (B minus A)":  { "group":"", "format": "number", "columnGroupShow": "open","headerTooltip":""},
    }
    stylecells = cell_styles(df, ["Total Shap Diff (B minus A)", "Average Shap Diff (B minus A)"], 10, color_conditions = color_conditions)

    
    columnDefs = myformatter(feature1_dict)


    cellStyle = {
            "styleConditions": stylecells
        }
    impact_table = dag.AgGrid(
        style={"height": 600},
        id="avsb-ag-grid",
        rowData=df.to_dict("records"),
        # columnDefs=[{"headerName": i, "field": i} for i in df.columns],
        columnDefs=columnDefs,
        defaultColDef={"resizable": True, "sortable": True, "filter": True, 'wrapHeaderText':True, 'autoHeaderHeight': True },
        rowSelection="single",
        dangerously_allow_html=True,
        cellStyle = cellStyle
    ),


    return html.Div(impact_table, className='avsb-table-style'), predictor_s, saved_custom_bin, {'display': 'block'}

@callback(
    Output("avsb-ag-grid", "enableExportDataAsCsv"),
    Input("avsb-csv-button", "n_clicks"),
    
)
def export_data_as_csv(n_clicks):
    if ctx.triggered_id == 'avsb-csv-button':
        return True
    return False
