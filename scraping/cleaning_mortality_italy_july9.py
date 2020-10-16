# coding=utf-8
import numpy as np
import pandas as pd
import json

with open("../data/Italy/translate.json") as ff:
    translate = json.load(ff)


translate_initalian = {'REGIONE':'codice_regione', 
            'NOME_REGIONE':'denominazione_regione',
             'PROVINCIA':'codice_provincia', 
             'NOME_PROVINCIA':'denominazione_provincia'}


weeks = ['01/01/2015-11/01/2015', '12/01/2015-18/01/2015',
         '19/01/2015-25/01/2015', '26/01/2015-01/02/2015',
         '02/02/2015-08/02/2015', '09/02/2015-15/02/2015',
        '16/02/2015-22/02/2015', '23/02/2015-29/02/2015',
         '01/03/2015-07/03/2015', '08/03/2015-14/03/2015',
         '15/03/2015-21/03/2015', '22/03/2015-28/03/2015',
         '29/03/2015-04/04/2015', '05/04/2015-11/04/2015',
         '12/04/2015-18/04/2015',
         '19/04/2015-25/04/2015',
         '26/04/2015-02/05/2015',
         '03/05/2015-09/05/2015',
         '10/05/2015-16/05/2015',
         '17/05/2015-23/05/2015',
         '24/05/2015-30/05/2015']


def regional(cls=1):

    df = pd.read_csv('../data/Italy/july9_total_deaths_2015-2020/dati-mortalità-comuni_giornalieri-al_31maggio.csv', encoding='latin1')
    df = df.rename(columns={'NOME_COMUNE':'town', 'NOME_REGIONE':'region', 'NOME_PROVINCIA':'province', 'CL_ETA':'ages', 'GE':'dates'})
    df = df[df['TIPO_COMUNE'] == 1]
    df = df[df['dates'] <=531]
    dfcut = df[df['T_20'] != 'n.d.']


    colsave = ['week', 'region', 'age_group', 'male', 'female', 'total']
    dfsave = pd.DataFrame(columns=colsave, dtype=None)
    ages = np.arange(22)
    years = [15, 16, 17, 18, 19, 20]
    dates = [[101, 111], [112, 118], [119, 125], [126, 201], [202, 208], [209, 215], [216, 222], [223, 229],
             [301, 307], [308, 314], [315, 321], [322, 328], [329, 404], [405, 411],  [412, 418],
             [419, 425],
             [426, 502],
             [503, 509],
             [510, 516],
             [517, 523],
             [524, 530]]
    
    
    for year in years:
        cols = ['M_%d'%year, 'F_%d'%year, 'T_%d'%year]
        for cc in cols:
            dfcut[cc] = dfcut[cc].astype(int)

    regions = np.unique(df['region'].values)
    for region in regions: 
    #for region in ['Abruzzo']: 
        print(region)
        tmp = dfcut[dfcut['region'] == region]
        
        for ia, age in enumerate(ages):
            tmpa = tmp[(tmp['ages'] == age)]
            for year in years:
                cols = ['M_%d'%year, 'F_%d'%year, 'T_%d'%year]
                weeklabel = [i[:8] + '%d'%year + i[10:-2]+ '%d'%year for i in weeks]
                
                for iw, week in enumerate(weeks):
                    #if (cls == 2) & (week.split('/')[3] == '04'): continue                    
                    tmpw = tmpa[(tmpa['dates'] >= dates[iw][0]) & (tmpa['dates'] <= dates[iw][1])]
                    deaths = tmpw[cols].sum().astype(float).tolist()
                    entry = np.array([weeklabel[iw], region, ia] + deaths).reshape(1, -1)
                    dfsave = dfsave.append(pd.DataFrame(entry, columns=colsave), ignore_index=True)
                    
    dfsave['age_group'] = dfsave['age_group'].astype(int) 
    dfsave['male'] = dfsave['male'].astype(float) 
    dfsave['female'] = dfsave['female'].astype(float) 
    dfsave['total'] = dfsave['total'].astype(float)     

    dfsave = dfsave.replace('Friuli-Venezia Giulia', 'Friuli Venezia Giulia')
    dfsave = dfsave.replace("Valle d'Aosta/Vallée d'Aoste", "Valle d'Aosta")
    dfsave.to_csv('../data//Italy/july9_total_deaths_2015-2020/regional_historic_mortality.tsv', sep='\t', encoding='utf-8')

    


def pop_ratio(cls=1, poplim = None):
    #df = pd.read_excel('/home/chirag/Research/Projects/covid-19-data/data/Italy/new_total_deaths_2015_2020/raw_mortality_data/dati-comunali-settimanali-ANPR-1/comuni_settimana.xlsx', encoding='latin1')
    #df = pd.read_excel('../data/Italy/april4_total_deaths_2015-2020/raw_data/comuni-settimana/comuni_settimana.xlsx')
    df = pd.read_csv('../data/Italy/july9_total_deaths_2015-2020/dati-mortalità-comuni_giornalieri-al_31maggio.csv', encoding='latin1')
    df = df.rename(columns={'GE':'dates'})
    df = df[df['dates'] <=531]
    df = df[df['T_20'] != 'n.d.']
    
    df2 = pd.read_excel('/home/chirag/Research/Projects/covid-19-data/data/Italy/Elenco-comuni-italiani.xls', encoding='latin1')
    df2 = df2.rename(columns={'Popolazione legale 2011 (09/10/2011)':'population'})
    df2 = df2.rename(columns={'Codice Comune formato alfanumerico':'commune_code'})
    regions = np.unique(df['NOME_REGIONE'].values)
    
    savecols = ['REG', 'region', 'total_commune', 'mortality_commune', 'total_population', 'mortality_population', 'completeness']
    dfsave = pd.DataFrame(columns=savecols)
    
    dfpoptown = pd.read_excel('../../covid-19-data/data/Italy/Elenco-comuni-italiani.xls')
    dfpoptown = dfpoptown.rename(columns={'Denominazione in italiano':'town', 'Popolazione legale 2011 (09/10/2011)':'population'})
    poptownd  = dict(dfpoptown[['town', 'population']].values)
    pops = np.array([poptownd[i] for i in df['NOME_COMUNE'].values])
    if poplim is not None: df = df[pops > poplim]

    regcodes = {}
    for i in range(1, 21): regcodes[df[df['REG'] == i]['NOME_REGIONE'].values[0]] = i
    
    for _, region in enumerate(regions):
        ir = regcodes[region]
        tmp = df[df['REG'] == ir]
        tmp2 = df2[df2['Codice Regione'] == ir]
        total_pop = float(tmp2.sum()['population'])
        ccode2 = np.unique(tmp2['commune_code'].values)
        popdict = dict(tmp2[['commune_code', 'population']].values)

        ccode = np.unique(tmp['COD_PROVCOM'].values)
        pop = 0
        for cc in ccode: 
            pop += popdict[cc]

        tosave = np.array([ir+1, region, ccode2.size, ccode.size, total_pop, pop, "%0.3f"%(pop/total_pop)]).reshape(1, -1)
        dfsave = dfsave.append(pd.DataFrame(tosave, columns=savecols))
        
    dfsave = dfsave.replace('Friuli-Venezia Giulia', 'Friuli Venezia Giulia')
    dfsave = dfsave.replace("Valle d'Aosta/Vallée d'Aoste", "Valle d'Aosta")

    dfsave['completeness'] = dfsave['completeness'].astype(float) 
    dfsave['total_population'] = dfsave['total_population'].astype(float) 
    dfsave['mortality_population'] = dfsave['mortality_population'].astype(float) 
    #dfsave.to_csv('../data/Italy/new_total_deaths_2015_2020/regional_population_fraction.tsv', sep='\t', encoding='utf-8')
    if poplim is not None: dfsave.to_csv('../data/Italy/july9_total_deaths_2015-2020/regional_population_fraction_%d.tsv'%poplim, sep='\t', encoding='utf-8')
    else: dfsave.to_csv('../data/Italy/july9_total_deaths_2015-2020/regional_population_fraction.tsv', sep='\t', encoding='utf-8')

    


if __name__=="__main__":

    #pop_ratio()
    regional()
    
