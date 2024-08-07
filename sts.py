from flask import Flask, url_for, redirect, session
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from authlib.integrations.flask_client import OAuth

# Initialize Flask server
server = Flask(__name__)
server.secret_key = 'random secret'

# Initialize OAuth
oauth = OAuth(server)

# Register ESSO-UAT OAuth client
esso_uat = oauth.register(
    name='esso-uat',
    client_id='3f6732ba-e495-4829-8717-7a30c0cbebba',
    client_secret='YOUR_CLIENT_SECRET',  # Replace with the actual secret you receive
    server_metadata_url='https://login.esso-uat.charter.com:8443/nidp/oauth/nam/.well-known/openid-configuration',
    api_base_url='https://login.esso-uat.charter.com:8443/nidp/oauth/nam/',
    client_kwargs={'scope': 'openid profile email sAMAccountName'}
)

# Initialize Dash app
app = Dash(__name__, server=server, url_base_pathname='/')

# Layout of the Dash app
app.layout = html.Div([
    dcc.Location(id='url', refresh=True),
    html.H1("Welcome to the Dash App"),
    html.Div(id='content'),
    html.Button('Login with ESSO-UAT', id='login-button', n_clicks=0),
    html.Div(id='user-info')
])

# Flask routes for OAuth
@server.route('/login')
def login():
    esso_uat_client = oauth.create_client('esso-uat')
    redirect_uri = 'https://mituat.chartercom.com/authorize'  # Use the registered redirect URI
    return esso_uat_client.authorize_redirect(redirect_uri)

@server.route('/authorize')
def authorize():
    esso_uat_client = oauth.create_client('esso-uat')
    token = esso_uat_client.authorize_access_token()
    resp = esso_uat_client.get('userinfo')
    resp.raise_for_status()
    user_info = resp.json()
    session['email'] = user_info['email']
    session['samaccountname'] = user_info.get('sAMAccountName', '')
    return redirect('/')

@server.route('/')
def index():
    return "Dash app is running"

# Dash callback to update content based on URL
@app.callback(
    Output('content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if 'email' in session:
        return html.Div([
            html.H2(f"Hello, {session['email']}"),
            html.P(f"sAMAccountName: {session['samaccountname']}"),
            html.A('Logout', href='/logout')
        ])
    else:
        return html.H2("You are not logged in.")

# Dash callback to handle login button click
@app.callback(
    Output('url', 'pathname'),
    [Input('login-button', 'n_clicks')]
)
def login_redirect(n_clicks):
    if n_clicks > 0:
        return '/login'
    return '/'

@server.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('samaccountname', None)
    return redirect('/')

if __name__ == '__main__':
    app.run_server(debug=True)
