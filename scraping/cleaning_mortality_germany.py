import numpy as np
import pandas as pd

xls =  pd.ExcelFile('../data/Germany/sterbefaelle.xlsx')
df = pd.read_excel('../data/Germany/sterbefaelle.xlsx', sheet_name=None)


def clean():

    dfsave = pd.DataFrame()
    colsave = ['date', 'death']
    # colsave = colsave + [list(i)[0] for i in list(df['2016_Tage'][10:-2][cols[:1]].values)]
    colsave = colsave + [i for i in df['2016_Tage'][10:-2]['Unnamed: 0'].values]
    for yr in [2016, 2017, 2018]:
        cols = df['%d_Tage'%yr].columns.copy()
        tosave = []
        tosave.append(df['%d_Tage'%yr][7:8][cols[1:-1]].values) #date
        tosave.append(df['%d_Tage'%yr][-1:][cols[1:-1]].values) #total
        tosave.append(df['%d_Tage'%yr][10:-2][cols[1:-1]].values) #age group
        tosave = np.concatenate(tosave, axis=0).T
        dfsave = dfsave.append(pd.DataFrame(data=tosave, columns = colsave), ignore_index=True)

    dfsave.to_csv('../data/Germany/national_historic_mortality.tsv', sep='\t', encoding='utf-8')

    ###########

    dfsave = pd.DataFrame()
    colsave = ['date', 'month', 'death']
    colsave = colsave + [i for i in df['2016_Monate'][10:-2]['Unnamed: 0'].values]

    for yr in [2016, 2017, 2018]:
        cols = df['%d_Monate'%yr].columns.copy()
        tosave = []
        tosave.append(np.array(['%d-%02d'%(yr, i) for i in range(1, 13)]).reshape(1, -1)) #date
        tosave.append(df['%d_Monate'%yr][7:8][cols[1:-1]].values) #month
        tosave.append(df['%d_Monate'%yr][-1:][cols[1:-1]].values) #total
        tosave.append(df['%d_Monate'%yr][10:-2][cols[1:-1]].values) #age group
        tosave = np.concatenate(tosave, axis=0).T
        dfsave = dfsave.append(pd.DataFrame(data=tosave, columns = colsave), ignore_index=True)


    dfsave.to_csv('../data/Germany/national_historic_mortality_monthly.tsv', sep='\t', encoding='utf-8')


if __name__=="__main__":
    clean()
