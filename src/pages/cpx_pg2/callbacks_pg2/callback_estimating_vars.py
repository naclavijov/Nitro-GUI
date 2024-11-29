from dash import callback
from dash.exceptions import PreventUpdate
from dash.dependencies import Input,Output,State
import numpy as np
import pandas as pd
import dash
import plotly.graph_objs as go
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
import dash_mantine_components as dmc
import json

import base64
from io import BytesIO
import os
import joblib

import dash_daq as daq
from datetime import date, datetime



def get_param(ENT):
    dig_type = ENT
    data = joblib.load(os.path.join(os.getcwd(),'Backend','data','data.joblib'))

    if dig_type == 'AC':
        df = data.iloc[5:9,:]
    if dig_type == 'BC':
        df = data.iloc[10:14,:]
    if dig_type == 'CC':
        df = data.iloc[15:19,:]
    if dig_type == 'R':
        df = data.iloc[:4,:]
    if dig_type == 'S':
        df = data.iloc[20:24,:]
    if dig_type == 'T':
        df = data.iloc[25:29,:]
    if dig_type == 'Y':
        df = data.iloc[30:34,:]
    
    return df

def get_product(ENT2):
    prod_type = ENT2
    print(prod_type)
    if prod_type == '1/2 ES':
        i = 0
    if prod_type == '1/2 ES GC':
        i = 1
    if prod_type == '400 E S':
        i = 2
    if prod_type == '2000 ES':
        i = 3

    return i

def plot_profile(temperatura):
    
    fig = go.Figure()
    fig.update_layout(template = "Morph")
    fig.add_trace(go.Scatter(
    y = temperatura,
    mode = 'lines',
    name = 'Perfil projetado'
    ))
    fig.update_layout(
                    xaxis_title = "Tempo de batelada (min)",
                    yaxis_title = "Temperatura")

    fig.update_layout(
                margin=dict(l=5, r=5, t=5, b=5),
                legend_title_text='Comparação de perfil',
                legend = dict(orientation = 'h', 
                    xanchor = "left", 
                    # x = 0.04, y= 1.11,
                    font_size=12,
                    # bgcolor="#20374c",
                    bordercolor="White",
                    borderwidth=0.5)

            )
    
    # fig.update_layout(showlegend=False)
    
    return fig

def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y = []))
    fig.update_layout(template = "Morph")
    fig.update_xaxes(showgrid = False, showticklabels = False, zeroline=False)
    fig.update_yaxes(showgrid = False, showticklabels = False, zeroline=False)
    
    return fig

def get_callback_computing_estimation():
    @callback([Output('temp-calc','children'), Output('temp-calc-min','children'), 
            Output('temp-calc-max','children'),Output('col_container_pg2_plot', 'children'),
            Output('temperature_profile_computed_data','data'),
            Output('temp-calc','style'),Output('temp-calc-min','style'),Output('temp-calc-max','style')],
            [Input('calc-tempo-btn','n_clicks')],
            [State('dig-selector','value'), State('prod-selector','value'), 
            State('temperatura-patamar-value','value'), State('viscosidade-value','value'),
            State('tempo-rampa-value','value'),State('temperatura-rampa-value','value')],
                    prevent_initial_call=True )
    def calculos(n_clicks,ENT,ENT2,ENT3,ENT4,ENT5,ENT6):

        ctx = dash.callback_context

        if ctx.triggered[0]["prop_id"].split(".")[0] == 'calc-tempo-btn':
            pass
        else:
            raise PreventUpdate

        if not n_clicks:
            raise PreventUpdate

        df = get_param(ENT)
        i = get_product(ENT2)
        print('adijf')
        print(df)
        print(i)

        fig1 = blank_fig()
        
        temperatura_de_patamar = ENT3
        Visc_pretendida = ENT4

        tempo_de_rampa_real = ENT5
        temperatura_fim_rampa = ENT6

        b = df['b'][i]
        b_decomp =  df['bDESCOMP.'][i]
        a_decomp = df['aDESCOMP.'][i]

        bfH = df['bFH'][i]
        afH = df['aFH'][i]

        a = (temperatura_fim_rampa - 90)/tempo_de_rampa_real
        

        # print('a',a)
        # print('a',a_decomp)
        # print('issues')

        t99 = (99.0 - b)/a
        t99_decomp = (99.0 -b_decomp)/a_decomp


        FatorH_rampa = (a/2 * tempo_de_rampa_real**2 + b*tempo_de_rampa_real) - (a/2*t99**2 + b*t99) - 10*(tempo_de_rampa_real - t99)

        FatorH_decomp = (a_decomp/2)*t99_decomp**2 + b_decomp*t99_decomp

        Tempo_necessario = (((bfH - Visc_pretendida)/(-afH)) - FatorH_rampa -  FatorH_decomp)/temperatura_de_patamar
        Tempo_necessario = int(Tempo_necessario)
        Minimo = int(0.956*Tempo_necessario)
        Maximo = int(1.044*Tempo_necessario)

        temp0 = a*np.linspace(0,int(tempo_de_rampa_real),int(tempo_de_rampa_real)) + b
        temperature_profile = np.hstack([temp0,np.linspace(temperatura_fim_rampa,temperatura_fim_rampa,int(Tempo_necessario)),np.linspace(temperatura_fim_rampa,99,int(t99_decomp))])

        fig1 = plot_profile(temperature_profile)

        div_cont = [dbc.Row(dbc.Col([
                            dmc.Button("Comparar",id='comparar-tempo-btn',
                                                    disabled=False,
                                                    leftIcon=DashIconify(icon='teenyicons:git-compare-solid',width=25), size="md",
                                                    variant="gradient", gradient={"from": "teal", "to": "blue", "deg": 60})
                    ],width=3),justify='start'),
                    
                    dbc.Row(dbc.Col([dcc.Graph(id = 'plot02', figure = fig1),
                                    
                                    dbc.Modal([
                                        dbc.ModalHeader("Carregar Arquivo txt"),
                                        dbc.ModalBody([
                                            dcc.Upload(
                                                id="upload-data-pg2-sub",
                                                children=html.Div([
                                                    "Arraste e solte ou ",
                                                    html.A("selecione um arquivo de texto")
                                                ],style={'marginBottom':'4%'}),
                                                multiple=False,
                                            ),
                                            dcc.Loading(id='loading-load-msg-pg2-sub',
                                                # type='circle',
                                                type='dot',
                                                color='#003760',
                                                children=
                                                html.Div(id="output-data-upload-pg2-sub"))
                                        ]),
                                        dbc.ModalFooter([
                                            dbc.Button("Fechar", id="close-pg2-sub", className="btn btn-primary")
                                        ]),
                                    ],
                                    id="modal-pg2sub",
                                    size="lg"
                                    ),
                                    
                                    
                                    
                                    
                                    ],width=12),
                            justify='center',style={'marginTop':'1%'})
                    ]

        style = {'border-style': 'dashed', 'border-width': '2px','border-color': '#13B68A'}

        return (Tempo_necessario,Minimo,Maximo, div_cont,json.dumps(temperature_profile.tolist()),style,style,style)
    return