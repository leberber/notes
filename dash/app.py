
import dash_mantine_components as dmc
from dash_iconify import DashIconify

from dash import (
    Dash, html, ALL, dcc, callback, Input, Output, State, 
    clientside_callback, ClientsideFunction,
    _dash_renderer, page_registry, page_container, no_update
)
import os
from flask import Flask, request, redirect, session
from flask_login import login_user, LoginManager, UserMixin, logout_user, current_user


restricted_page = {}
def require_login(page):
    for pg in page_registry:
        if page == pg:
            restricted_page[page_registry[pg]['path']] = True
            
_dash_renderer._set_react_version("18.2.0")

stylesheets = [
    "https://unpkg.com/@mantine/dates@7/styles.css",
    "https://unpkg.com/@mantine/code-highlight@7/styles.css",
    "https://unpkg.com/@mantine/charts@7/styles.css",
    "https://unpkg.com/@mantine/carousel@7/styles.css",
    "https://unpkg.com/@mantine/notifications@7/styles.css",
    "https://unpkg.com/@mantine/nprogress@7/styles.css",
]

server = Flask(__name__)
app = Dash(
    __name__, external_stylesheets=stylesheets,server=server, use_pages=True, suppress_callback_exceptions=True
)

header = dmc.Group(
            justify='space-between',
            className = 'header-inner-container',
            px = 10,
            children = [
                dmc.Burger(id="burger-button", opened=False, hiddenFrom="md"),
                dmc.Paper(
                    className = 'baylek-logo-image',
                    children = [
                        dmc.Image(src="/assets/baylek.png",  className='image-width'),
                    ]
                ),
                dmc.Flex(
                    children = [
                        dcc.Location(id="url"),
                        html.Div(id="user-status-header"),
                        dmc.ActionIcon(
                            id = 'color-scheme-toggle',
                            n_clicks=0, 
                            variant= "transparent",
                            children = [
                                DashIconify(icon="ic:baseline-light-mode",  color='100%')
                            ]
                        )
                    ]
                ) 
            ]
        )






VALID_USERNAME_PASSWORD = {"test": "test", "hello": "world"}

server.config.update(SECRET_KEY=os.getenv("SECRET_KEY"))

# Login manager object will be used to login / logout users
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = "/login"


class User(UserMixin):
    # User data model. It has to have at least self.id as a minimum
    def __init__(self, username):
        self.id = username


@login_manager.user_loader
def load_user(username):
    """This function loads the user by user id. Typically this looks up the user from a user database.
    We won't be registering or looking up users in this example, since we'll just login using LDAP server.
    So we'll simply return a User object with the passed in username.
    """
    return User(username)

links = dmc.Box([
        html.Div(
            dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
        ) for page in page_registry.values()
    ]),

app.layout = dmc.MantineProvider(
    id="mantine-provider",
    children = [
        dmc.AppShell(
            id="app-shell",
            navbar={ "breakpoint": "md", "collapsed": {"mobile": True}},
            children = [
                dmc.AppShellHeader(header),
                dmc.AppShellNavbar(links, withBorder=True),
                dmc.AppShellMain(page_container),
            ]
        )
    ]   
)
@server.route('/', methods=['POST'])
def login_button_click():
    print("ddd")
    if request.form:
        username = request.form['username']
        password = request.form['password']
        if VALID_USERNAME_PASSWORD.get(username) is None:
            return """invalid username and/or password <a href='/login'>login here</a>"""
        if VALID_USERNAME_PASSWORD.get(username) == password:
            login_user(User(username))
            if 'url' in session:
                if session['url']:
                    url = session['url']
                    session['url'] = None
                    return redirect(url) ## redirect to target url
            return redirect('/') ## redirect to home
        return """invalid username and/or password <a href='/login'>login here</a>"""
    
@app.callback(
    Output("user-status-header", "children"),
    Output('url','pathname'),
    Input("url", "pathname"),
    Input({'index': ALL, 'type':'redirect'}, 'n_intervals')
)
def update_authentication_status(path, n):
    print(path, n)
    ### logout redirect
    if n:
        if not n[0]:
            return '', no_update
        else:
            return '', '/login'

    ### test if user is logged in
    if current_user.is_authenticated:
        if path == '/login':
            return dcc.Link("logout", href="/logout"), '/'
        return dcc.Link("logout", href="/logout"), no_update
    else:
        ### if page is restricted, redirect to login and save path
        if path in restricted_page:
            session['url'] = path
            return dcc.Link("login", href="/login"), '/login'

    ### if path not login and logout display login link
    if current_user and path not in ['/login', '/logout']:
        return dcc.Link("login", href="/login"), no_update

    ### if path login and logout hide links
    if path in ['/login', '/logout']:
        return '', no_update
    
clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='theme_switcher_callback'
    ),
    Output("mantine-provider", "theme"),
    Output("mantine-provider", "forceColorScheme"),
    Output("color-scheme-toggle", "children"),
    Input("color-scheme-toggle", "n_clicks")

)
clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='side_bar_toggle'
    ),
    Output("app-shell", "navbar"),
    Input("burger-button", "opened"),
    State("app-shell", "navbar"),

)



if __name__ == "__main__":
    app.run_server(debug=True, port= 8053)

