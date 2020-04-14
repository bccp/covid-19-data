import numpy as np
import pandas as pd
from scipy import stats

dfpop = pd.read_csv('../../covid-19-data/data/Italy/regional_pop_dist_byyear.csv')

# bin size in years
nyearbin = 10
# regions we might want
#regions = ['Emilia-Romagna', 'Lazio', 'Liguria', 'Lombardia', 'Marche', 'Molise', 'Piemonte', 'Puglia', 'Sardegna', 'Sicilia', 'Toscana', 'Umbria', 'Veneto']
df = pd.read_excel('../data/Italy/march28_total_deaths_2015-2020/raw_data/comuni-settimana/comuni_settimana.xlsx')
regions = np.unique(df['NOME_REGIONE'].values)
regions = np.append(regions, 'Bergamo')

print('Regions: ', regions)

ages = np.arange(101) # last year is 100+
age_bins = np.arange(100//nyearbin + 1)*nyearbin 
age_bins[0] = 0
age_bins[-1] = 110
print("Age bins : ", age_bins)

binned_pop = {}
for region in regions:
    tmp = dfpop[dfpop['Territory'] == region]
    
    if tmp.shape[0] > 0:
        # last index is total
        N = tmp['Value'].values[:-1] # number of people for each age year
        Nb, bin_edges, binnumber = stats.binned_statistic(ages, N, statistic='sum', bins=age_bins)
        binned_pop[region] = Nb.astype(int)

colnames = ['{:d}-{:d} years'.format(age_bins[i], age_bins[i+1]-1) for i in range(len(age_bins[:-1]))]

print('\nbinned into columns: ', colnames)

# save as csv
df = pd.DataFrame.from_dict(binned_pop, orient='index',columns=colnames)
df = df.replace('Friuli-Venezia Giulia', 'Friuli Venezia Giulia')
df = df.replace("Valle d'Aosta/Vallée d'Aoste", "Valle d'Aosta")

df.index.name='region'

df.to_csv('../../covid-19-data/data/Italy/regional_pop_dist_bybin.tsv', '\t')
