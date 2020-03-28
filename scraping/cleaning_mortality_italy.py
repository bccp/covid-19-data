import numpy as np
import pandas as pd
import json

with open("../data/Italy/translate.json") as ff:
    translate = json.load(ff)


translate_initalian = {'REGIONE':'codice_regione', 
            'NOME_REGIONE':'denominazione_regione',
             'PROVINCIA':'codice_provincia', 
             'NOME_PROVINCIA':'denominazione_provincia'}

def province():

    dfread = pd.read_excel('../data/Italy/mortality_data/totali_provinciali.xlsx')

    dfsave = pd.DataFrame()

    for year in [2015, 2016, 2017, 2018, 2019]:
        for i, datestamp in enumerate(pd.date_range('1/1/%d'%year, '30/4/%d'%year)):
            d = dfread[dfread['MESE_DECESSO'] == datestamp.month]
            d = d[d['GIORNO_DECESSO'] == datestamp.month]
            d = d[['REGIONE', 'NOME_REGIONE', 'PROVINCIA', 'NOME_PROVINCIA', 'DECESSI_%d'%year]]
            d['data'] = datestamp
            for key in translate_initalian: d.rename(columns={key:translate_initalian[key]}, inplace=True)
            d.rename(columns={'DECESSI_%d'%year:'deceduti'}, inplace=True)
            dfsave = dfsave.append(d, ignore_index = True)

    for key in translate:
        try:    dfsave.rename(columns = {key:translate[key]}, inplace=True)
        except: pass
    dfsave.to_csv('../data/Italy/province_historical_mortality.tsv', sep='\t', encoding='utf-8')

def regional():

    dfread = pd.read_excel('../data/Italy/mortality_data/totali_regionali.xlsx')

    dfsave = pd.DataFrame()
    for year in [2015, 2016, 2017, 2018, 2019]:
        for i, datestamp in enumerate(pd.date_range('1/1/%d'%year, '30/4/%d'%year)):
            d = dfread[dfread['MESE'] == datestamp.month]
            d = d[d['GIORNO'] == datestamp.month]
            d = d[['REGIONE', 'NOME_REGIONE', 'DECESSI_%d'%year]]
            d['data'] = datestamp
            for key in translate_initalian: d.rename(columns={key:translate_initalian[key]}, inplace=True)
            d.rename(columns={'DECESSI_%d'%year:'deceduti'}, inplace=True)
            dfsave = dfsave.append(d, ignore_index = True)

    for key in translate:
        try:    dfsave.rename(columns = {key:translate[key]}, inplace=True)
        except: pass
    dfsave.to_csv('../data/Italy/regional_historical_mortality.tsv', sep='\t', encoding='utf-8')



if __name__=="__main__":

    province()
    regional()
