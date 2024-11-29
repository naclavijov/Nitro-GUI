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

import base64
from io import BytesIO
import os

import dash_daq as daq

# from Backend.source.Class_Case import Case


def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    print('filename',filename)
    if 'txt' in filename:
        df = pd.read_csv(BytesIO(decoded),  header=None,index_col=0)
        df.index = pd.to_datetime(df.index,dayfirst=True)

        df.columns = ['Temperatura(°C)']   

        # Pretreatment based on ocurrencs
        df = df[~df.index.duplicated(keep='first')]

        msg = html.Div([
            dbc.Alert(
                        [
                            html.H4("Ótimo!", className="alert-heading"),
                            html.P(
                                "O arquivo (txt) com os dados de digestão foi carregado com sucesso, "
                                "ao fechar este quadro de dialogo estará habilitado o botão  "
                                "de visualização da curva de digestão."
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
                                "O arquivo (txt) com os dados de digestão não foi carregado com sucesso, "
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
        Output("modal", "is_open"),
        Output("output-data-upload", "children",allow_duplicate=True),
        Input("open", "n_clicks"),
        Input("close", "n_clicks"),
        State("modal", "is_open"),
        State("upload-data", "contents"),
        State("upload-data", "filename"),
        prevent_initial_call=True
    )
    def toggle_modal(n1, n2, is_open,contents,  filename):

        if n1 or n2:
            return not is_open, None
        return is_open, None
    return


def get_callback_content():
    # Primeiro dcc Store para almazenar o dataframe raw e gerar os options para os Dropdown menus (Store Callback)
    @callback([Output('digest-loaddata-pg1', 'data'), Output("output-data-upload", "children")],
            [Input("upload-data", "contents")], State("upload-data", "filename"),
                    prevent_initial_call=True)
    def update_output(contents, filename):

        df = pd.DataFrame()
        if contents == None or filename==None:
            raise PreventUpdate
        else:
            df, children = parse_contents(contents, filename)
            # some expensive data processing step by ex:
            # cleaned_df = slow_processing_step(value)
            
            # more generally, this line would be
            # json.dumps(cleaned_df)

        return (df.to_json(date_format='iso', orient='split'),children)
    return


#------------


