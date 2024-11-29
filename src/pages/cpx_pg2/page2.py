import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash import callback

import pandas as pd
import numpy as np
import plotly.graph_objects as go

import base64
from io import BytesIO
import joblib

from .callbacks_pg2 import callback_estimating_vars
from .callbacks_pg2 import callback_loaddata_subpg2

load_figure_template(["Morph"])

def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y = []))
    fig.update_layout(template = "Morph")
    fig.update_xaxes(showgrid = False, showticklabels = False, zeroline=False)
    fig.update_yaxes(showgrid = False, showticklabels = False, zeroline=False)
    
    return fig


cabecalho = dbc.Card(className='bg-light',
    children=[
    
        dbc.CardHeader(
            # className='bg-primary',
            children=[html.H2( 'Ferramenta de referência - Tempo de patamar', id='my_headerpg2', style={'display':'inline-block'})],
            style={
                "height":"100%",
                "text-align": "center",
                "color": "white",
                "border-radius":"2px",
                "border-width":"0px",
                "backgroundColor": '#003760'
                # "backgroundColor": "black",
                # "backgroundColor": '#78C2AD',
            },
        ),



    ],
style={"height":"100%","border-radius":"1px","border-width":"5px",})




    


info_box1 = dbc.Card(className="card text-black bg-secondary mb-4",
                                    style={'border': '3px solid'}, 
                    children =[
                        dbc.CardHeader(
                            "Escolha com as informações de referência",
                            style = {
                                "text-align": "center",
                                "color": "black",
                                "border-radius":"1px",
                                "border-width":"5px",
                                "border-top":"1 px ",
                               
                            }
                        ),
                        dbc.CardBody(
                                    dbc.Row([
                                        dbc.Col([
                                            dbc.Row(
                                                html.Div(children ="Escolha o digestor", style = {
                                "text-align": "center"} )
                                            ),
                                            dbc.Row(
                                                html.Div(
                                                    children = [
                                                        html.Div(
                                                            id = 'div-digestor-selector',
                                                            children = [
                                                                
                                                                dcc.Dropdown(
                                                                    id = 'dig-selector',
                                                                    options = [{"label":"AC", "value": "AC"}, {"label": "BC", "value": "BC"}, {"label": "CC", "value": "CC"},
                                                                    {"label": "R", "value": "R"} ,{ "label": "S", "value":"S"}, {"label":"T", "value": "T"}, {"label": "Y", "value": "Y"}],
                                                                    multi = False
                                                                )
                                                            ]
                                                        )
                                                    ]
                                                )
                                            )
                                    ]),
                                        dbc.Col([
                                            dbc.Row(
                                                html.Div(children ="Escolha o produto" ,style = {
                                "text-align": "center"})
                                            ),
                                            dbc.Row(
                                                html.Div(
                                                    children = [
                                                        html.Div(
                                                            id = 'div-product-selector',
                                                            children = [
                                                                
                                                                dcc.Dropdown(
                                                                    id = 'prod-selector',
                                                                    options = ["1/2 ES", "1/2 ES GC", "400 ES", "2000 ES"],
                                                                    multi = False
                                                                )
                                                            ]
                                                        )
                                                    ]
                                                )
                                            )
                                            

                                    ])
                    ])
                                    )
                                
                    ])

info_box2 = dbc.Card(className='card text-black bg-secondary mb-3', 
                                style={'border': '3px solid',
                                        },
                    children =[
                        dbc.CardHeader(
                            "Entre com as informações da operação",
                            style = {
                                "text-align": "center",
                                "color": "black",
                                "border-radius":"1px",
                                "border-width":"5px",
                                "border-top":"1 px"
                                
                            }
                        ), 
                        dbc.CardBody(
                            dbc.Row([
                                dbc.Col(
                                    [
                                        dbc.Row([
                                            html.Div(
                                                id = 'Div-temperatura-patamar',
                                                children = [
                                                    html.Label(["Temperatura do",html.Br(), "patamar [°C]"]),
                                                    # dmc.Text("Temperatura do patamar em °C",c='dimmed',size='md'),
                                                    # dcc.Input(
                                                    #     id = 'temperatura-patamar-value',
                                                    #     type = "number"
                                                    # )
                                                    dmc.NumberInput(
                                                        id = 'temperatura-patamar-value',
                                                        min=1,
                                                        step=1,
                                                    ),
                                                    dbc.Tooltip(
                                                        ["Temperatura do patamar [°C]",
                                                        html.Br(),
                                                        "Insera um valor positivo (°C)"],
                                                        target='temperatura-patamar-value',
                                                        placement="bottom"
                                                    )
                                                ], style = {
                                "text-align": "center"}
                                            )
                                        ]
                                            
                                        )
                                        
                                    ]
                                ),
                                dbc.Col([
                                    dbc.Row([
                                            html.Div(
                                                id = 'Div-viscosidade',
                                                children = [
                                                    html.Label(["Viscosidade",html.Br(),"desejada [cP]"]),
                                                    # dcc.Input(
                                                    #     id = 'viscosidade-value',
                                                    #     type = "number"
                                                    # )
                                                    dmc.NumberInput(
                                                        id = 'viscosidade-value',
                                                        min=1,
                                                        step=1,
                                                    ),
                                                    dbc.Tooltip(
                                                        ["Viscosidade desejada [cP]",
                                                        html.Br(),
                                                        "Insera um valor positivo (cP)"],
                                                        target='viscosidade-value',
                                                        placement="bottom"
                                                    )
                                                ], style = {
                                "text-align": "center"}
                                            )
                                        ])
                                ]),
                                dbc.Col([
                                    dbc.Row([
                                            html.Div(
                                                id = 'Div-tempo-rampa',
                                                children = [
                                                    html.Label(["Tempo real",html.Br(),"de rampa [min]"]),
                                                    # dcc.Input(
                                                    #     id = 'tempo-rampa-value',
                                                    #     type = "number"
                                                    # )
                                                    dmc.NumberInput(
                                                        id = 'tempo-rampa-value',
                                                        min=1,
                                                        step=1,
                                                    ),
                                                    dbc.Tooltip(
                                                        ["Tempo real de rampa [min]",
                                                        html.Br(),
                                                        "Insera um valor positivo (min)"],
                                                        target='tempo-rampa-value',
                                                        placement="bottom"
                                                    )
                                                ], style = {
                                "text-align": "center"}
                                            )
                                        ])
                                ]),
                                dbc.Col([
                                    dbc.Row([
                                            html.Div(
                                                id = 'Div-temperatura-rampa',
                                                children = [
                                                    html.Label(["Temperatura ao final",html.Br(),"da rampa [°C]"]),
                                                    # dcc.Input(
                                                    #     id = 'temperatura-rampa-value',
                                                    #     type = "number",
                                                    #     min=90
                                                    # )
                                                    dmc.NumberInput(
                                                        id = 'temperatura-rampa-value',
                                                        min=91,
                                                        step=1,
                                                    ),
                                                    dbc.Tooltip(
                                                        ["Temperatura ao final da rampa [°C]",
                                                        html.Br(),
                                                        "Insera um valor maior do que 90 °C"
                                                        "e menor do que a temperatura do patamar."],
                                                        target='temperatura-rampa-value',
                                                        placement="bottom"
                                                    )
                                                ], style = {
                                "text-align": "center"}
                                            )
                                        ])
                                ])
                    ,
                    dbc.Row(
                                html.Div(
                                    [
                                    dmc.Button("Calcular",id='calc-tempo-btn',
                                    disabled=False,
                                    leftIcon=DashIconify(icon='ph:math-operations-fill',width=25), size="md",
                                    variant="gradient", gradient={"from": "orange", "to": "yellow"}),

                                    dcc.Loading(id='loading-load-msg_pg2',
                                                # type='circle',
                                                type='dot',
                                                color='#003760',
                                                children=
                                                html.Div(id="output-data-upload_pg2"))

                                    
                                    ],style = {"text-align": "center",
                                            
                                            "marginTop":25}
                                )
                            )])
                        )
                    ])

info_box3 = dbc.Card(className='card text-black bg-secondary mb-3', style={'border': '3px solid'
                                        },
                    children =[
                        dbc.CardHeader(
                            "Predição do tempo de patamar",
                            style = {
                                "text-align": "center",
                                "color": "black",
                                "border-radius":"1px",
                                "border-width":"5px",
                                "border-top":"1 px"
                                
                            }
                        ), 
                        dbc.CardBody([
                            
                            dbc.Row(
                                [
                                    dbc.Col(
                                        html.Label("Tempo necessário de patamar (min)"),
                                        width=2
                                    ),
                                    dbc.Col(
                                        html.Div(
                                            id='temp-calc',
                                            children = None,
                                            # style = {'border-style': 'dashed', 'border-width': '3px', 'border-left-width': '10px', 'border-right-width': '10px',
                                            # 'border-color': 'rgb(9,37,54)'}
                                        )
                                    ,width=2
                                    ),
                                    dbc.Col(
                                        html.Label("Tempo mínimo de patamar (min)")
                                        ,width=2
                                    ),
                                    dbc.Col(
                                        html.Div(
                                            id='temp-calc-min',
                                            children = None,
                                            # style = {'border-style': 'dashed', 'border-width': '3px', 'border-left-width': '10px', 'border-right-width': '10px',
                                            # 'border-color': 'rgb(9,37,54)'}
                                        )
                                        ,width=2
                                    ),
                                    dbc.Col(
                                        html.Label("Tempo máximo de patamar (min)")
                                        ,width=2
                                    ),
                                    dbc.Col(
                                        html.Div(
                                            id='temp-calc-max',
                                            children = None,
                                            # style = {'border-style': 'dashed', 'border-width': '3px', 'border-left-width': '10px', 'border-right-width': '10px',
                                            # 'border-color': 'rgb(9,37,54)'}
                                        )
                                        ,width=2
                                    )
                                ]
                            ,align='center'
                            ),

                            
                            
                            
                            ],style = {
                                "text-align": "center"}
                        )
                    ])

info_box4 = dbc.Card(className='card secundary mb-3', style={'border': '3px solid'
                                        },
                    children =[
                        dbc.CardHeader(
                            "Curvas perfil de temperatura",
                            style = {
                                "text-align": "center",
                                "color": "black",
                                "border-radius":"1px",
                                "border-width":"5px",
                                "border-top":"1 px"
                                
                            }
                        ),
                        dbc.CardBody(
                            dbc.Row(
                                dbc.Col(
                                    id='col_container_pg2_plot',
                                    children=[]
                                    # dcc.Graph(id = 'plot02', figure = blank_fig())
                                )
                            )
                        )
                    ])
    

# info_box4 = dbc.Card(className='card secundary mb-3', style={'border': '5px solid',
#                                         'border-color':'#B83C08'},
#                     children =[
#                         dbc.CardHeader(
#                             "Coluna de visualização de alguma coisa",
#                             style = {
#                                 "text-align": "center",
#                                 "color": "white",
#                                 "border-radius":"1px",
#                                 "border-width":"5px",
#                                 "border-top":"1 px",
#                                 'background-color': '#B83C08'
#                             }
#                         ),
#                         dbc.CardBody(
#                             html.P("Ferramenta de predição desenvolvida pela Nitroquímica"), style = {'background-color':'#EB5406'}
#                         )
#                     ])



layout = dbc.Container(fluid = True,
                           children = [
                               cabecalho,
                               dbc.Row([
                                    dbc.Col([
                                        dbc.Row(
                                            dbc.Col(info_box1, width = 12)
                                        ),
                                        dbc.Row(
                                            dbc.Col(info_box2, width = 12)
                                        ),
                                        dbc.Row([
                                            dbc.Col(info_box3, width = 12)
                                        ]),
                                        dbc.Row([
                                            dbc.Col(info_box4, width = 12)
                                        ])
                                    ])
                               ])
                           ])


callback_estimating_vars.get_callback_computing_estimation()

callback_loaddata_subpg2.get_callback_nodal()
callback_loaddata_subpg2.get_callback_content()
callback_loaddata_subpg2.get_callback_div_content2()
callback_loaddata_subpg2.get_callback_plot_comparison()    

