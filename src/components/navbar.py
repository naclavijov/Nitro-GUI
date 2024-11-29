# package imports
from dash import html, callback, Output, Input, State
import dash_bootstrap_components as dbc

# local imports
from utils.images import logo_nitro_encoded,logo_senai_encoded
from dash.exceptions import PreventUpdate
import json
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash import dcc


def create_nav_link(icon, label, href):
    return dcc.Link(
        dmc.Group(
            [
                dmc.ThemeIcon(
                    DashIconify(icon=icon, width=18),
                    size=30,
                    radius=30,
                    variant="light",
                ),
                dmc.Text(label, size="sm", color="black",weight=700),
            ]
        ),
        href=href,
        style={"textDecoration": "none"},
    )


navbar = html.Div([




    dbc.Nav(
    vertical = 'md',
    pills = True,
    fill = True,
    horizontal='start',
    navbar_scroll = False,
    # justified=True,
    children=[
    html.H4("Menu",className='text-bold-black'),
    html.Hr(),
    html.Div(
            children=[
                dmc.Stack(
                    children=[
                        create_nav_link(
                            icon="radix-icons:rocket",
                            label="Home",
                            href="/",
                        ),
                    ],
                ),
                dmc.Divider(
                    label="", style={"marginBottom": 20, "marginTop": 20}
                ),
                dmc.Stack(
                    children=[
                        create_nav_link(
                            icon="fa:bar-chart", label="Visualização", href="/page1"
                        )
                    ],
                ),
                dmc.Divider(
                    label="", style={"marginBottom": 20, "marginTop": 20}
                ),
                dmc.Stack(
                    children=[
                        create_nav_link(
                            icon="ph:squares-four-duotone", label='Predição', href='/page2'
                        )
                    ],
                ),
            ],
        )
        
    ],
style={
    # "position": "fixed",
    # "top": "15rem",
    "left": 0,
    "width": "13rem",
    "padding": "1rem 1rem",
    # "background-color": "lightgreen",
    'border-top': '2px solid black',
    "overflow": "hidden"
})
    ],className='text-black',
    style={'border-top': '0px solid black', 'border-bottom': '0px solid black','border-radius': 0,"backgroundColor": '#D9E3F1'}
    # style=SIDEBAR_STYLE
)




"""

# add callback for toggling the collapse on small screens
@callback(
    Output('navbar-collapse', 'is_open'),
    Input('navbar-toggler', 'n_clicks'),
    State('navbar-collapse', 'is_open'),
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


# @callback(
#     Output('n_clicker_navbar_pg2', 'data'),
#     Input('navlink_pg2', 'n_clicks'),
# )
# def pass_nclick_nav(n):
#     return n


# @callback(
#     Output('navlink_pg2', 'disabled'),
#     Input('intermediate-treated-data-value','data'),
# )
# def activate_pg2(data):
#     if data is not None:
#         return False
#     else:
#         return True
    

# @callback(
#     Output('navlink_pg30', 'disabled'),
#     [Input('retreinamentopg3-flag-check-json','data'),
#     Input('kappa_pred_UP_MAG_to_pg3','data')],
# )
# def activate_pg30(flag_load,data):
#     print(flag_load,type(flag_load), 'inside navbar')
#     if flag_load is None:
#             raise PreventUpdate
#     flag_load = json.loads(flag_load)
#     print(flag_load,type(flag_load), 'inside navbar 2')
    
#     if data is not None and flag_load:
#         return False
#     else:
#         return True
    
# @callback(
#     Output('navlink_pg3', 'disabled'),
#     Input('kappa_pred_UP_MAG_to_pg3','data'),
# )
# def activate_pg3(data):
#     # print(data, 'activatepg3 inside navbar')
#     if data is not None:
#         return False
#     else:
#         return True

# #-
# @callback(
#     Output('btn_pg30_home', 'disabled'),
#     [Input('retreinamentopg3-flag-check-json','data'),
#     Input('kappa_pred_UP_MAG_to_pg3','data')],
# )
# def activate_pg30(flag_load,data):
#     print(flag_load,type(flag_load), 'inside navbar')
#     if flag_load is None:
#             raise PreventUpdate
#     flag_load = json.loads(flag_load)
#     print(flag_load,type(flag_load), 'inside navbar 2')
    
#     if data is not None and flag_load:
#         return False
#     else:
#         return True
    
# @callback(
#     Output('btn_pg3_home', 'disabled'),
#     Input('kappa_pred_UP_MAG_to_pg3','data'),
# )
# def activate_pg3(data):
#     # print(data, 'activatepg3 inside navbar')
#     if data is not None:
#         return False
#     else:
#         return True

"""