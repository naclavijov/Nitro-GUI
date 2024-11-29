import dash
# import dash_core_components as dcc
from dash import dcc
import dash_bootstrap_components as dbc
# import dash_html_components as html
from dash import html
from dash.exceptions import PreventUpdate
from dash.dependencies import Input,Output,State
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import json
from numpy import random
from dash_bootstrap_templates import load_figure_template
import dash_daq as daq
import datetime
load_figure_template(["minty"])

# from app import app


# Connect to your app pages
# from pages import page1,
# from pages import page2 #, page4
# from pages.cpx_pg3 import page3
from pages.cpx_pg1 import page1
from pages.cpx_pg2 import page2

from pages import home
# Connect the navbar to the index
from components import navbar
from utils.images import logo_nitro_encoded
# Define the navbar
nav = navbar


#-----
from app import app_builder
app = app_builder()
# server = app.server

# app = dash.Dash(__name__, use_pages=True, pages_folder="",external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])
# app.config.suppress_callback_exceptions = True
dash.register_page("Home", layout=home.layout)
dash.register_page("Page1", layout=page1.layout)
dash.register_page("Page2", layout=page2.layout)
#-----

logo_sidebar = html.A(

                html.Img(src=logo_nitro_encoded,className="w-100"),
                href='https://plotly.com',
                style={"textDecoration": "none",
                       'margin-right': '1px',
                       'verticalAlign': 'top',
                       'border-bottom': '0px solid black'},
            )



app.layout = html.Div(children=[

    dbc.Row([   
        # dbc.Navbar(children=[ 
        dbc.Card([ 
        dbc.CardHeader(children=[       
        html.A(
                dbc.Row([
                    # dbc.Col(html.Img(src=logo_nitro_encoded,className="w-100"),width=2,align="center",style={'margin-right': '5px','verticalAlign': 'top','border-right': '2px solid white'}),

                    dbc.Col(dbc.NavbarBrand(children = [html.H5("Companhia Nitro Química Brasileira",
                                                style={'color':'white','verticalAlign': 'top','margin-top': '10px','margin-left': '5px'})], style={'margin-top': '2px','verticalAlign': 'top'}),width=12,align="center", className="ms-2"),
                    
                    ],
                    align="center",
                    className="g-0",
                ),
                # href="/",
                href='https://plotly.com',
                style={"textDecoration": "none"},
            )]
            ,
            style={
                    "border-radius": "1px",
                    "border-width": "2px",
                    "border-bottom": "2px solid black",
                    "backgroundColor": '#003760',
                })
        ],color='primary')
            ],align="center"),
    dbc.Row([
    dcc.Store(id='digest-loaddata-pg1',storage_type='session'),
    dcc.Store(id='digest-loaddata-pg2',storage_type='session'),
    dcc.Store(id='temperature_profile_computed_data',storage_type='session'),
    dcc.Location(id='url', refresh=False),
    ]),


    dbc.Row([dbc.Col([dbc.Row(children=[logo_sidebar])],width=2), 
                dbc.Col([dbc.Row()],width=10)],
                align='start', style={"display": "inlineBlock",
                            "marginTop": "1%"
                        }),
    # dbc.Row(dbc.Col(html.Hr(style={'borderWidth': "0.3vh", "width": "100%","opacity":"1"}),width=2),
    #         align='start', style={"display": "inlineBlock",
    #                         "marginTop": "0%"
    #                     }), 

    dbc.Row([dbc.Col([dbc.Row(children=[nav])],width=2), 
            dbc.Col([dbc.Row([html.Div(id='page-content', children=[])])],width=10)],
            align='start', style={"display": "inlineBlock",
                        "marginTop": "0%"
                    })

    , 
])


@app.callback(Output('page-content', 'children'),
            [Input('url', 'pathname')],
            prevent_initial_call=True
            )
def display_page(pathname):

    options = []

    if pathname == '/': #/home
        return home.layout
    if pathname == '/page1':
        return page1.layout
    if pathname == '/page2':
        return page2.layout
    else: # if redirected to unknown link
        return "404 Page Error! Please choose a link"


if __name__ == "__main__":
    app.run_server()

# if __name__ == "__main__":
#     app.run_server(debug=True)

    