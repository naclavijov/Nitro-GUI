import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from dash.dependencies import Input, Output, State
from dash import callback

import dash_mantine_components as dmc
from dash_iconify import DashIconify

from dash.exceptions import PreventUpdate

from datetime import date, datetime

import dash_daq as daq

import pandas as pd
import numpy as np
import plotly.graph_objects as go

import base64
from io import BytesIO

from .callbacks_pg1 import callback_loaddata, callback_plotting_data

load_figure_template(["Morph"])
# load_figure_template(["Minty"])


cabecalho = dbc.Card(className='bg-light',
    children=[
    
        dbc.CardHeader(
            # className='bg-primary',
            children=[html.H2( "Visualização e cálculo do Fator H", id='my_header', style={'display':'inline-block'})],
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

info_box = dbc.Card(className='card text-black bg-secondary mb-3', #'bg-light mb-3',
                    style={'border': '3px solid'},
                    children =[
                        dbc.CardHeader(
                            "Entre com o perfil de temperatura da batelada",
                            style = {
                                "text-align": "center",
                                "color": "black",
                                "border-radius":"1px",
                                "border-width":"5px",
                                "border-top":"1 px solid rgb(216, 216, 216)"
                            }
                        ),
                        dbc.CardBody(
                            dbc.Row([
                                # html.Div(
                                dbc.Col([
                                    # dbc.Button('Carregar',id = 'open'),
                                    dmc.Button("Carregar dados",id='open',
                                                leftIcon=DashIconify(icon='fa-solid:file-upload',width=20), size="md",
                                                color='#23a847',variant="gradient", gradient={"from": "teal", "to": "lime", "deg": 105}),
                                    dbc.Modal([
                                        dbc.ModalHeader(dbc.CardHeader(children="Carregar Arquivo txt",
                                                                    className="card-title",)),
                                        dbc.ModalBody([
                                            dcc.Upload(
                                                id="upload-data",
                                                children=html.Div([
                                                    "Arraste e solte ou ",
                                                    html.A("selecione um arquivo de texto")
                                                ],style={'marginBottom':'4%'}),
                                                multiple=False,
                                            ),
                                            dcc.Loading(id='loading-load-msg',
                                                # type='circle',
                                                type='dot',
                                                color='#003760',
                                                children=
                                                html.Div(id="output-data-upload"))
                                        ]),
                                        dbc.ModalFooter([
                                            dbc.Button("Fechar", id="close", className="btn btn-primary")
                                        ]),
                                    ],
                                    id="modal",
                                    size="lg"
                                    ),
                                    # dcc.Store stores the intermediate value
                                    dcc.Store(id='intermediate-value'),
                                    # dcc.Store stores the segregated value
                                    dcc.Store(id='segregated-value')]
                                , width=3),
                            
                            dbc.Col([dmc.Button("Visualizar curva",id='visualizar_data_digesta_pg1',
                                    disabled=False,
                                    leftIcon=DashIconify(icon='cib:mathworks',width=25), size="md",
                                    variant="gradient", gradient={"from": "orange", "to": "red"})
                                ],width=3)

                            ],justify='evenly')
                        )
                    ])


def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y = []))
    fig.update_layout(template = "Morph")
    fig.update_xaxes(showgrid = False, showticklabels = False, zeroline=False)
    fig.update_yaxes(showgrid = False, showticklabels = False, zeroline=False)

    return fig


get_predictionLIG = dbc.Card(className = 'bg-light mb-3',
                             children = [
                                 dbc.CardHeader(
                            "Fator H",
                            style = {
                                "text-align": "center",
                                "color": "black",
                                "border-radius":"1px",
                                "border-width":"5px",
                                "border-top":"1 px solid rgb(216, 216, 216)",
                                "backgroundColor": '#008131'
                            }
                        ),
                             dbc.CardBody(
                                    dbc.Row(
                                        html.Div(
                                            id = 'pred_fatorH',
                                            children = None, 
                                            style = {"text-align": "center"}
                                        )
                                    ),
                                style={"backgroundColor":'#D9E3F1'}
                                )
                                ],

)

get_predictionLIG2 = dbc.Card(className = 'bg-light mb-3',
                             children = [
                                 dbc.CardHeader(
                            "Temperatura do patamar (°C)",
                            style = {
                                "text-align": "center",
                                "color": "black",
                                "border-radius":"1px",
                                "border-width":"5px",
                                "border-top":"1 px solid rgb(216, 216, 216)",
                                "backgroundColor": '#008131'
                            }
                        ),
                             dbc.CardBody(
                                    dbc.Row(
                                        html.Div(
                                            id = 'pred_init',
                                            children = None, 
                                            style = {"text-align": "center"}
                                        )
                                    )
                                ,style={"backgroundColor":'#D9E3F1'}
                                )
                                ]

)

get_predictionLIG3 = dbc.Card(className = 'bg-light mb-3',
                             children = [
                                 dbc.CardHeader(
                            "Duração do patamar (min)",
                            style = {
                                "text-align": "center",
                                "color": "black",
                                "border-radius":"1px",
                                "border-width":"5px",
                                "border-top":"1 px solid rgb(216, 216, 216)",
                                "backgroundColor": '#008131'

                            }
                        ),
                             dbc.CardBody(
                                    dbc.Row(
                                        children= html.Div(
                                            id = 'pred_dur',
                                            children = None, 
                                            style = {"text-align": "center",
                                                    # 'width':'100%'
                                                    }
                                        ),
                                    # style={'width':'100%'}
                                    )
                                ,style={"backgroundColor":'#D9E3F1',
                                        # 'width':'100%'
                                        }
                                )
                                ],
# style = {'width':'100%'}
)





# Styling parameters:
# colors = {'background': '#F5CFF7','text':'#A939AD '}




layout = dbc.Container(fluid = True,
                        children = [
                            cabecalho,
                            dbc.Row(
                                [
                                    dbc.Col( 
                                        [
                                            dbc.Row(
                                                dbc.Col(info_box, width = 12)
                                            ),
                                            dbc.Row(
                                                dbc.Col(
                                                    #    dcc.Graph(id = 'plot01',figure = blank_fig()), width = 12
                                                    dcc.Loading(id='loading-figure-visualization-pg2',
                                                                    # type='circle',
                                                                    type='cube',
                                                                    color='#003760',
                                                                    children=dcc.Graph(id = 'plot01',figure = blank_fig()))
                                                                    , width = 12
                                                )
                                            ),
                                            
                                            dbc.Row([
                                                dbc.Col(get_predictionLIG,width = 4)
                                                ,
                                                dbc.Col(get_predictionLIG2,width = 4),
                                                dbc.Col(get_predictionLIG3,width = 4)
                                            ]
                                            )
                                        ]
                                    )
                                ]
                            )
                        ])

callback_loaddata.get_callback_nodal()
callback_loaddata.get_callback_content()

callback_plotting_data.get_callback_plotting()