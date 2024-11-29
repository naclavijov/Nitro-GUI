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
from datetime import date, datetime

from Backend.source import Plotter_Class


def plot_profile(temperatura):
    fig = go.Figure()
    fig.update_layout(template = "Morph")
    fig.add_trace(go.Scatter(
    y = temperatura,
    mode = 'lines'
    ))

    fig.update_layout(
            title="Dado carregado",
            title_x = 0.5,
            xaxis = dict(title='Tempo de batelada (min)',
                # backgroundcolor="rgb(200, 200, 230)",
                # gridcolor="white",
                # showbackground=True,
                # zerolinecolor="white",
                ),
            yaxis = dict(
                title="Temperatura (°C)",
                # backgroundcolor="rgb(230, 200,230)",
                # gridcolor="white",
                # showbackground=True,
                # zerolinecolor="white"
                ),
                
                # height=250,
                ) 

    return fig


def get_callback_plotting():
    @callback([Output('plot01', 'figure'),Output("pred_fatorH", "children"),
            Output("pred_init", "children"),Output("pred_dur", "children")], 
            [Input('visualizar_data_digesta_pg1', "n_clicks")], State('digest-loaddata-pg1', 'data'),
                    prevent_initial_call=True)
    def predict_output(nclicks_vis, data_js):
        if nclicks_vis is None or data_js is None:
            raise PreventUpdate
        
        Plotter_obj = Plotter_Class.Plotter(digestion_id='Test',user='User',date=datetime.now(),extracomments='None')
        
        df = pd.read_json(data_js, orient='split')

        Plotter_obj.df_f =  df

        H = Plotter_obj.H_factor(method_int ='trapz')
        Plotter_obj.level_duration(Temp_tol=5)

        fig1 = Plotter_obj.plot_profile()
        


        iniPat = Plotter_obj.init_level
        TempPat = Plotter_obj.level_low_crit
        durPat = np.round(Plotter_obj.level_dur,2)



        #--------

        temperatura = df.iloc[:,0].values

        print(len(temperatura))


        Time_indicator =    daq.Gauge(
            # color={"gradient":True,"ranges":{"green":[0,6],"yellow":[6,8],"red":[8,10]}},
            color = '#7CC823',
            # color={
            #     "gradient": True,
            #     "ranges": {"green": [0, 2000], "red": [2000, 10000]},
            # },
            # color ={"gradient":True,"ranges":{"green":[0,6],"yellow":[6,8],"red":[8,10]}}
            # scale={"start": 0, "interval": 75, "labelInterval": 2},
            size=230,
            value=durPat,
            min=0,
            max=(df.index[-1] -df.index[0]).total_seconds()/60, #(btime-atime).seconds/60,
            showCurrentValue=True,
            units="Minutos",
            # style={"width": "100%"}
        )

        Temperature_indicator = daq.Thermometer(
                        min=np.round(np.amin(temperatura),1),
                        max=np.round(np.amax(temperatura),1),
                        value=TempPat,
                        showCurrentValue=True,
                        units="°C",
                        color = '#e52527',
                        className='dark-theme-control')

        print(H,'numb')

        FatorHdiv = daq.LEDDisplay(
            value=round(H,2),
            color='#003760',
            backgroundColor='#D9E3F1'
            # className='dark-theme-control'
        )
        
        return fig1, FatorHdiv, Temperature_indicator,Time_indicator
    return