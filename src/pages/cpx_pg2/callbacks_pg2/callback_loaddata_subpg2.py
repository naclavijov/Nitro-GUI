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
import json
import dash_mantine_components as dmc
from dash import no_update
import base64
from io import BytesIO
import os

import dash_daq as daq

# from Backend.source.Class_Case import Case


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

def plot_profile_comparison(temperatura_exp,temperatura_comp):
    
    fig = go.Figure()
    fig.update_layout(template = "Morph")
    fig.add_trace(go.Scatter(
    y = temperatura_comp,
    mode = 'lines',
    name = 'Perfil projetado'
    ))
    fig.add_trace(go.Scatter(
    y = temperatura_exp,
    mode = 'markers',
    name = 'Perfil experimental'
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

def div_function(fig):
    div_cont = [dbc.Row(dbc.Col([
            dmc.Button("Visualizar comparação",id='visualizar_comp-temp-btn',
                                    disabled=False,
                                    leftIcon=DashIconify(icon='game-icons:all-seeing-eye',width=25), size="md",
                                    variant="gradient", gradient={"from": "teal", "to": "blue", "deg": 60})
    ],width=3),justify='start'),

    dbc.Row(dbc.Col([dcc.Graph(id = 'plot03', figure = fig)],width=12),
            justify='center',style={'marginTop':'1%'})
    ]
    return div_cont

def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    if 'txt' in filename:
        df = pd.read_csv(BytesIO(decoded),  header=None)
        print(df.head())
        msg = html.Div([
            dbc.Alert(
                        [
                            html.H4("Ótimo!", className="alert-heading"),
                            html.P(
                                "O arquivo (txt) com os dados de digestão de comparação foi carregado com sucesso. "
                                "Ao fechar este quadro de dialogo estará habilitado um botão  "
                                "de visualização e comparação das curvas de digestão carregada e simulada."
                            ),
                            html.Hr(),
                            html.P(
                                "Este quadro de dialogo poderá ser fechado com um click",
                                "ou atomaticamente em 9 segundos",
                                className="mb-0",
                            ),
                        ],
                    color="success",
                    dismissable=True,
                    duration=9000)
        ],style={'martginTop':'2%'})
    
    
    else:
        df = pd.DataFrame()
        msg = html.Div([
            dbc.Alert(
                        [
                            html.H4("Mmmm!", className="alert-heading"),
                            html.P(
                                "O arquivo (txt) com os dados de digestão de comparação não foi carregado com sucesso, "
                                "verifique se o mesmo se encontra na formatação requerida ou se  "
                                "está corrompido."
                            ),
                            html.Hr(),
                            html.P(
                                "Este quadro de dialogo poderá ser fechado com um click",
                                "ou atomaticamente em 9 segundos",
                                className="mb-0",
                            ),
                        ],
                    color="danger",
                    dismissable=True,
                    duration=9000)
        ])
    
    return df , msg
    
def get_callback_nodal():
    @callback(
        Output("modal-pg2sub", "is_open"),
        Output("output-data-upload-pg2-sub", "children",allow_duplicate=True),
        Input("comparar-tempo-btn", "n_clicks"),
        Input("close-pg2-sub", "n_clicks"),
        State("modal-pg2sub", "is_open"),
        State("upload-data-pg2-sub", "contents"),
        State("upload-data-pg2-sub", "filename"),
        prevent_initial_call=True
    )
    def toggle_modal(n1, n2, is_open,contents,  filename):

        if n1 or n2:
            return not is_open, None
        return is_open, None
    return


def get_callback_content():
    # Primeiro dcc Store para almazenar o dataframe raw e gerar os options para os Dropdown menus (Store Callback)
    @callback(
            # [Output('digest-loaddata-pg2', 'data'), Output("output-data-upload-pg2-sub", "children")],
            [Output("output-data-upload-pg2-sub", "children"),
            Output('digest-loaddata-pg2', 'data')],
            [Input("upload-data-pg2-sub", "contents")], [State("upload-data-pg2-sub", "filename")],
                    prevent_initial_call=True)
    def update_output(contents, filename):

        df = pd.DataFrame()
        if contents == None or filename==None is None:
            raise PreventUpdate
        else:
            df, children = parse_contents(contents, filename)
            # some expensive data processing step by ex:
            # cleaned_df = slow_processing_step(value)
            
            # more generally, this line would be
            # json.dumps(cleaned_df)

            temperatura_comparison_exp = df.iloc[:,1].values
            #--------------------------------------------------------
            '''
            Continuar fazendo o plot com 2 tracas, a saida deste callback nao precisa ser mais
            um store e sim diretamente o plot
            '''
            #

        print(df.head(),'parasite')

        # return (df.to_json(date_format='iso', orient='split'),children)
        return (children,json.dumps(temperatura_comparison_exp.tolist()))
    return


#------------

def get_callback_div_content2():
    @callback(
    # [Output('digest-loaddata-pg2', 'data'), Output("output-data-upload-pg2-sub", "children")],
    Output('col_container_pg2_plot', 'children',allow_duplicate=True),
    [Input("modal-pg2sub", "is_open")], #Input('close-pg2-sub','n_clicks'),
    [State('digest-loaddata-pg2', 'data'),State('temperature_profile_computed_data', 'data')],
            prevent_initial_call=True)
    def update_output(modal_isopen,temperature_exp_js, temperature_comp_js):
        if temperature_comp_js is None or temperature_exp_js is None:
            raise PreventUpdate
        if modal_isopen is None:
            raise PreventUpdate
        temperature_computed_profile = json.loads(temperature_comp_js)
        # ctx = dash.callback_context
        # if ctx.triggered[0]["prop_id"].split(".")[0] == 'close-pg2-sub':
        #     fig1 = plot_profile(temperature_computed_profile)
        #     div_content = div_function(fig1)
        #     return div_content
        if modal_isopen:
            return no_update
        else:
            fig1 = plot_profile(temperature_computed_profile)
            div_content = div_function(fig1)
            return div_content
    return


def get_callback_plot_comparison():
    @callback(
        Output('plot03','figure'),
        [Input('visualizar_comp-temp-btn', "n_clicks")], 
        [State('temperature_profile_computed_data', 'data'),State('digest-loaddata-pg2', 'data')],
        prevent_initial_call=True)
    def update_output(n_clicks_comp,temperature_comp_js,temperature_exp_js):
        if n_clicks_comp is None:
            raise PreventUpdate
        if None in [temperature_comp_js,temperature_exp_js]:
            raise PreventUpdate
        
        ctx = dash.callback_context
        if ctx.triggered[0]["prop_id"].split(".")[0] == 'visualizar_comp-temp-btn':
            fig = plot_profile_comparison(json.loads(temperature_exp_js),json.loads(temperature_comp_js))
            return fig
        else:
            no_update
    return



