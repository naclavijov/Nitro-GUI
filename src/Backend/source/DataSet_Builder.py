import numpy as np
import pandas as pd
from scipy import integrate
import os
import base64
from io import BytesIO
from datetime import date,datetime
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from Plotter_Class import Plotter


class DataSet_Builder():

    def Sheet_reader(self):
        """ Carregar conjunto de dados 

        :param filename_data: nome do arquivo que contem os dados
        :type filename_data: str
        :param convert_index_to_datetime: indica se o índice do conjunto de dados deve ser convertido a datetime, defaults to False
        :type convert_index_to_datetime: bool, optional
        :raises TypeError: erro indicando uma extensão inválida para o arquivo
        :return: retorna um DataFrame com os dados
        :rtype: DataFrame
        """

        filename=(os.path.join(os.getcwd(),'data','Planilha_registro_de_experimentos.xlsx'))
        self.df_raw =pd.read_excel(filename,index_col=1,sheet_name='Hoja1',skiprows=[0])    
        return self.df_raw

    def Pretreatment(self):
        df = self.df_raw.drop(self.df_raw[self.df_raw['Data Experimento (Digestão)'].isin([None,'DEU ERRADO'])].index,inplace=False)
        first_idx = self.df_raw.index.difference(df.index).tolist()

        df = df[df['Data Experimento (Digestão)'].notna()]
        df = df[df['Tipo de produto'].notna()]

        self.experiments_removed = self.df_raw.index.difference(df.index).tolist() 

        self.treated_df = df

        print('Foram removidos os seguintes ' + str(len(self.experiments_removed)) + 'experimentos: ' + str(self.experiments_removed))


    def Computing_curve_properties(self):

            digestion_id='a'
            user='nayher'
            date=datetime.now().date()
            extracomments='None'
            plot_obj = Plotter(digestion_id,user,date,extracomments)
            datadir= os.path.join(os.getcwd(),'data','data_digestions')

            for filedir in os.listdir(datadir):
                print(filedir)
                if filedir == 'Amostra 23 - Correto.txt':
                    continue
                
                idx = int(filedir.split('.')[0].split('Amostra ')[1])
                plot_obj.load_data(filedir)

                H = plot_obj.H_factor(method_int ='trapz')
                plot_obj.level_duration(Temp_tol=5)
                H1,H2,H3 =plot_obj.H_factor_segment(method_int ='trapz')

                plot_obj.plot_profile(name='Sample_'+str(idx)+'.png')

                self.treated_df.loc[idx,'HFactor_total'] = H
                self.treated_df.loc[idx,'HFactor_ramp'] = H1
                self.treated_df.loc[idx,'HFactor_level'] = H2
                self.treated_df.loc[idx,'HFactor_descomp'] = H3
                self.treated_df.loc[idx,'Temperature_level_computed'] = plot_obj.level_low_crit
                self.treated_df.loc[idx,'ramp_time'] = plot_obj.ramp_dur
                self.treated_df.loc[idx,'descomp_time'] = plot_obj.descomp_dur
                self.treated_df.loc[idx,'level_time'] = plot_obj.level_dur

            self.treated_df.to_csv('FinalDataset.csv')



Dataset = DataSet_Builder()
Dataset.Sheet_reader()
Dataset.Pretreatment()
Dataset.Computing_curve_properties()
