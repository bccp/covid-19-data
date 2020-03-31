import numpy as np
import pandas as pd

def collect_and_save():

    df1 = pd.read_csv('../data/US/US_county_population_estimate_data.csv')
    df2 = pd.read_csv('../data/US/US_county_area_data_2010.csv')

    df1cols = df1.columns
    df2cols = df2.columns
    cols_to_save = df2cols[[6, 4, 7, 8, 9, 11, 12, 13]]
    states = np.unique(df1['STNAME'].values)
    
    colheader = ['state', 'county_name', 'fips', 'population_2010', 'housing_units', 'total_area_sqmiles', 'land_area_sqmiles', 'population_density', 'housing_density', 'population_2010_est', 'population_2019_est']
    df = pd.DataFrame(columns=colheader)

    for iss, ss in enumerate(states):
        #get population in 2019
        tmp = df1[df1['STNAME'] == ss][1:]
        pops = tmp[df1cols[[8, 18]]].values
        #get area and population, housing and densities in 2010
        props = []
        for i in tmp['CTYNAME']:
            try:
                matchkey = 'United States - %s - %s'%(ss, i)
                entry = df2[df2["GCT_STUB.display-label"] == matchkey][cols_to_save].values.tolist()[0]
            except:
                entry = [np.NaN] * len(cols_to_save)
            props.append(['%s'%ss] + entry)
        props = np.array(props)
        #combine and save
        tosave = np.concatenate([props, pops], axis=1)
        df = df.append(pd.DataFrame(tosave, columns=colheader), ignore_index=True)

    df.to_csv('../data/US/county_popdata.tsv', sep='\t', encoding='utf-8')



if __name__ == "__main__":
    collect_and_save()
    


        
    
