#Data scraped from JHU time series for different regions in Canada
import numpy as np
from argparse import ArgumentParser
import json
import os.path
import requests
import sys
import pandas as pd
import io

def scrape():

    url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
    s=requests.get(url).content
    c0=pd.read_csv(io.StringIO(s.decode()))
    url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
    s=requests.get(url).content
    c1=pd.read_csv(io.StringIO(s.decode()))
    url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'
    s=requests.get(url).content
    c2=pd.read_csv(io.StringIO(s.decode()))


    cc = 'Canada'
    c0 = c0[(c0['Country/Region'] == cc)]
    c1 = c1[(c1['Country/Region'] == cc)]
    c2 = c2[(c2['Country/Region'] == cc)]

    states = np.unique(c0['Province/State'].values)
    dates = c0.columns[4:]

    df = pd.DataFrame()

    for ic, cc in enumerate(states):
        confirmed = c0[(c0['Province/State'] == cc)].sum(numeric_only=True).values[2:]
        deaths = c1[(c1['Province/State'] == cc)].sum(numeric_only=True).values[2:]
        recovered = c2[(c2['Province/State'] == cc)].sum(numeric_only=True).values[2:]
        country = [cc]*deaths.size
        data = np.array([dates, country, confirmed, deaths, recovered]).T
        df = df.append(pd.DataFrame(data, columns=['date', 'state', 'confirmed', 'death', 'recovered']), ignore_index=True)

    df.to_csv('../data/Canada/jhu.tsv', sep='\t', encoding='utf-8')
    return df


if __name__=="__main__":

    _ = scrape()
    


