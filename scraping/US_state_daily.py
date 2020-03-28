from argparse import ArgumentParser
import json
import os.path
import requests
import sys
import pandas as pd
import io



def scrape():

    url="https://raw.githubusercontent.com/COVID19Tracking/covid-tracking-data/master/data/states_daily_4pm_et.csv"
    s=requests.get(url).content
    df=pd.read_csv(io.StringIO(s.decode()))
    df.to_csv('../data/US/states_daily.tsv', sep='\t', encoding='utf-8')
    return df


if __name__=="__main__":

    _ = scrape()
    

