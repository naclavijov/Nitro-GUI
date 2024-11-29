import dash
from dash import callback
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
load_figure_template(["slate"])
import numpy as np
import pandas as pd
import json
from numpy import random

import dash_mantine_components as dmc
from dash_iconify import DashIconify


from dash.exceptions import PreventUpdate
from dash.dependencies import Input,Output,State
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots


from utils.images import logo_nitro_encoded,logo_senai_encoded, logo_embrapii_encoded

import dash_daq as daq
import datetime
# from app import app
# from layouts import layout

#-----------------

# package imports
import base64
import os

# logo information
cwd = os.getcwd()





#-----------------

def logo():
    # asses_path = os.getcwd() +'/src/new_assets'
    title = html.H5(children=[
        "INTERFACE DE VISUALIZAÑÇÃO E CÁLCULO DO FATOR H - NITROQUÍMICA"],
        style={"marginTop": 5, "marginLeft": "10px",'color':'#ccc'},
    )

    info_about_app = html.H6(children=[
        "Este Dashboard está destinado apresentar a visualização e cálculo do fator H"
        " Os resultados são apresentados interativamente baseado na inserção de entradas"],
        style={"marginLeft": "10px", "font-size":"13px", 'color':'#bbb'},
    )

    # logo_image = html.Img(
    #     src=dash.get_asset_url("logo_INOVA3.png"), style={"float": "right", "height": 50,'marginTop':5}
    # )

    logo_image = html.Img(
        src=r'assets/logos/Nitroquimica_logo2.png', style={"float": "right", "height": 80,'marginTop':5}
    )

    link = html.A(logo_image, href="https://plotly.com/dash/")

    return dbc.Row(
        # [dbc.Col([dbc.Row([title]), dbc.Row([info_about_app])]), dbc.Col(link)]
        [dbc.Col([dbc.Row([title]), dbc.Row([info_about_app])])]
    )

def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y = []))
    fig.update_layout(template = "slate")
    fig.update_xaxes(showgrid = False, showticklabels = False, zeroline=False)
    fig.update_yaxes(showgrid = False, showticklabels = False, zeroline=False)
    
    return fig


graphs = dbc.Card(#className='bg-dark border-primary mb-3',
                  className= 'mb-3',
    children=[
        dbc.CardBody(
            [
                html.Div(
                    [
                        dcc.Graph(
                            id="Main-Graph-home",
                            figure=blank_fig() #Analise.figure5(kappa_pred_UP_MAG,u_pred_UP_MAG)
                            # figure=figure4(FullNp_u_prinN)
                            # config={"displayModeBar": True},
                        ),
                    ],
                    style={"width": "98%", "display": "inline-block"},
                ),
            ],
            style={
                # "backgroundColor": "black",
                'border-color':'#78C2AD',
                "border-radius": "1px",
                "border-width": "5px",
                "border": "1px solid rgb(120, 194, 173)",
            },
        )
    ],style={"backgroundColor":'#343A40'}
)


setup_title_box = dbc.Card(className='bg-light',
    children=[
    
        dbc.CardHeader(
            # className='bg-primary',
            children=[html.H1( "Estimador - Fator H", id='my_h1', style={'display':'inline-block', 'color':'white'})],
            style={
                "height":"100%",
                "text-align": "center",
                "color": "black",
                # "backgroundColor": "black",
                "backgroundColor": '#003760',
                "border-radius": "1px",
                "border-width": "5px",
                "border-top": "1px solid rgb(216, 216, 216)",
            },
        ),

        dbc.CardBody([dcc.Markdown(children = '''
            > __Estimador - Fator H__ é uma ferramenta computacional desenvolvida pela equipe técnica da Nitroquímica para prever o fator H com base em um modelo interno. 
                                   O software foi criado utilizando a biblioteca Dash-Plotly Open Source em Python. Esta página oferece uma visão geral da interface e suas principais funcionalidades.
                                   Na aba “Visualização”, o usuário pode avaliar a curva de temperatura de uma digestão já realizada e obter informações relevantes sobre a corrida. 
                                   Já na aba “Predição”, o usuário pode determinar o tempo adequado de patamar, baseado nas informações da digestão, para atingir a qualidade especificada, 
                                   além de visualizar as curvas teórica e real de temperatura.


                ''',style={'text-align':'justify'})],
                # style={"backgroundColor":'#343A40'}
                )

    ],
style={"height":"100%"})



logos_plots= html.Div(
                    [
                    dbc.Row([dbc.Col(html.Img(src=logo_senai_encoded, style={'width':'100%'}),width=12),
                            
                                    ], align="center",
                                    className="g-0",
                                    justify='end',
                                    style={
                                        "marginTop": "0%"
                                    },),
                    dbc.Row([
                            dbc.Col([],width=2),
                            dbc.Col(html.Img(src=logo_embrapii_encoded, style={'width':'100%'}),width=8),
                            dbc.Col([],width=2)
                                    ], align="center",
                                    className="g-0",
                                    justify='end',
                                    style={
                                        "marginTop": "5%"
                                    },)

                    ],
                    style={"width": "98%", "display": "inline-block"},
                ),

card_icon = {
    "color": "white",
    "textAlign": "center",
    "fontSize": 30,
    "margin": "auto",
}

cards_functionality = dbc.CardGroup(
    [

#
dbc.Card(
        [   
            dbc.Row([dbc.CardHeader(dmc.Anchor(dmc.Button('Visualização de dados',size="lg",variant="gradient",
                                            gradient={"from": "orange", "to": "red"},style={'width': '100%'},disabled=False),href='/page1')
                    ,className="col-md-8",style={'width': '100%'})],
                                    className="g-0 d-flex align-items-center",
                                    style={'border-left': '5px solid',
                                        'border-left-color':'#d9534f'}),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.CardImg(
                            src="/assets/static/simple-icons--alwaysdata_color.svg",
                            className="img-fluid rounded-start", 
                            style={'width':'90%',"marginLeft": "10%"}
                            
                        ),
                        className="col-md-4",
                    ),
                    dbc.Col(
                        
                        dbc.CardBody(
                            [
                                # dmc.Text("This is a wider card with supporting text "
                                #     "below as a natural lead-in to additional "
                                #     "content. This content is a bit longer.",
                                #     className="animate__animated animate__fadeInUp animate__slow",
                                #     style={'border-top':'2px solid white'}
                                # ),
                                html.P(
                                    # "This is a wider card with supporting text "
                                    # "below as a natural lead-in to additional "
                                    # "content. This content is a bit longer.",

                                    "A aba de visualização tem como objetivo"
                                    "o carregamento, limpeza e pre-tratamento de"
                                    "dados, assim como a visualização de varíaveis.",
                                    className="card-text",
                                    style={'border-top':'2px solid white'}
                                ),
                                html.Small(
                                    "Last updated 3 mins ago",
                                    className="card-text text-muted",
                                ),
                            ],#className='border-start border-white border-1'
                        ),
                        className="col-md-8",
                    ),
                ],
                className="g-0 d-flex align-items-center",
                style={'border-left': '5px solid',
                       'border-left-color':'#d9534f'}
            )
        ],
        className="mb-3",
        style={"maxWidth": "540px"},
    ),
#
            dbc.Card(
        [   
            dbc.Row([dbc.CardHeader(dmc.Anchor(dmc.Button('Predição via ML',id='btn_pg2_home',size="lg",variant="gradient",
                                        gradient={"from": "teal", "to": "lime"},style={'width': '100%'},disabled=True),href='/page2')
                    ,className="col-md-8",style={'width': '100%'})],
                                    className="g-0 d-flex align-items-center",
                                    style={'border-left': '5px solid',
                                        'border-left-color':'#20c997'}),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.CardImg(
                            src="/assets/static/carbon--machine-learning-model_color.svg",
                            className="img-fluid rounded-start",
                            style={'width':'90%',"marginLeft": "10%"}
                        ),
                        className="col-md-4",
                    ),
                    dbc.Col(
                        
                        dbc.CardBody(
                            [
                                html.P(
                                    # "This is a wider card with supporting text "
                                    # "below as a natural lead-in to additional "
                                    # "content. This content is a bit longer.",

                                    "A aba de predição ML tem como objetivo"
                                    "o treinamento de modelos ML internos e a"
                                    "exibição de métricas de ajustes dos conjuntos",
                                    className="card-text",
                                    style={'border-top':'2px solid white'}
                                ),
                                html.Small(
                                    "Last updated 3 mins ago",
                                    className="card-text text-muted",
                                ),
                            ],#className='border-start border-white border-1'
                        ),
                        className="col-md-8",
                    ),
                ],
                className="g-0 d-flex align-items-center",
                style={'border-left': '5px solid',
                       'border-left-color':'#20c997'}
            )
        ],
        className="mb-3",
        style={"maxWidth": "540px"},
    ),
#
            
#---
dbc.Card(
        [   
            dbc.Row([dbc.CardHeader(dmc.Anchor(dmc.Button('Re-Treinamento',id='btn_pg30_home',size="lg",variant="gradient",
                                                gradient={"from": "indigo", "to": "cyan"},style={'width': '100%'},disabled=True),href='\home')
                    ,className="col-md-8",style={'width': '100%'})],
                                    className="g-0 d-flex align-items-center",
                                    style={'border-left': '5px solid',
                                        'border-left-color':'#4c9be8'}),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.CardImg(
                            src="/assets/static/fa--gears_color.svg",
                            className="img-fluid rounded-start",
                            style={'width':'90%',"marginLeft": "10%"}
                        ),
                        className="col-md-4",
                    ),
                    dbc.Col(
                        
                        dbc.CardBody(
                            [
                                html.P(
                                    # "This is a wider card with supporting text "
                                    # "below as a natural lead-in to additional "
                                    # "content. This content is a bit longer.",

                                    "A aba re-treinamento tem como objetivo a"
                                    "obtenção das métricas de desempenho do"
                                    "modelo ML nos conjuntos de treino e teste",
                                    className="card-text",
                                    style={'border-top':'2px solid white'}
                                ),
                                html.Small(
                                    "Last updated 3 mins ago",
                                    className="card-text text-muted",
                                ),
                            ],#className='border-start border-white border-1'
                        ),
                        className="col-md-8",
                    ),
                ],
                className="g-0 d-flex align-items-center",
                style={'border-left': '5px solid',
                       'border-left-color':'#4c9be8'}
            )
        ],
        className="mb-3",
        style={"maxWidth": "540px"},
    ),

#-
dbc.Card(
        [   
            dbc.Row([dbc.CardHeader(dmc.Anchor(dmc.Button('Análise de influências',id='btn_pg3_home',size="lg",variant="gradient",
                                        gradient={"from": "yellow", "to": "orange"},style={'width': '100%'},disabled=True),href='/page4')
                    ,className="col-md-8",style={'width': '100%'})],
                                    className="g-0 d-flex align-items-center",
                                    style={'border-left': '5px solid',
                                        'border-left-color':'#ffc107'}),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.CardImg(
                            src="/assets/static/fluent-mdl2--test-step_color.svg",
                            className="img-fluid rounded-start",
                            style={'width':'90%',"marginLeft": "10%"}
                        ),
                        className="col-md-4",
                    ),
                    dbc.Col(
                        
                        dbc.CardBody(
                            [
                                html.P(
                                    # "This is a wider card with supporting text "
                                    # "below as a natural lead-in to additional "
                                    # "content. This content is a bit longer.",

                                    "A aba de análise de influências tem como objetivo"
                                    "a geração de disturbios nas variáveis primarias"
                                    "e a obtenção das respostas das varíaveis do sistema",
                                    className="card-text",
                                    style={'border-top':'2px solid white'}
                                ),
                                html.Small(
                                    "Last updated 3 mins ago",
                                    className="card-text text-muted",
                                ),
                            ],#className='border-start border-white border-1'
                        ),
                        className="col-md-8",
                    ),
                ],
                className="g-0 d-flex align-items-center",
                style={'border-left': '5px solid',
                       'border-left-color':'#ffc107'}
            )
        ],
        className="mb-3",
        style={"maxWidth": "540px"},
    ),


    ]
)

gauge_size = "auto"
sidebar_size = 12
graph_size = 10
layout = dbc.Container(
    fluid=True,
    children=[

        dbc.Row(
            [
                dbc.Col(
                    [   
                        dbc.Row(dbc.Col(setup_title_box,
                                        width=sidebar_size),
                                style={'marginTop':'0%',"marginBottom": "0%"},justify='end'),
                    ], width=10
                ),

                dbc.Col(
                    [   
                        dbc.Row(dbc.Col(logos_plots))]
                ,width=2)


                ],
                justify='end',
                style={"display": "inlineBlock",
                        "marginTop": "0%"
                    }),

        ]
)

