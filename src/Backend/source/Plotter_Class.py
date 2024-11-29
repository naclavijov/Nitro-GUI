import numpy as np
import pandas as pd
from scipy import integrate
import os
import base64
from io import BytesIO
from datetime import date,datetime
import matplotlib.pyplot as plt
import kaleido
import plotly.graph_objects as go
from statsmodels.tsa.stattools import kpss, adfuller

import warnings
from statsmodels.tools.sm_exceptions import InterpolationWarning
warnings.simplefilter('ignore', InterpolationWarning)
warnings.simplefilter('ignore', UserWarning)

class Plotter():
    def __init__(self,digestion_id,user,date,extracomments):
        self.digestion_id = digestion_id
        self.user = user
        self.date = date
        self.extracomments = extracomments
        self.temperature_digest_bound = 100

        self.df_f = None

    def load_data(self, filename_data, convert_index_to_datetime = True):
        """ Carregar conjunto de dados 

        :param filename_data: nome do arquivo que contem os dados
        :type filename_data: str
        :param convert_index_to_datetime: indica se o índice do conjunto de dados deve ser convertido a datetime, defaults to False
        :type convert_index_to_datetime: bool, optional
        :raises TypeError: erro indicando uma extensão inválida para o arquivo
        :return: retorna um DataFrame com os dados
        :rtype: DataFrame
        """
        self.filename_data = filename_data

        if self.filename_data.endswith(".txt"):
            self.df_f =pd.read_csv(os.path.join(os.getcwd(),'data','data_digestions',self.filename_data), index_col=0,header=None)
        elif self.filename_data.endswith(".hdf"):
            self.df_f = pd.read_hdf(os.path.join(os.getcwd(),'data','data_digestions',self.filename_data))
        elif self.filename_data.endswith(".xlsx"):
            self.df_f =pd.read_excel(os.path.join(os.getcwd(),'data','data_digestions',self.filename_data), index_col=0) 
        elif self.filename_data.endswith(".csv"):
            self.df_f =pd.read_csv(os.path.join(os.getcwd(),'data','data_digestions',self.filename_data), index_col=0)
        elif self.filename_data.endswith(".pkl"):
            self.df_f =pd.read_pickle(os.path.join(os.getcwd(),'data','data_digestions',self.filename_data))
        else:
            raise TypeError('The dataframe file is not sopported, try with files txt,hdf, xlsx, csv, or pkl')
        
        if convert_index_to_datetime:
            self.df_f.index = pd.to_datetime(self.df_f.index,dayfirst=True)

        self.df_f.columns = ['Temperatura(°C)']   

        # Pretreatment based on ocurrencs
        self.df_f = self.df_f[~self.df_f.index.duplicated(keep='first')]
        return self.df_f
    
    def detect_level0(self,mode,window_size=4,threshold=0.2):

        if mode == 'sorting':
            df_f =self.df_f.sort_values('Temperatura(°C)',ascending=False)
        else:
            df_f = self.df_f

        rolling_mean = df_f[df_f['Temperatura(°C)'] > 0].rolling(window=window_size).mean()
        # rolling_mean = df_f[df_f['Temperatura(°C)'] > self.temperature_digest_bound].rolling(window=window_size).mean()
        rolling_diff = rolling_mean.diff()

        constant_points = rolling_diff.abs() < threshold


        # Encontrar o primeiro ponto onde a série fica aproximadamente constante
        idx = constant_points[constant_points['Temperatura(°C)']==True].index[0]
        level = df_f.loc[idx,'Temperatura(°C)']
        return level
    
    def detect_level(self,mode,window_size=5):
        if mode == 'sorting':
            df_f = self.df_f.sort_values('Temperatura(°C)',ascending=False)
        else:
            df_f = self.df_f
        rolling_var = df_f[df_f['Temperatura(°C)'] > self.temperature_digest_bound].rolling(window=window_size).var()

        if mode == 'sorting':
            idx = rolling_var.index[0]

        else:
            idx = rolling_var.idxmin()[0]

        level = df_f.loc[idx,'Temperatura(°C)']

        return level
    
    def adf_test(self,timeseries):
        dftest = adfuller(timeseries, autolag="AIC")
        dfoutput = pd.Series(
            dftest[0:4],
            index=[
                "Test Statistic",
                "p-value",
                "#Lags Used",
                "Number of Observations Used",
            ],
        )
        for key, value in dftest[4].items():
            dfoutput["Critical Value (%s)" % key] = value
        return dfoutput['p-value']

    def kpss_test(self,timeseries):
        # https://mlpills.dev/time-series/stationarity-in-time-series-and-how-to-check-it/
        # https://www.statsmodels.org/stable/examples/notebooks/generated/stationarity_detrending_adf_kpss.html
        kpsstest = kpss(timeseries, regression="c", nlags="auto")
        kpss_output = pd.Series(
            kpsstest[0:3], index=["Test Statistic", "p-value", "Lags Used"]
        )
        for key, value in kpsstest[3].items():
            kpss_output["Critical Value (%s)" % key] = value

        return kpss_output['p-value']
    
    def detect_level_adf(self,mode,window_size=10):
        if mode == 'sorting':
            df_f = self.df_f.sort_values('Temperatura(°C)',ascending=False)
        else:
            df_f = self.df_f

        df_rolled_adf = df_f[df_f['Temperatura(°C)'] > self.temperature_digest_bound].rolling(window=window_size).apply(self.adf_test)
        # Agora a coluna 'Temperatura(°C)' corresponde aos p-values
        if mode == 'sorting':
            idx = df_rolled_adf.index[0]
        else:
            idx = df_rolled_adf.idxmin()[0]
        level = df_f.loc[idx,'Temperatura(°C)']
        return level
    
    def detect_level_kpss(self,mode,window_size=10):
        if mode == 'sorting':
            df_f = self.df_f.sort_values('Temperatura(°C)',ascending=False)
        else:
            df_f = self.df_f

        df_rolled_kpss = df_f[df_f['Temperatura(°C)'] > self.temperature_digest_bound].rolling(window=window_size).apply(self.kpss_test)        
        # Agora a coluna 'Temperatura(°C)' corresponde aos p-values
        if mode == 'sorting':
            idx = df_rolled_kpss.index[0]
        else:
            idx = df_rolled_kpss.idxmin()[0]
        level = df_f.loc[idx,'Temperatura(°C)']
        return level
    
    def level_duration(self,Temp_tol):
        self.Temp_tol = Temp_tol
        mode = 'sorting'
        self.level_low_crit = self.detect_level(mode)
        df = self.df_f[(self.df_f['Temperatura(°C)'] >= self.level_low_crit - Temp_tol) & (self.df_f['Temperatura(°C)'] <= self.level_low_crit + Temp_tol)]
        self.init_level = self.df_f.index.get_loc(df.index[0])
        self.init_level_idx = df.index[0] 
        self.final_level_idx = df.index[-1]
        self.level_dur = (df.index[-1] -df.index[0]).total_seconds()/60
        self.ramp_dur = (df.index[0] - self.df_f[self.df_f['Temperatura(°C)'] > self.temperature_digest_bound].index[0] ).total_seconds()/60
        self.descomp_dur = (self.df_f[self.df_f['Temperatura(°C)'] > self.temperature_digest_bound].index[-1] - df.index[-1]).total_seconds()/60
        
        # print(self.init_level,df.index[-1])
        # print(self.level_dur)

            
    
    def plot_profile(self,name='test_plot'):
        plotfile = os.path.join(os.getcwd(),'data','curve_plots',name+'.png')
        mode = 'no_sorting'
        mode = 'sorting'
        self.level_low_crit = self.detect_level(mode)
        # print('lower var', self.level_low_crit)
        try:
            self.level_adf = self.detect_level_adf(mode)
        except:
            self.level_adf = self.level_low_crit 
        # print('adf',self.level_adf)
        try:
            self.level_kpss = self.detect_level_kpss(mode)
        except:
            self.level_kpss = self.level_low_crit 
        # print('kpss',self.level_kpss)
        self.level_first_cri = self.detect_level0(mode)
        # print('first valid', self.level_first_cri)
        self.temperatura = self.df_f.loc[:,'Temperatura(°C)'].values
        # self.temperatura = self.df_f.iloc[:,0].values
        fig = go.Figure()
        fig.add_trace(go.Scatter(
        y = self.temperatura,
        mode = 'lines',
        name = 'Dado exp'
        ))


        
        fig.update_layout(template = "Morph")
        
        fig.update_layout(title="Dado carregado",
                        title_x = 0.5,
                            xaxis_title = "Tempo de batelada (min)",
                            yaxis_title = "Temperatura") 
        # fig.add_hline(y=self.level, line_width=3, line_dash="dash", line_color="green")

        fig.add_trace(go.Scatter(x=[0,self.df_f.shape[0]], 
                        y=[self.level_first_cri,self.level_first_cri], 
                        mode='lines', 
                        line=dict(color='green', width=3, dash='dash'),
                        name='First valid Criteria'))

        fig.add_trace(go.Scatter(x=[0,self.df_f.shape[0]], 
                        y=[self.level_low_crit,self.level_low_crit], 
                        mode='lines', 
                        line=dict(color='red', width=3, dash='dash'),
                        name='Low variance Criteria'))
        
        fig.add_trace(go.Scatter(x=[0,self.df_f.shape[0]], 
                        y=[self.level_adf,self.level_adf], 
                        mode='lines', 
                        line=dict(color='black', width=3, dash='dash'),
                        name='ADF Criteria'))
        
        fig.add_trace(go.Scatter(x=[0,self.df_f.shape[0]], 
                        y=[self.level_kpss,self.level_kpss], 
                        mode='lines', 
                        line=dict(color='black', width=3, dash='dash'),
                        name='KPSS Criteria'))
        Temp_tol = self.Temp_tol

        fig.add_shape(type="rect",
            x0=int(self.init_level), y0=self.level_low_crit - Temp_tol, x1=int(self.init_level+self.level_dur), y1=self.level_low_crit + Temp_tol,
            line=dict(
                color="RoyalBlue",
                width=2,
            ),
            opacity=0.5,
            layer="below", line_width=0,
            fillcolor="orange",
        )
        

        fig.update_layout(showlegend=True)
        # fig.write_image(plotfile) 
        # fig.show()
        
        return fig
    
    def H_factor(self,method_int='trapz'):

        if method_int =='trapz':
            Hfactor = self.df_f[self.df_f['Temperatura(°C)'] > self.temperature_digest_bound].apply(integrate.trapezoid,axis=0)
            self.Hfactor = Hfactor.values[0]
        elif method_int =='cum_trapz':
            Hfactor = self.df_f[self.df_f['Temperatura(°C)'] > self.temperature_digest_bound].apply(integrate.cumulative_trapezoid,axis=0)
            self.Hfactor = Hfactor['Temperatura(°C)'].values[-1]
        elif method_int =='simpson':
            Hfactor = self.df_f[self.df_f['Temperatura(°C)'] > self.temperature_digest_bound].apply(integrate.simpson,axis=0)
            self.Hfactor = Hfactor.values[0]
        else:
            Hfactor = self.df_f[self.df_f['Temperatura(°C)'] > self.temperature_digest_bound].apply(np.trapz,axis=0)
            self.Hfactor = Hfactor.values[0]
        return self.Hfactor
    
    def H_factor_segment(self,method_int='trapz'):

        idx_T =self.df_f.columns.get_loc('Temperatura(°C)')
        self.df_r = self.df_f[self.df_f['Temperatura(°C)'] > self.temperature_digest_bound]

        if method_int =='trapz':
            Hfactor_ramp = self.df_r.loc[:self.init_level_idx,:].apply(integrate.trapezoid,axis=0)
            Hfactor_level = self.df_r.loc[self.init_level_idx:self.final_level_idx,:].apply(integrate.trapezoid,axis=0)
            Hfactor_descomp = self.df_r.loc[self.final_level_idx:,:].apply(integrate.trapezoid,axis=0)

            self.Hfactor_ramp = Hfactor_ramp.values[0]
            self.Hfactor_level = Hfactor_level.values[0]
            self.Hfactor_descomp = Hfactor_descomp.values[0]
        elif method_int =='cum_trapz':
            Hfactor_ramp = self.df_r.loc[:self.init_level_idx,:].apply(integrate.cumulative_trapezoid,axis=0)
            Hfactor_level = self.df_r.loc[self.init_level_idx:self.final_level_idx,:].apply(integrate.cumulative_trapezoid,axis=0)
            Hfactor_descomp = self.df_r.loc[self.final_level_idx:,:].apply(integrate.cumulative_trapezoid,axis=0)

            self.Hfactor_ramp = Hfactor_ramp.values[-1]
            self.Hfactor_level = Hfactor_level.values[-1]
            self.Hfactor_descomp = Hfactor_descomp.values[-1]

        elif method_int =='simpson':
            Hfactor_ramp = self.df_r.loc[:self.init_level_idx,:].apply(integrate.simpson,axis=0)
            Hfactor_level = self.df_r.loc[self.init_level_idx:self.final_level_idx,:].apply(integrate.simpson,axis=0)
            Hfactor_descomp = self.df_r.loc[self.final_level_idx:,:].apply(integrate.simpson,axis=0)

            self.Hfactor_ramp = Hfactor_ramp.values[0]
            self.Hfactor_level = Hfactor_level.values[0]
            self.Hfactor_descomp = Hfactor_descomp.values[0]

        else:
            Hfactor_ramp = self.df_r.loc[:self.init_level_idx,:].apply(np.trapz,axis=0)
            Hfactor_level = self.df_r.loc[self.init_level_idx:self.final_level_idx,:].apply(np.trapz,axis=0)
            Hfactor_descomp = self.df_r.loc[self.final_level_idx:,:].apply(np.trapz,axis=0)

            self.Hfactor_ramp = Hfactor_ramp.values[0]
            self.Hfactor_level = Hfactor_level.values[0]
            self.Hfactor_descomp = Hfactor_descomp.values[0]

        return self.Hfactor_ramp,self.Hfactor_level,self.Hfactor_descomp


# digestion_id='a'
# user='nayher'
# date=datetime.now().date()
# extracomments='None'
# plot_obj = Plotter(digestion_id,user,date,extracomments)
# # plot_obj.load_data('dados_teste.txt')
# # plot_obj.load_data('Amostra 60.txt')
# plot_obj.load_data('Amostra 01.txt')

# H = plot_obj.H_factor(method_int ='trapz')
# plot_obj.level_duration(Temp_tol=5)
# print(H)

# H1,H2,H3 =plot_obj.H_factor_segment(method_int ='trapz')
# print(H1,H2,H3,(H1+H2+H3))

# plot_obj.plot_profile()

# dff=plot_obj.df_f.loc[plot_obj.df_f['Temperatura(°C)'] > plot_obj.temperature_digest_bound]
# print(dff,dff.shape)
# print(plot_obj.df_f)


