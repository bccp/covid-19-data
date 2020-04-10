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
    dfsave.to_csv('../data/Italy/province_historic_mortality.tsv', sep='\t', encoding='utf-8')

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
    dfsave.to_csv('../data/Italy/regional_historic_mortality.tsv', sep='\t', encoding='utf-8')

    
def province_new():
    #df = pd.read_excel('/home/chirag/Research/Projects/covid-19-data/data/Italy/new_total_deaths_2015_2020/raw_mortality_data/dati-comunali-settimanali-ANPR-1/comuni_settimana.xlsx')
    df = pd.read_excel('/home/chirag/Research/Projects/covid-19-data/data/Italy/march28_total_deaths_2015-2020/raw_mortality_data/dati-comunali-settimanali-ANPR-1/comuni_settimana.xlsx') 
    weeks = df['SETTIMANA'][:11]
    ages = np.unique(df['CLASSE_DI_ETA'])
    provinces = np.unique(df['NOME_PROVINCIA'].values)

    colsave = ['week', 'province', 'region', 'age_group', 'male', 'female', 'total']
    years = [2015, 2016, 2017, 2018, 2019, 2020]

    dfsave = pd.DataFrame(columns=colsave)

    for province in provinces:
        tmp0 = df[df['NOME_PROVINCIA'] == province]
        region = tmp0['NOME_REGIONE'].values[0]

        for ia, age in enumerate(ages):

            for year in years:
                cols = ['MASCHI_%d'%year, 'FEMMINE_%d'%year, 'TOTALE_%d'%year]            
                weeklabel = [i[:5] + '/%d'%year + i[5:11]+ '/%d'%year for i in weeks]
                for iw, week in enumerate(weeks):
                    deaths = tmp0[(tmp0['CLASSE_DI_ETA'] == age) & (tmp0['SETTIMANA'] == week)][cols].sum().astype(float).tolist()
                    entry = np.array([weeklabel[iw], province, region, ia] + deaths).reshape(1, -1)
                    dfsave = dfsave.append(pd.DataFrame(entry, columns=colsave), ignore_index=True)

    #dfsave = dfsave.replace('Emilia-Romagna', 'Emilia Romagna')
    dfsave = dfsave.replace('Friuli-Venezia Giulia', 'Friuli Venezia Giulia')
    dfsave = dfsave.replace("Valle d'Aosta/Vallée d'Aoste", "Valle d'Aosta")

    dfsave.to_csv('../data/Italy/march28_total_deaths_2015-2020/province_historic_mortality.tsv', sep='\t', encoding='utf-8')
    #dfsave.to_csv('../data/Italy/new_total_deaths_2015_2020/province_historic_mortality.tsv', sep='\t', encoding='utf-8')


    
def regional_new():
    #df = pd.read_excel('/home/chirag/Research/Projects/covid-19-data/data/Italy/new_total_deaths_2015_2020/raw_mortality_data/dati-comunali-settimanali-ANPR-1/comuni_settimana.xlsx')
    df = pd.read_excel('../data/Italy/march28_total_deaths_2015-2020/raw_data/comuni-settimana/comuni_settimana.xlsx')
    weeks = df['SETTIMANA'][:12]
    ages = np.unique(df['CLASSE_DI_ETA'])
    regions = np.unique(df['NOME_REGIONE'].values)


    colsave = ['week', 'region', 'age_group', 'male', 'female', 'total']
    years = [2015, 2016, 2017, 2018, 2019, 2020]

    dfsave = pd.DataFrame(columns=colsave)

    for region in regions:
        print(region)
        tmp0 = df[df['NOME_REGIONE'] == region]

        for ia, age in enumerate(ages):

            for year in years:
                cols = ['MASCHI_%d'%year, 'FEMMINE_%d'%year, 'TOTALE_%d'%year]            
                weeklabel = [i[:5] + '/%d'%year + i[5:11]+ '/%d'%year for i in weeks]
                for iw, week in enumerate(weeks):
                    deaths = tmp0[(tmp0['CLASSE_DI_ETA'] == age) & (tmp0['SETTIMANA'] == week)][cols].sum().astype(float).tolist()
                    entry = np.array([weeklabel[iw], region, ia] + deaths).reshape(1, -1)
                    dfsave = dfsave.append(pd.DataFrame(entry, columns=colsave), ignore_index=True)

    #dfsave = dfsave.replace('Emilia-Romagna', 'Emilia Romagna')
    dfsave = dfsave.replace('Friuli-Venezia Giulia', 'Friuli Venezia Giulia')
    dfsave = dfsave.replace("Valle d'Aosta/Vallée d'Aoste", "Valle d'Aosta")

    #dfsave.to_csv('../data/Italy/new_total_deaths_2015_2020/regional_historic_mortality.tsv', sep='\t', encoding='utf-8')
    dfsave.to_csv('../data/Italy/march28_total_deaths_2015-2020/regional_historic_mortality.tsv', sep='\t', encoding='utf-8')


def regional_fine():
    #df = pd.read_excel('/home/chirag/Research/Projects/covid-19-data/data/Italy/new_total_deaths_2015_2020/raw_mortality_data/dati-comunali-settimanali-ANPR-1/comuni_settimana.xlsx')
    df = pd.read_excel('../data/Italy/march28_total_deaths_2015-2020/raw_data/comuni-settimana/comuni_settimana.xlsx')
    weeks = ['01/01/2015-11/01/2015', '12/01/2015-18/01/2015',
             '19/01/2015-25/01/2015', '26/01/2015-01/02/2015',
             '02/02/2015-08/02/2015', '09/02/2015-15/02/2015',
            '16/02/2015-22/02/2015', '23/02/2015-29/02/2015',
             '01/03/2015-07/03/2015', '08/03/2015-14/03/2015',
             '15/03/2015-21/03/2015', '22/03/2015-28/03/2015']

    df = pd.read_csv('../data/Italy/march28_total_deaths_2015-2020/raw_data/comune-giorno/comune_giorno.csv', encoding='latin1')
    df = df.rename(columns={'NOME_COMUNE':'town', 'NOME_REGIONE':'region', 'NOME_PROVINCIA':'province', 'CL_ETA':'ages', 'GE':'dates'})
    df = df[df['dates'] <=328]
    dfwaste = df[(df['TOTALE_20'] == 9999)]
    dfcut = df[~(df['TOTALE_20'] == 9999).values]


    colsave = ['week', 'region', 'age_group', 'male', 'female', 'total']
    dfsave = pd.DataFrame(columns=colsave, dtype=None)
    ages = np.arange(22)
    years = [15, 16, 17, 18, 19, 20]
    dates = [[101, 111], [112, 118], [119, 125], [126, 201], [202, 208], [209, 215], [216, 222], [223, 229],
        [301, 307], [308, 314], [315, 321], [322, 328]]
    
    regions = np.unique(df['region'].values)
    for region in regions:
        print(region)
        tmp = dfcut[dfcut['region'] == region]

        for ia, age in enumerate(ages):
            tmpa = tmp[(tmp['ages'] == age)]
            for year in years:
                cols = ['MASCHI_%d'%year, 'FEMMINE_%d'%year, 'TOTALE_%d'%year]
                weeklabel = [i[:8] + '%d'%year + i[10:-2]+ '%d'%year for i in weeks]
                
                for iw, week in enumerate(weeks):
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
    #dfsave.to_csv('/home/chirag/Research/Projects/covid-19-data/data/Italy/new_total_deaths_2015_2020/regional_historic_mortality_fine.tsv', sep='\t', encoding='utf-8')
    dfsave.to_csv('../data//Italy/march28_total_deaths_2015-2020/regional_historic_mortality_fine.tsv', sep='\t', encoding='utf-8')


def regional_daily():

    df = pd.read_csv('/home/chirag/Research/Projects/covid-19-data/data/Italy/march28_total_deaths_2015-2020/raw_data/comune-giorno/comune_giorno.csv', encoding='latin1')
    df = df.rename(columns={'NOME_COMUNE':'town', 'NOME_REGIONE':'region', 'NOME_PROVINCIA':'province', 'CL_ETA':'ages', 'GE':'dates'})
    df = df[df['dates'] <=328]
    dfwaste = df[(df['TOTALE_20'] == 9999)]
    dfcut = df[~(df['TOTALE_20'] == 9999).values]


    colsave = ['dateindex', 'date', 'region', 'age_group', 'male', 'female', 'total']
    dfsave = pd.DataFrame(columns=colsave, dtype=None)

    dates = np.concatenate([np.arange(101, 132), np.arange(201, 230), np.arange(301, 329)])
    datelabel = ['%s/%s'%(str(i)[0], str(i)[1:]) for i in dates]
    ages = np.arange(22)
    years = [15, 16, 17, 18, 19, 20]

    dfsave = pd.DataFrame(columns=colsave, dtype=None)
    regions = np.unique(df['region'].values)

    for region in regions:
        print(region)
        tmp = dfcut[dfcut['region'] == region]
        for ia, age in enumerate(ages):
            tmpa = tmp[(tmp['ages'] == age)]
            yrentries = []
            for year in years:
                cols = ['MASCHI_%d'%year, 'FEMMINE_%d'%year, 'TOTALE_%d'%year]
                datelabelyr = [d + '/20%d'%year for d in datelabel]
                entries = []
                for idd, date in enumerate(dates):
                    deaths = tmpa[tmpa['dates'] == date][cols].sum().astype(float).tolist()
                    entries.append([date, datelabelyr[idd], region, ia] + deaths)
                dfsave = dfsave.append(pd.DataFrame(np.array(entries), columns=colsave), ignore_index=True)

    dfsave['age_group'] = dfsave['age_group'].astype(int) 
    dfsave['male'] = dfsave['male'].astype(float) 
    dfsave['female'] = dfsave['female'].astype(float) 
    dfsave['total'] = dfsave['total'].astype(float)     

    dfsave = dfsave.replace('Friuli-Venezia Giulia', 'Friuli Venezia Giulia')
    dfsave = dfsave.replace("Valle d'Aosta/Vallée d'Aoste", "Valle d'Aosta")
    #dfsave.to_csv('/home/chirag/Research/Projects/covid-19-data/data/Italy/new_total_deaths_2015_2020/regional_historic_mortality_fine.tsv', sep='\t', encoding='utf-8')
    dfsave.to_csv('../data//Italy/march28_total_deaths_2015-2020/regional_historic_mortality_fine_daily.tsv', sep='\t', encoding='utf-8')



    
def region_deaths():
    df = pd.read_csv('../../covid-19-data/data/Italy/regional_deaths_2018_raw.csv')
    df = df[4:][['Unnamed: 1', 'Unnamed: 2']]
    df = pd.DataFrame(df.values, columns=['region', 'deaths_2018'])
    #df = df.replace('Emilia-Romagna', 'Emilia Romagna')
    df = df.replace('Friuli-Venezia Giulia', 'Friuli Venezia Giulia')
    df = df.replace('Trentino-South Tyrol', 'Trentino-Alto Adige/Südtirol')
    df = df.replace('Aosta Valley', "Valle d'Aosta")
    df = df.replace('Lombardy', "Lombardia")
    df = df.replace('Tuscany', "Toscana")
    df = df.replace('Sardinia', "Sardegna")
    df = df.replace('Sicily', "Sicilia")
    df = df.replace('Apulia', "Puglia")
    df = df.replace('Piedmont', 'Piemonte')

    df.to_csv('../data/Italy/regional_deaths_2018.tsv', sep='\t', encoding='utf-8')


def pop_ratio():
    #df = pd.read_excel('/home/chirag/Research/Projects/covid-19-data/data/Italy/new_total_deaths_2015_2020/raw_mortality_data/dati-comunali-settimanali-ANPR-1/comuni_settimana.xlsx', encoding='latin1')
    df = pd.read_excel('../data/Italy/march28_total_deaths_2015-2020/raw_data/comuni-settimana/comuni_settimana.xlsx')
    df2 = pd.read_excel('/home/chirag/Research/Projects/covid-19-data/data/Italy/Elenco-comuni-italiani.xls', encoding='latin1')
    df2 = df2.rename(columns={'Popolazione legale 2011 (09/10/2011)':'population'})
    df2 = df2.rename(columns={'Codice Comune formato alfanumerico':'commune_code'})
    regions = np.unique(df['NOME_REGIONE'].values)
    
    savecols = ['REG', 'region', 'total_commune', 'mortality_commune', 'total_population', 'mortality_population']
    dfsave = pd.DataFrame(columns=savecols)
    
    regcodes = {}
    for i in range(1, 21): regcodes[df[df['REG'] == i]['NOME_REGIONE'].values[0]] = i
    
    for _, region in enumerate(regions):
        ir = regcodes[region]
        tmp = df[df['REG'] == ir]
        tmp2 = df2[df2['Codice Regione'] == ir]
        total_pop = tmp2.sum()['population']
        ccode2 = np.unique(tmp2['commune_code'].values)
        popdict = dict(tmp2[['commune_code', 'population']].values)

        ccode = np.unique(tmp['COD_PROVCOM'].values)
        pop = 0
        for cc in ccode: 
            pop += popdict[cc]

        tosave = np.array([ir+1, region, ccode2.size, ccode.size, total_pop, pop]).reshape(1, -1)
        dfsave = dfsave.append(pd.DataFrame(tosave, columns=savecols))
        
    dfsave = dfsave.replace('Friuli-Venezia Giulia', 'Friuli Venezia Giulia')
    dfsave = dfsave.replace("Valle d'Aosta/Vallée d'Aoste", "Valle d'Aosta")
    #dfsave.to_csv('../data/Italy/new_total_deaths_2015_2020/regional_population_fraction.tsv', sep='\t', encoding='utf-8')
    dfsave.to_csv('../data/Italy/march28_total_deaths_2015-2020/regional_population_fraction.tsv', sep='\t', encoding='utf-8')


def pop_dist():
    dfpopage = pd.read_excel('../../covid-19-data/data/Italy/covid-19-data/population-in-by-age-group.xlsx', sheet_name='Data')
    v1, v2 = dfpopage['Unnamed: 2'][-2:].values
    ratio = v1/(v1+v2)

    dfagedist = pd.read_excel('../../covid-19-data/data/Italy/covid-19-data/age-distribution--by-region.xlsx', sheet_name='Data')
    tosave = dfagedist.values[4:, 1:-1]
    old = tosave[:, -1]
    old = np.array([old*ratio, old*(1-ratio)]).T
    tosave = np.hstack([tosave[:, :-1], old])
    colsave = ['region', 'age_0', 'age_1', 'age_2', 'age_3']
    df = pd.DataFrame(tosave, columns=colsave)
    df = df.replace('Friuli-Venezia Giulia', 'Friuli Venezia Giulia')
    df = df.replace('Trentino-South Tyrol', 'Trentino-Alto Adige/Südtirol')
    df = df.replace('Aosta Valley', "Valle d'Aosta")
    df = df.replace('Lombardy', "Lombardia")
    df = df.replace('Tuscany', "Toscana")
    df = df.replace('Sardinia', "Sardegna")
    df = df.replace('Sicily', "Sicilia")
    df = df.replace('Apulia', "Puglia")
    df = df.replace('Piedmont', 'Piemonte')
    df.to_csv('../data/Italy/regional_pop_dist.tsv', sep='\t', encoding='utf-8')
    


if __name__=="__main__":

    #province()
    #regional()
    #regional_new()
    #province_new()
    #region_deaths()
    #pop_ratio()
    #pop_dist()
    #regional_fine()
    regional_daily()
    
