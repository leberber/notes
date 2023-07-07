from dash import Dash, html

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

# list(my_colors.values()), classes=list(my_colors.keys()))
print(len(my_colors))
app = Dash(__name__)

divs=[]
for x, y in my_colors.items():
    divs.append(html.Div(
        [
            html.Div(style={ 'display': 'inline-block', 'width': '10px', 'height': '10px', 'background-color': y, 'margin-right':'7px'}),
            html.Div(x,style={ 'display': 'inline-block', 'font-family':'Robato', 'font-size':'12px', 'color':'#52504a'}),
        ],
        ) )



app.layout = html.Div(
divs
)

if __name__ == '__main__':
    app.run_server(debug=True, port=8070)