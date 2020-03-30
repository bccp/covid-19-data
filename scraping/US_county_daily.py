from argparse import ArgumentParser
import json
import os.path
import requests
import sys
import pandas as pd
import io



def scrape():

    url="https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"
    s=requests.get(url).content
    df=pd.read_csv(io.StringIO(s.decode()))
    df.rename(columns={'deaths':'death'}, inplace=True)
    df.to_csv('../data/US/county_daily.tsv', sep='\t', encoding='utf-8')
    return df


def scrape_JHU():

    with open('../data/US/US_pop_density.json') as ff:
        states = json.load(ff)['data']
        
    df = pd.DataFrame()
    for mm in [1, 2, 3]:
        for dd in np.arange(1, 32):
            url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/%02d-%d-2020.csv'%(mm, dd)
            s=requests.get(url).content        
            c=pd.read_csv(io.StringIO(s.decode()))
            if c.size:
                for iss, state in enumerate(states):
                    try:
                        ss = state['State']
                        df = df.append(c[c['Province_State'] == ss]) 
                    except : pass
    df.rename(columns={'Admin2':'county', 'Deaths':'death'}, inplace=True)
    df.to_csv('../data/US/county_daily_JHU.tsv', sep='\t', encoding='utf-8')
                

if __name__=="__main__":

    _ = scrape()
    

