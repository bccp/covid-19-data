from argparse import ArgumentParser
import json
import os.path
import requests
import sys
import pandas as pd

def scrape():

    url_province="https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-province.json"
    url_national="https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-andamento-nazionale.json"
    url_regional="https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-regioni.json"

    with open("../data/Italy/translate.json") as ff:
        translate = json.load(ff)

    dfs = []
    s=requests.get(url_province).json()
    df = pd.DataFrame.from_dict(s)
    for key in translate:
        try:    df.rename(columns = {key:translate[key]}, inplace=True)
        except: pass
    df.to_csv('../data/Italy/province_daily.tsv', sep='\t', encoding='utf-8')
    dfs.append(df)

    s=requests.get(url_regional).json()
    df = pd.DataFrame.from_dict(s)
    for key in translate:
        try:    df.rename(columns = {key:translate[key]}, inplace=True)
        except: pass
    df.to_csv('../data/Italy/regional_daily.tsv', sep='\t', encoding='utf-8')
    dfs.append(df)

    s=requests.get(url_national).json()
    df = pd.DataFrame.from_dict(s)
    for key in translate:
        try:    df.rename(columns = {key:translate[key]}, inplace=True)
        except: pass
    df.to_csv('../data/Italy/national_daily.tsv', sep='\t', encoding='utf-8')
    dfs.append(df)

    return dfs

if __name__=="__main__":

    _ = scrape()
#    df = scrape(urljson=url_province)
#    df.to_csv('../data/Italy/province_daily.tsv', sep='\t', encoding='utf-8')
#
#    df = scrape(urljson=url_national)
#    df.to_csv('../data/Italy/national_daily.tsv', sep='\t', encoding='utf-8')
#
#    df = scrape(urljson=url_regional)
#    df.to_csv('../data/Italy/regional_daily.tsv', sep='\t', encoding='utf-8')
#
#
#
